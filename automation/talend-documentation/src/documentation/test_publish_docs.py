"""Self-check for publish_docs.py. Run directly: uv run src/documentation/test_publish_docs.py"""

import subprocess
import sys
import tempfile
from pathlib import Path

PUBLISH_DOCS_PATH = Path(__file__).parent / "publish_docs.py"


def _make_bare_docs_repo(tmp_dir: Path) -> Path:
    """A local bare repo with one initial commit (a .gitkeep placeholder, so
    the 'main' branch exists for clone_or_update_repo's --branch main to find),
    usable as a "docs repo" via its filesystem path (file:// scheme) — no
    network needed. Caller must pass a fresh/unique tmp_dir per invocation
    (this always creates "docs.git" / "docs_init_work" under it)."""
    bare = tmp_dir / "docs.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(bare)], check=True)
    work = tmp_dir / "docs_init_work"
    subprocess.run(["git", "clone", str(bare), str(work)], check=True)
    (work / ".gitkeep").write_text("")
    subprocess.run(["git", "-C", str(work), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(work), "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "init"],
        check=True,
    )
    subprocess.run(["git", "-C", str(work), "push", "origin", "main"], check=True)
    return bare


def _commit_count(bare: Path) -> int:
    out = subprocess.run(
        ["git", "-C", str(bare), "rev-list", "--count", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return int(out)


def _run_publish_docs(repo_url: str, branch: str, local_path: Path, source_dir: Path, *, dry_run: bool = False):
    args = [
        sys.executable,
        str(PUBLISH_DOCS_PATH),
        "--docs-repo-url",
        repo_url,
        "--branch",
        branch,
        "--local-path",
        str(local_path),
        "--source-dir",
        str(source_dir),
    ]
    if dry_run:
        args.append("--dry-run")
    return subprocess.run(args, capture_output=True, text=True, check=False)


def test_publish_creates_commit_then_is_idempotent(tmp_dir: Path) -> None:
    test_dir = tmp_dir / "basic"
    test_dir.mkdir()
    bare = _make_bare_docs_repo(test_dir)
    repo_url = f"file://{bare}"

    source_dir = test_dir / "documentation"
    source_dir.mkdir()
    (source_dir / "00_overview.md").write_text("# Overview\n")

    local_path = test_dir / "docs-working"

    baseline = _commit_count(bare)  # 1 (the "init" commit)

    result = _run_publish_docs(repo_url, "main", local_path, source_dir)
    assert result.returncode == 0, result.stderr
    after_first = _commit_count(bare)
    assert after_first == baseline + 1

    content = subprocess.run(
        ["git", "-C", str(bare), "show", "HEAD:00_overview.md"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert content == "# Overview\n"

    # Rerun the exact same command unchanged — must be a no-op, no new commit.
    result2 = _run_publish_docs(repo_url, "main", local_path, source_dir)
    assert result2.returncode == 0, result2.stderr
    after_rerun = _commit_count(bare)
    assert after_rerun == after_first


def test_stale_file_removed_on_republish(tmp_dir: Path) -> None:
    test_dir = tmp_dir / "stale"
    test_dir.mkdir()
    bare = _make_bare_docs_repo(test_dir)
    repo_url = f"file://{bare}"

    source_dir = test_dir / "documentation"
    source_dir.mkdir()
    (source_dir / "a.md").write_text("# A\n")
    (source_dir / "b.md").write_text("# B\n")

    local_path = test_dir / "docs-working"

    baseline = _commit_count(bare)  # 1 (the "init" commit)

    result = _run_publish_docs(repo_url, "main", local_path, source_dir)
    assert result.returncode == 0, result.stderr
    after_first = _commit_count(bare)
    assert after_first == baseline + 1

    # Remove one of the two source files, then republish.
    (source_dir / "b.md").unlink()
    result2 = _run_publish_docs(repo_url, "main", local_path, source_dir)
    assert result2.returncode == 0, result2.stderr
    after_second = _commit_count(bare)
    assert after_second == after_first + 1  # a real change landed a new commit

    # The surviving file is present with its original content...
    a_content = subprocess.run(
        ["git", "-C", str(bare), "show", "HEAD:a.md"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert a_content == "# A\n"

    # ...but the removed file is gone from the latest commit.
    b_show = subprocess.run(
        ["git", "-C", str(bare), "cat-file", "-e", "HEAD:b.md"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert b_show.returncode != 0

    # .git history (all commits) remains intact — nothing was rewritten.
    assert _commit_count(bare) == baseline + 2


def test_dry_run_never_touches_history(tmp_dir: Path) -> None:
    test_dir = tmp_dir / "dryrun"
    test_dir.mkdir()
    bare = _make_bare_docs_repo(test_dir)
    repo_url = f"file://{bare}"

    source_dir = test_dir / "documentation"
    source_dir.mkdir()
    (source_dir / "x.md").write_text("# X\n")

    local_path = test_dir / "docs-working"

    baseline = _commit_count(bare)  # 1 (the "init" commit)

    result = _run_publish_docs(repo_url, "main", local_path, source_dir, dry_run=True)
    assert result.returncode == 0, result.stderr

    # The local working copy was updated (copy always happens)...
    assert (local_path / "x.md").is_file()
    # ...but nothing was committed or pushed to the remote.
    assert _commit_count(bare) == baseline


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)
        test_publish_creates_commit_then_is_idempotent(tmp_dir)
        test_stale_file_removed_on_republish(tmp_dir)
        test_dry_run_never_touches_history(tmp_dir)
    print("All publish_docs checks passed.")


if __name__ == "__main__":
    main()
