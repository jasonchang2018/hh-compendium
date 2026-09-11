#!/usr/bin/env python3
"""
Automated AI Documentation Enrichment (Step 6)
================================================
Calls Claude (via the Anthropic API) to replace the structural/deterministic
documentation produced by generate_documentation.py (Step 4) and
enrich_documentation.py (Step 5) with narrative, plain-English versions —
automating what AI_DOCUMENTATION_PROMPT.md otherwise asks a human/agent to
do by hand.

Disabled by default. Set AI_ENRICHMENT_ENABLED=true (and ANTHROPIC_API_KEY)
to enable. When disabled, this script no-ops (exit 0) and run_pipeline.py
falls back to printing the existing manual-enrichment reminder instead.

One Anthropic API call per output document (not one combined call): once
per Talend job, once per Qlik app, and once each for the four system-level
docs (01_system_architecture.md, 04_data_lineage_map.md,
05_operational_runbook.md, 06_dependency_matrix.md). Each call is given the
existing deterministic file (already written by Steps 4/5) as ground truth,
plus a sanitized JSON slice of the extracted metadata, and its response
overwrites that file directly.

Requires Steps 4 and 5 to have already run — this script reads their output
as input; it does not synthesize documents from JSON alone.

Usage:
    AI_ENRICHMENT_ENABLED=true ANTHROPIC_API_KEY=sk-... \
        uv run src/documentation/ai_enrich_documentation.py \
        --talend talend_metadata.json --qlik qlik_metadata.json \
        --output ./documentation/
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from llm_client import LLMProvider, get_provider

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = "config/llm.yaml"

# ---------------------------------------------------------------------------
# Sanitization — defense-in-depth before any metadata leaves the process
# bound for a third-party API. This sits on top of, not instead of, the
# extractors' own name-based redaction (SENSITIVE_PARAM_NAMES /
# SENSITIVE_CONN_PROPS in talend_extractor.py / qlik_cloud_extractor.py).
# ---------------------------------------------------------------------------

DENY_KEY_SUBSTRINGS = {
    "password", "secret", "token", "key", "connection_string", "credential", "value",
}

JOB_ALLOWED_TOP_LEVEL_KEYS = {
    "name", "purpose", "description", "version", "project", "job_type", "framework",
    "author", "created_date", "modified_date", "components", "connections",
    "context_groups", "subjobs", "file_path",
}

APP_ALLOWED_TOP_LEVEL_KEYS = {
    "id", "name", "description", "space_id", "owner_id", "created_at", "updated_at",
    "load_script", "script_sections", "extracted_tables", "reload_tasks",
    "last_reload_time", "published", "publish_time",
}


def _strip_denied_keys(obj):
    """Recursively drop any dict key whose name matches a deny-list substring."""
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            if any(bad in k.lower() for bad in DENY_KEY_SUBSTRINGS):
                continue
            cleaned[k] = _strip_denied_keys(v)
        return cleaned
    if isinstance(obj, list):
        return [_strip_denied_keys(item) for item in obj]
    return obj


def sanitize_payload(data: dict, allowed_top_level_keys: set[str] | None = None) -> dict:
    """
    Allow-lists expected top-level keys (when given) and recursively strips
    anything that looks like a credential/literal value at any nesting depth.

    Intentionally conservative: logs (rather than silently drops) any
    unexpected top-level key, so a newly-added extractor field can't leak
    unreviewed.
    """
    cleaned: dict = {
        k: _strip_denied_keys(v)
        for k, v in data.items()
        if not any(bad in k.lower() for bad in DENY_KEY_SUBSTRINGS)
    }
    if allowed_top_level_keys is not None:
        unexpected = set(cleaned.keys()) - allowed_top_level_keys
        if unexpected:
            logger.info(f"Sanitizer passed through unlisted top-level keys: {unexpected} — review if unexpected.")
    return cleaned


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

GROUND_RULES = """\
Ground rules:
- Base your description ONLY on the structured metadata and the existing
  document provided below. Do not invent functionality, business purpose,
  or data meaning that isn't evidenced by them.
- Treat the existing document's tables and factual statements as ground
  truth — keep them (verbatim or reformatted, but not contradicted), and
  add narrative, explanation, and plain-English translation on top of them.
- When you must infer something (e.g. a job's business purpose from its
  name and component structure), clearly mark it under an
  "Inferred / Needs Verification" section rather than stating it as fact
  elsewhere.
- Do not fabricate sample data, connection strings, or credentials. If none
  were provided, do not include any.
- Write for a developer who has never seen this system before and needs to
  understand it to safely modify or debug it.
- Be concise. Prefer plain, direct language over marketing-style or padded
  descriptions.
- Output ONLY the final Markdown document — no preamble, no explanation of
  what you're about to do, no closing remarks.
"""

JOB_SYSTEM_PROMPT = f"""\
You are documenting an existing Talend ETL job for internal engineering reference.

{GROUND_RULES}
Produce a complete replacement for `talend/<ProjectName>/job_<JobName>.md` with
these sections: Overview, Detail table (Job name, Version, Project, Author,
Created, Last Modified — omit a row if the metadata has none), Step-by-step
data flow, Settings tables (per source/target component, with a "what it
means" column), Dependencies & configuration, Glossary (Talend component
types used, in plain English), and Issues observed (only if evident from the
metadata; omit the section otherwise).
"""

APP_SYSTEM_PROMPT = f"""\
You are documenting an existing Qlik Cloud app for internal engineering reference.

{GROUND_RULES}
Produce a complete replacement for `qlik/app_<AppName>.md` with these
sections: Overview, Detail table (App name, Space, Published status — omit a
row if the metadata has none), Data model (what data it loads and from
where, tables/relationships, in plain English rather than raw load-script
text), Settings table (data connections and reload schedule, with a "what it
means" column), Glossary (Qlik-specific terms used), and Issues observed
(only if evident from the metadata; omit the section otherwise).
"""

# Requirements text per system-level doc, mirroring items 1/4/5/6 of
# generate_documentation.py's generate_ai_prompt() so the automated and
# manual paths ask for the same structure.
SYSTEM_DOC_REQUIREMENTS = {
    "01_system_architecture.md": """\
Produce a complete replacement for `01_system_architecture.md` with these
sections:
- Overview — one short paragraph on what the platform does end to end
  (sources -> Talend ETL -> Snowflake -> Qlik Cloud).
- Detail table — project/tenant name, total Talend jobs, total DB
  connections, total Qlik apps (use the extracted summary counts; omit a row
  if the metadata has none).
- Data flow — the overall path from sources through Talend ETL into
  Snowflake and out to Qlik dashboards, as a Mermaid diagram.
- Glossary — a short table translating recurring platform terms (e.g. Space,
  Reload task, Context group) into plain English.
""",
    "04_data_lineage_map.md": """\
Produce a complete replacement for `04_data_lineage_map.md` with these
sections:
- Overview — one short paragraph on how to read the lineage trace that
  follows.
- Trace — source -> Talend job -> Snowflake table -> Qlik app, as a Mermaid
  flowchart, plus a plain-English walkthrough of each hop.
- Gaps — any point in the chain that could not be determined from the
  metadata, stated explicitly as unknown rather than inferred.
""",
    "05_operational_runbook.md": """\
Produce a complete replacement for `05_operational_runbook.md` with these
sections:
- Overview — one short paragraph on what this runbook covers.
- How-to sections — numbered, plain-English steps for: monitoring job/reload
  status, restarting a failed job, and troubleshooting the most likely
  failure modes evident from the metadata (e.g. missing schema, hardcoded
  connection values).
- Glossary — a short table translating any ops-specific terms used that
  weren't already covered elsewhere.
""",
    "06_dependency_matrix.md": """\
Produce a complete replacement for `06_dependency_matrix.md` with these
sections:
- Overview — one short paragraph on what the matrix shows and how to read
  it.
- Matrix table — which jobs depend on which connections and context groups.
- Notes — plain-English callouts for anything in the matrix that looks risky
  (e.g. many jobs sharing one connection, a job with no visible dependencies
  that seems like it should have some).
""",
}


def system_doc_prompt(filename: str) -> str:
    return f"You are a senior data platform engineer and technical writer, reverse-engineering an undocumented Talend + Qlik data platform for the engineers who now own it.\n\n{GROUND_RULES}\n{SYSTEM_DOC_REQUIREMENTS[filename]}"


def build_user_prompt(existing_doc: str, metadata_json: str) -> str:
    return f"""\
Existing document (ground truth for facts/tables — keep or reformat, don't contradict):
---
{existing_doc}
---

Structured metadata (extracted from the platform):
---
{metadata_json}
---
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def safe_filename(name: str) -> str:
    """Sanitize a string for safe use as a filesystem path component.

    Duplicated from generate_documentation.py's safe_filename() so this
    script can construct the same job_<JobName>.md / app_<AppName>.md paths
    without importing across stage scripts (this repo's existing
    standalone-script precedent — see CLAUDE.md).
    """
    return (
        "".join(c if c.isalnum() or c in "-_ " else "_" for c in name)
        .strip()
        .replace(" ", "_")
    )


class EnrichmentTarget:
    def __init__(self, path: Path, system_prompt: str, payload: dict, label: str):
        self.path = path
        self.system_prompt = system_prompt
        self.payload = payload
        self.label = label


def collect_targets(talend: dict | None, qlik: dict | None, output_dir: Path) -> list[EnrichmentTarget]:
    targets: list[EnrichmentTarget] = []

    if talend:
        for project in talend.get("projects", []):
            proj_dir = output_dir / "talend" / project["name"]
            for job in project.get("jobs", []):
                job_name = safe_filename(job.get("name", "Unknown"))
                targets.append(
                    EnrichmentTarget(
                        path=proj_dir / f"job_{job_name}.md",
                        system_prompt=JOB_SYSTEM_PROMPT,
                        payload=sanitize_payload(job, JOB_ALLOWED_TOP_LEVEL_KEYS),
                        label=f"job:{project['name']}/{job.get('name', 'Unknown')}",
                    )
                )

    if qlik:
        qlik_dir = output_dir / "qlik"
        for app in qlik.get("apps", []):
            safe_name = safe_filename(app.get("name", "Unknown"))
            targets.append(
                EnrichmentTarget(
                    path=qlik_dir / f"app_{safe_name}.md",
                    system_prompt=APP_SYSTEM_PROMPT,
                    payload=sanitize_payload(app, APP_ALLOWED_TOP_LEVEL_KEYS),
                    label=f"app:{app.get('name', 'Unknown')}",
                )
            )

    system_payload = sanitize_payload({"talend": talend or {}, "qlik": qlik or {}})
    for filename in SYSTEM_DOC_REQUIREMENTS:
        if filename in ("04_data_lineage_map.md", "06_dependency_matrix.md") and not talend:
            continue
        targets.append(
            EnrichmentTarget(
                path=output_dir / filename,
                system_prompt=system_doc_prompt(filename),
                payload=system_payload,
                label=f"system-doc:{filename}",
            )
        )

    return targets


def enrich_target(llm: LLMProvider, target: EnrichmentTarget) -> bool:
    """Returns True on success. Failures are logged, not raised — a bad
    document must not abort the rest of the run."""
    if not target.path.is_file():
        logger.error(
            f"[{target.label}] Expected existing document at {target.path} but it doesn't exist. "
            "Run generate_documentation.py / enrich_documentation.py first."
        )
        return False

    existing_doc = target.path.read_text(encoding="utf-8")
    user_prompt = build_user_prompt(existing_doc, json.dumps(target.payload, indent=2))

    try:
        logger.info(f"Requesting enrichment for {target.label} -> {target.path}")
        response = llm.generate(system_prompt=target.system_prompt, user_prompt=user_prompt)
    except Exception as e:  # noqa: BLE001 - a single failed document must not abort the run
        logger.error(f"[{target.label}] Enrichment failed: {e}")
        return False

    logger.debug(f"[{target.label}] tokens in/out: {response.input_tokens}/{response.output_tokens}")
    target.path.write_text(response.text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Automated AI documentation enrichment (Step 6) — calls Claude to replace "
        "structural/deterministic docs with narrative versions, one API call per document.",
    )
    parser.add_argument(
        "--talend",
        default=os.environ.get("TALEND_METADATA_PATH"),
        help="Path to talend_metadata.json (from talend_extractor.py, or set TALEND_METADATA_PATH env var)",
    )
    parser.add_argument(
        "--qlik",
        default=os.environ.get("QLIK_METADATA_PATH"),
        help="Path to qlik_metadata.json (from qlik_cloud_extractor.py, or set QLIK_METADATA_PATH env var)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.environ.get("OUTPUT_DOCUMENTATION_PATH", "./documentation"),
        help="Documentation directory already populated by Steps 4/5 (default: ./documentation/, "
        "or set OUTPUT_DOCUMENTATION_PATH env var)",
    )
    parser.add_argument(
        "--config",
        default=os.environ.get("AI_ENRICHMENT_CONFIG", DEFAULT_CONFIG_PATH),
        help=f"Path to the LLM config YAML (default: {DEFAULT_CONFIG_PATH}, or set AI_ENRICHMENT_CONFIG env var)",
    )
    parser.add_argument("--model", default=None, help="Override the model configured in config/llm.yaml for this run")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be sent/written (document count) without calling the API or writing files",
    )
    args = parser.parse_args()

    if os.environ.get("AI_ENRICHMENT_ENABLED", "false").strip().lower() not in ("1", "true", "yes"):
        logger.info(
            "AI-powered enrichment is disabled by default. Set AI_ENRICHMENT_ENABLED=true "
            "(and ANTHROPIC_API_KEY) to enable this stage."
        )
        return

    if not args.talend and not args.qlik:
        logger.error("Provide at least one of --talend or --qlik")
        sys.exit(1)

    output_dir = Path(args.output)
    if not output_dir.is_dir():
        logger.error(f"Output directory {output_dir} doesn't exist — run generate_documentation.py first.")
        sys.exit(1)

    talend = load_json(args.talend) if args.talend else None
    qlik = None
    if args.qlik:
        try:
            qlik = load_json(args.qlik)
        except Exception as e:  # noqa: BLE001 -- a missing/malformed Qlik file must not abort the run
            logger.warning(f"Could not load --qlik metadata ({e}) — continuing with Talend only")

    targets = collect_targets(talend, qlik, output_dir)
    if not targets:
        logger.info("No jobs/apps/documents found to enrich.")
        return

    if args.dry_run:
        logger.info(f"Dry run: would send {len(targets)} API call(s), one per document:")
        for t in targets:
            logger.info(f"  {t.label} -> {t.path}")
        return

    try:
        config = load_config(args.config)
    except FileNotFoundError:
        logger.error(f"LLM config not found at {args.config}. See config/llm.yaml for the expected format.")
        sys.exit(1)

    llm = get_provider(config, model_override=args.model)

    succeeded, failed = 0, 0
    for target in targets:
        if enrich_target(llm, target):
            succeeded += 1
        else:
            failed += 1

    logger.info(f"AI enrichment complete: {succeeded} succeeded, {failed} failed, out of {len(targets)} document(s).")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
