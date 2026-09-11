"""Self-check for talend_extractor.py Mode C (git-repo input). Run directly: uv run src/talend/test_mode_c.py"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from git_repo import (
    GitAccessError,
    clone_or_update_repo,
    get_commit_sha,
    is_git_url,
    redact_repo_url,
    resolve_auth,
)

TALEND_EXTRACTOR_PATH = Path(__file__).parent / "talend_extractor.py"

MINIMAL_ITEM_XML = '<?xml version="1.0"?><Process/>'


def _make_bare_repo_with_job(tmp_dir: Path) -> Path:
    """A local bare repo with one commit containing a minimal .item fixture,
    usable as a git remote via its filesystem path (file:// scheme) — no
    network needed. Caller must pass a fresh/unique tmp_dir per invocation
    (this always creates "fixture.git" / "fixture_work" under it)."""
    bare = tmp_dir / "fixture.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(bare)], check=True)
    work = tmp_dir / "fixture_work"
    subprocess.run(["git", "clone", str(bare), str(work)], check=True)
    (work / "process").mkdir(parents=True)
    (work / "process" / "TestJob_0.1.item").write_text(MINIMAL_ITEM_XML)
    subprocess.run(["git", "-C", str(work), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(work), "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "init"],
        check=True,
    )
    subprocess.run(["git", "-C", str(work), "push", "origin", "main"], check=True)
    return bare


def test_is_git_url() -> None:
    assert is_git_url("https://github.com/org/repo.git")
    assert is_git_url("git@host:org/repo.git")
    assert is_git_url("ssh://host/org/repo")
    assert is_git_url("file:///abs/path.git")
    assert is_git_url("some/repo.git")  # anything ending .git
    assert not is_git_url("/some/local/directory")
    assert not is_git_url("foo.zip")


def test_redact_repo_url() -> None:
    redacted = redact_repo_url("https://tok@host/a/b.git")
    assert "***REDACTED***" in redacted
    assert "tok" not in redacted

    plain = "https://host/a/b.git"
    assert redact_repo_url(plain) == plain


def test_clone_or_update_repo_clones_then_updates_idempotently(tmp_dir: Path) -> None:
    # Use a file:// URL (not a bare filesystem path) so this exercises the
    # exact same is_git_url()/resolve_auth() code paths Mode C uses in
    # production, without needing live credentials — resolve_auth() treats
    # file:// as always-authorized (see git_repo.py's module docstring).
    test_dir = tmp_dir / "clone_update"
    test_dir.mkdir()
    bare = _make_bare_repo_with_job(test_dir)
    repo_url = f"file://{bare}"
    local_path = test_dir / "clone_target"

    clone_or_update_repo(repo_url, "main", local_path)
    assert (local_path / "process" / "TestJob_0.1.item").is_file()
    first_sha = get_commit_sha(local_path)

    # Push a second commit to the bare repo from a second worktree, then
    # re-run clone_or_update_repo against the same local_path.
    work2 = test_dir / "fixture_work2"
    subprocess.run(["git", "clone", str(bare), str(work2)], check=True)
    (work2 / "process" / "SecondJob_0.1.item").write_text(MINIMAL_ITEM_XML)
    subprocess.run(["git", "-C", str(work2), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(work2), "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "second"],
        check=True,
    )
    subprocess.run(["git", "-C", str(work2), "push", "origin", "main"], check=True)

    clone_or_update_repo(repo_url, "main", local_path)
    second_sha = get_commit_sha(local_path)
    assert second_sha != first_sha
    assert (local_path / "process" / "SecondJob_0.1.item").is_file()


def test_get_commit_sha_matches_git_rev_parse(tmp_dir: Path) -> None:
    test_dir = tmp_dir / "sha_check"
    test_dir.mkdir()
    bare = _make_bare_repo_with_job(test_dir)
    repo_url = f"file://{bare}"
    local_path = test_dir / "sha_check_target"
    clone_or_update_repo(repo_url, "main", local_path)

    expected = subprocess.run(
        ["git", "-C", str(local_path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert get_commit_sha(local_path) == expected


def test_resolve_auth_raises_without_credentials(tmp_dir: Path) -> None:
    # Namespace the env var names under this run's own tempdir name so they
    # cannot collide with anything real in the environment.
    prefix = f"TESTMODEC_{tmp_dir.name}"
    token_env_var = f"{prefix}_TOKEN_DOES_NOT_EXIST"
    ssh_key_env_var = f"{prefix}_SSH_KEY_DOES_NOT_EXIST"
    assert token_env_var not in os.environ
    assert ssh_key_env_var not in os.environ

    try:
        resolve_auth("https://example.invalid/org/repo.git", token_env_var, ssh_key_env_var)
        raise AssertionError("expected GitAccessError")
    except GitAccessError:
        pass


def test_end_to_end_git_mode(tmp_dir: Path) -> None:
    test_dir = tmp_dir / "e2e"
    test_dir.mkdir()
    bare = _make_bare_repo_with_job(test_dir)
    repo_url = f"file://{bare}"
    working_dir = test_dir / "working"
    report_path = test_dir / "extraction-report.json"
    metadata_path = test_dir / "talend_metadata.json"

    result = subprocess.run(
        [
            sys.executable,
            str(TALEND_EXTRACTOR_PATH),
            repo_url,
            "--branch",
            "main",
            "--working-dir",
            str(working_dir),
            "--report-output",
            str(report_path),
            "--output",
            str(metadata_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"extractor failed: {result.stderr}"

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["mode"] == "git"
    assert report["branch"] == "main"
    assert report["commit_sha"]
    assert report["archive_name"] is None
    assert report["archive_sha256"] is None
    assert report["repo_url"] == repo_url  # file:// carries no credential to redact
    names_and_status = {j["name"]: j["status"] for j in report["jobs"]}
    assert names_and_status.get("TestJob") == "SUCCESS"


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)
        test_is_git_url()
        test_redact_repo_url()
        test_clone_or_update_repo_clones_then_updates_idempotently(tmp_dir)
        test_get_commit_sha_matches_git_rev_parse(tmp_dir)
        test_resolve_auth_raises_without_credentials(tmp_dir)
        test_end_to_end_git_mode(tmp_dir)
    print("All Mode C checks passed.")


if __name__ == "__main__":
    main()
