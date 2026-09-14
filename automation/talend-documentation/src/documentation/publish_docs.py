#!/usr/bin/env python3
"""
Publish Generated Documentation to a Docs Git Repo
=====================================================
Optional pipeline stage. Copies the toolkit's generated `documentation/`
folder into a separate "docs repo" (clone/update it, replace its contents
with the current documentation/, commit, and push) — so the human-readable
output can live in its own repo with its own history, separate from this
toolkit's source.

This never touches production data, and it never touches this toolkit's own
git history — it only clones/commits/pushes the *target* docs repo at
`--local-path`.

Usage:
    python publish_docs.py \
        --docs-repo-url https://github.com/org/docs-repo.git \
        --branch main \
        --source-dir documentation

Requirements:
    Python 3.8+ (standard library only, except python-dotenv for .env loading)
"""

import argparse
import json
import logging
import os
import shutil
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from git_repo import GitAccessError, clone_or_update_repo, commit_and_push, run_git

# Load variables from the .env file into the system environment
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def _default_commit_message() -> str:
    """f"docs: update documentation (<today>)", best-effort suffixed with the
    source Talend extraction's commit SHA when the last extraction ran in
    git mode (Mode C) and its report is available. Non-fatal if the report
    is missing, unreadable, or not from a git-mode run."""
    base = f"docs: update documentation ({date.today().isoformat()})"  # noqa: DTZ011 -- calendar date only, no timezone semantics needed
    report_path = Path("full-documentation/output/extraction-report.json")
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("mode") == "git" and report.get("commit_sha"):
            return f"{base} — source commit {report['commit_sha'][:8]}"
    except (OSError, json.JSONDecodeError):
        pass
    return base


def _replace_dest_contents(dest: Path) -> None:
    """Remove everything under `dest` except a `.git` directory, so a stale
    copy of `dest` (left over from a previous publish run of this tool)
    doesn't leave orphaned files behind that no longer exist in
    `source_dir` — full-replace semantics, not a merge.

    Safe for both the empty `--project-subdir` case (dest == local_path,
    where `.git` lives directly under dest and must be preserved) and the
    non-empty case (dest is a subdirectory of local_path; `.git` lives at
    local_path, outside dest, so there is nothing to guard there — this
    function still behaves correctly, it just never encounters a `.git`
    entry to skip).

    No-op if `dest` doesn't exist yet (nothing to remove before copytree
    creates it).
    """
    if not dest.exists():
        return
    for entry in dest.iterdir():
        if entry.name == ".git":
            continue
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry)
        else:
            entry.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish generated documentation to a separate docs git repo"
    )
    parser.add_argument(
        "--docs-repo-url",
        default=os.environ.get("DOCS_REPO_URL"),
        help="Git URL of the docs repo to publish into (env: DOCS_REPO_URL).",
    )
    parser.add_argument(
        "--branch",
        default=os.environ.get("DOCS_REPO_BRANCH"),
        help="Branch to publish to (env: DOCS_REPO_BRANCH). No default — must be explicit.",
    )
    parser.add_argument(
        "--local-path",
        default=os.environ.get("DOCS_REPO_LOCAL_PATH", "full-documentation/docs-repo-working"),
        help="Local working directory for the cloned docs repo (env: DOCS_REPO_LOCAL_PATH).",
    )
    parser.add_argument(
        "--source-dir",
        default=os.environ.get("DOCS_REPO_SOURCE_DIR", "documentation"),
        help="Directory whose contents get published (env: DOCS_REPO_SOURCE_DIR).",
    )
    parser.add_argument(
        "--project-subdir",
        default=os.environ.get("DOCS_REPO_PROJECT_SUBDIR", ""),
        help="Subdirectory within the docs repo to publish into (env: DOCS_REPO_PROJECT_SUBDIR). "
        "Empty publishes at the docs repo root.",
    )
    parser.add_argument(
        "--git-token-env-var",
        default=os.environ.get("DOCS_REPO_GIT_TOKEN_ENV_VAR", "DOCS_REPO_GIT_TOKEN"),
        help="Name of the env var holding an HTTPS token for the docs repo "
        "(env: DOCS_REPO_GIT_TOKEN_ENV_VAR).",
    )
    parser.add_argument(
        "--git-ssh-key-env-var",
        default=os.environ.get("DOCS_REPO_GIT_SSH_KEY_PATH_ENV_VAR", "DOCS_REPO_GIT_SSH_KEY_PATH"),
        help="Name of the env var holding an SSH private key path for the docs repo "
        "(env: DOCS_REPO_GIT_SSH_KEY_PATH_ENV_VAR).",
    )
    parser.add_argument(
        "--commit-message",
        default=os.environ.get("DOCS_REPO_COMMIT_MESSAGE"),
        help="Commit message to use (env: DOCS_REPO_COMMIT_MESSAGE). "
        "Defaults to an auto-generated message.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Copy files and show what would change, but do not commit or push.",
    )
    args = parser.parse_args()

    if not args.docs_repo_url:
        logger.error("--docs-repo-url required (or set DOCS_REPO_URL env var).")
        sys.exit(1)
    if not args.branch:
        logger.error("--branch required (or set DOCS_REPO_BRANCH env var).")
        sys.exit(1)

    source_dir = Path(args.source_dir)
    if not source_dir.is_dir():
        logger.error(f"Source directory not found: {source_dir}")
        sys.exit(1)

    local_path = Path(args.local_path)
    try:
        clone_or_update_repo(
            args.docs_repo_url,
            args.branch,
            local_path,
            token_env_var=args.git_token_env_var,
            ssh_key_env_var=args.git_ssh_key_env_var,
        )
    except GitAccessError as e:
        logger.error(str(e))
        sys.exit(1)

    resolved_local_path = local_path.resolve()
    dest = (local_path / args.project_subdir).resolve() if args.project_subdir else resolved_local_path
    if not dest.is_relative_to(resolved_local_path):
        logger.error(f"--project-subdir must stay inside --local-path: {args.project_subdir}")
        sys.exit(1)
    _replace_dest_contents(dest)
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, dest, dirs_exist_ok=True)

    if args.dry_run:
        status = run_git(["status", "--porcelain"], cwd=local_path)
        print(status or "No changes to publish.")
        return

    message = args.commit_message or _default_commit_message()
    try:
        pushed = commit_and_push(
            local_path,
            message,
            args.branch,
            token_env_var=args.git_token_env_var,
            ssh_key_env_var=args.git_ssh_key_env_var,
        )
    except GitAccessError as e:
        logger.error(str(e))
        sys.exit(1)
    logger.info("Published documentation changes." if pushed else "No documentation changes to publish.")


if __name__ == "__main__":
    main()
