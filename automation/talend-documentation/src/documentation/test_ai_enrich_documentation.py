"""Self-check for ai_enrich_documentation.py. Run directly: uv run src/documentation/test_ai_enrich_documentation.py

No real Anthropic API calls are made — enrich_target() is exercised against a
fake LLMProvider stub, and the CLI-level checks only exercise the disabled
(no-op) and --dry-run paths, neither of which needs ANTHROPIC_API_KEY.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ai_enrich_documentation import (
    EnrichmentTarget,
    collect_targets,
    enrich_target,
    safe_filename,
    sanitize_payload,
)
from llm_client import LLMResponse

AI_ENRICH_PATH = Path(__file__).parent / "ai_enrich_documentation.py"

TALEND_SAMPLE = {
    "projects": [
        {
            "name": "FA_ETL_Core",
            "jobs": [
                {
                    "name": "Nightly_Load",
                    "version": "1.2",
                    "project": "FA_ETL_Core",
                    "components": [{"unique_name": "tFileInputDelimited_1"}],
                    "connections": [],
                    "context_groups": [],
                    "db_password": "should-be-stripped",
                }
            ],
        }
    ]
}

QLIK_SAMPLE = {
    "apps": [
        {
            "id": "abc-123",
            "name": "Sales Dashboard",
            "space_id": "space-1",
            "reload_tasks": [],
            "api_key": "should-be-stripped",
        }
    ]
}


def test_sanitize_payload_strips_denied_substrings_recursively() -> None:
    cleaned = sanitize_payload({"name": "job", "nested": {"api_token": "x", "safe": "y"}})
    assert "api_token" not in cleaned["nested"]
    assert cleaned["nested"]["safe"] == "y"
    assert cleaned["name"] == "job"


def test_sanitize_payload_strips_lists_of_dicts() -> None:
    cleaned = sanitize_payload({"items": [{"secret": "x", "keep": "y"}]})
    assert "secret" not in cleaned["items"][0]
    assert cleaned["items"][0]["keep"] == "y"


def test_safe_filename_matches_generate_documentation_behavior() -> None:
    assert safe_filename("Nightly Load") == "Nightly_Load"
    assert safe_filename("Job/With:Weird*Chars") == "Job_With_Weird_Chars"


def test_collect_targets_builds_expected_paths_and_labels() -> None:
    output_dir = Path("/tmp/does-not-need-to-exist-for-this-check")
    targets = collect_targets(TALEND_SAMPLE, QLIK_SAMPLE, output_dir)

    job_targets = [t for t in targets if t.label.startswith("job:")]
    assert len(job_targets) == 1
    assert job_targets[0].path == output_dir / "talend" / "FA_ETL_Core" / "job_Nightly_Load.md"
    assert "db_password" not in job_targets[0].payload

    app_targets = [t for t in targets if t.label.startswith("app:")]
    assert len(app_targets) == 1
    assert app_targets[0].path == output_dir / "qlik" / "app_Sales_Dashboard.md"
    assert "api_key" not in app_targets[0].payload

    system_doc_targets = {t.path.name for t in targets if t.label.startswith("system-doc:")}
    assert system_doc_targets == {
        "01_system_architecture.md",
        "04_data_lineage_map.md",
        "05_operational_runbook.md",
        "06_dependency_matrix.md",
    }


def test_collect_targets_omits_talend_only_docs_without_talend_metadata() -> None:
    targets = collect_targets(None, QLIK_SAMPLE, Path("/tmp/unused"))
    system_doc_names = {t.path.name for t in targets if t.label.startswith("system-doc:")}
    assert "04_data_lineage_map.md" not in system_doc_names
    assert "06_dependency_matrix.md" not in system_doc_names
    assert "01_system_architecture.md" in system_doc_names


class _FakeLLM:
    def __init__(self, text: str = "# Enriched\n", raise_error: bool = False):
        self._text = text
        self._raise_error = raise_error

    def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        if self._raise_error:
            raise RuntimeError("simulated API failure")
        return LLMResponse(text=self._text, model="fake-model", input_tokens=10, output_tokens=5)


def test_enrich_target_writes_response_over_existing_file(tmp_dir: Path) -> None:
    target_path = tmp_dir / "job_Nightly_Load.md"
    target_path.write_text("# Deterministic placeholder\n")

    target = EnrichmentTarget(path=target_path, system_prompt="sys", payload={"name": "job"}, label="job:test")
    ok = enrich_target(_FakeLLM(text="# AI-Enriched Job Doc\n"), target)

    assert ok is True
    assert target_path.read_text() == "# AI-Enriched Job Doc\n"


def test_enrich_target_missing_file_fails_without_writing() -> None:
    target = EnrichmentTarget(
        path=Path("/tmp/definitely-does-not-exist/job_X.md"), system_prompt="sys", payload={}, label="job:missing"
    )
    ok = enrich_target(_FakeLLM(), target)
    assert ok is False


def test_enrich_target_api_failure_leaves_existing_file_untouched(tmp_dir: Path) -> None:
    target_path = tmp_dir / "job_Untouched.md"
    target_path.write_text("# Original\n")

    target = EnrichmentTarget(path=target_path, system_prompt="sys", payload={}, label="job:fail")
    ok = enrich_target(_FakeLLM(raise_error=True), target)

    assert ok is False
    assert target_path.read_text() == "# Original\n"


def _run_cli(args: list[str], env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(AI_ENRICH_PATH), *args],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_disabled_by_default_is_a_clean_noop(tmp_dir: Path) -> None:
    import os

    env = os.environ.copy()
    env.pop("AI_ENRICHMENT_ENABLED", None)
    env.pop("ANTHROPIC_API_KEY", None)

    result = _run_cli(["--talend", str(tmp_dir / "nonexistent.json")], env)
    assert result.returncode == 0, result.stderr
    assert "disabled by default" in result.stderr.lower() or "disabled by default" in result.stdout.lower()


def test_dry_run_lists_targets_without_api_key(tmp_dir: Path) -> None:
    import json
    import os

    talend_path = tmp_dir / "talend_metadata.json"
    talend_path.write_text(json.dumps(TALEND_SAMPLE))

    output_dir = tmp_dir / "documentation"
    output_dir.mkdir()

    env = os.environ.copy()
    env["AI_ENRICHMENT_ENABLED"] = "true"
    env.pop("ANTHROPIC_API_KEY", None)

    result = _run_cli(
        ["--talend", str(talend_path), "--output", str(output_dir), "--dry-run"],
        env,
    )
    assert result.returncode == 0, result.stderr
    assert "Nightly_Load" in result.stderr or "Nightly_Load" in result.stdout


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)
        test_sanitize_payload_strips_denied_substrings_recursively()
        test_sanitize_payload_strips_lists_of_dicts()
        test_safe_filename_matches_generate_documentation_behavior()
        test_collect_targets_builds_expected_paths_and_labels()
        test_collect_targets_omits_talend_only_docs_without_talend_metadata()
        test_enrich_target_writes_response_over_existing_file(tmp_dir)
        test_enrich_target_missing_file_fails_without_writing()
        test_enrich_target_api_failure_leaves_existing_file_untouched(tmp_dir)
        test_disabled_by_default_is_a_clean_noop(tmp_dir)
        test_dry_run_lists_targets_without_api_key(tmp_dir)
    print("All ai_enrich_documentation checks passed.")


if __name__ == "__main__":
    main()
