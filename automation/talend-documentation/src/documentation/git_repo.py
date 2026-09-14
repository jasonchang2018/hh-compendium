"""Git repo cloning + publishing for the docs-publish stage.

Deliberately duplicated (not shared) with src/talend/git_repo.py — see
CLAUDE.md's "no shared library code between scripts" note for why.

`file://` URLs are recognized and require no credential (see `resolve_auth`)
purely to let local/offline self-check tests point at a local bare git repo
as a fake "remote" without needing live credentials. Production usage here
is expected to be `https://` (token auth) or `ssh://`/scp-style (SSH key
auth) — `file://` is not a supported production transport.

Unlike the Talend twin (which only ever clones/fetches for job extraction
input), this module also supports pushing: `commit_and_push` stages,
commits, and pushes the toolkit's generated documentation/ folder to a
separate publishing repo (used by publish_docs.py). It resolves auth for
the push independently of `clone_or_update_repo` (reading the current
`origin` URL fresh via `git remote get-url origin`, since any token
injected earlier is scrubbed back out of `.git/config` right after
clone/fetch), but reuses the exact same token-injection/scrub-around-the-
call structure. Its git-invocation helper is named `run_git` (no leading
underscore, unlike the Talend twin's `_run_git`) because publish_docs.py
calls it directly for a `--dry-run` status preview.
"""
from __future__ import annotations

import logging
import os
import re
import shlex
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

_GIT_URL_RE = re.compile(
    r"^(https?://|ssh://|git://|file://)"      # scheme-form (incl. local file:// for tests)
    r"|^[\w.\-]+@[\w.\-]+:[\w./\-]+(\.git)?$"  # scp-style git@host:org/repo(.git)
)


class GitAccessError(Exception):
    """Raised for any git-plumbing failure (auth, clone, fetch, commit, push)."""


def is_git_url(value: str) -> bool:
    """True if `value` looks like a git remote URL rather than a local path."""
    if not value:
        return False
    if value.lower().endswith(".git"):
        return True
    return bool(_GIT_URL_RE.match(value))


def redact_repo_url(url: str) -> str:
    """Mask any embedded userinfo/token in a URL before it's logged or persisted.

    https://TOKEN@host/org/repo.git -> https://***REDACTED***@host/org/repo.git
    URLs with no embedded credential pass through unchanged.
    """
    return re.sub(r"://[^/@\s]+@", "://***REDACTED***@", url)


def run_git(args: list[str], cwd: Path | None = None, env: dict | None = None) -> str:
    """subprocess.run(["git", *args], ...), raising GitAccessError (never
    sys.exit) with a REDACTED command line on failure."""
    full_env = {**os.environ, **env} if env else None
    redacted_args = [redact_repo_url(a) for a in args]
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=full_env,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        # git itself echoes the (possibly credential-bearing) URL back in
        # stderr on many real failure paths (auth failures, "repository not
        # found", connection errors on a token-embedded https URL) — redact
        # stderr too, not just the constructed argv, before it ever reaches
        # an exception message.
        raise GitAccessError(
            f"git {' '.join(redacted_args)} failed (exit {result.returncode}): "
            f"{redact_repo_url(result.stderr.strip())}"
        )
    return result.stdout.strip()


def _inject_https_token(repo_url: str, token: str) -> str:
    """https://host/a/b.git -> https://<token>@host/a/b.git."""
    if not repo_url.startswith("https://"):
        raise GitAccessError(f"Token auth requires an https:// URL, got: {redact_repo_url(repo_url)}")
    return repo_url.replace("https://", f"https://{token}@", 1)


def _is_ssh_form(repo_url: str) -> bool:
    """True for `ssh://...` or scp-style `user@host:path` forms."""
    if repo_url.startswith(("ssh://", "git@")):
        return True
    # scp-style (no scheme at all, but has userinfo before a ':')
    return "://" not in repo_url and "@" in repo_url


def resolve_auth(repo_url: str, token_env_var: str, ssh_key_env_var: str) -> tuple[str, dict | None]:
    """Decide auth method from what's configured in the environment + the URL scheme.

    Returns (auth_url_to_use, subprocess_env_overrides_or_None).
    Raises GitAccessError if neither mechanism is usable, naming both env
    vars checked (never the raw URL).

    `file://` URLs are local/test-only and need no credential — they are
    returned unchanged, before any SSH-key or token env var is checked.
    """
    if repo_url.startswith("file://"):
        return repo_url, None

    ssh_key = os.environ.get(ssh_key_env_var)
    if ssh_key and _is_ssh_form(repo_url):
        return repo_url, {
            "GIT_SSH_COMMAND": f"ssh -i {shlex.quote(ssh_key)} -o StrictHostKeyChecking=accept-new"
        }

    token = os.environ.get(token_env_var)
    if token and repo_url.startswith("https://"):
        return _inject_https_token(repo_url, token), None

    raise GitAccessError(
        f"No usable git auth for this URL. Checked SSH key env var "
        f"'{ssh_key_env_var}' and token env var '{token_env_var}' — "
        "set one of them, matching the URL's scheme."
    )


def _set_origin_url(local_path: Path, url: str) -> None:
    """git remote set-url origin <url>. Raises GitAccessError like any
    other run_git call — used both to (re-)inject a token-bearing URL
    just before a fetch that needs it, and by _scrub_origin_url below."""
    run_git(["remote", "set-url", "origin", url], cwd=local_path)


def _scrub_origin_url(local_path: Path, repo_url: str) -> None:
    """Best-effort: reset the 'origin' remote back to the token-free
    repo_url so no credential-bearing URL is left sitting in plaintext in
    <local_path>/.git/config. Never raises — a failure here must not mask
    a preceding (and more important) git error from the caller; it's
    logged instead."""
    try:
        _set_origin_url(local_path, repo_url)
    except GitAccessError as exc:
        logger.warning(
            "Could not scrub credential from origin remote URL in %s: %s", local_path, exc
        )


def clone_or_update_repo(
    repo_url: str,
    branch: str,
    local_path: Path,
    *,
    token_env_var: str = "DOCS_REPO_GIT_TOKEN",
    ssh_key_env_var: str = "DOCS_REPO_GIT_SSH_KEY_PATH",
) -> Path:
    """Clone repo_url@branch into local_path if absent; otherwise fetch +
    hard-reset to origin/<branch>. Idempotent/rerun-safe, same contract as
    unpack_archive()'s rmtree-then-recreate.

    When token auth is used (auth_url != repo_url), the token-embedded URL
    only ever touches the 'origin' remote transiently — it's scrubbed back
    to the token-free repo_url immediately after each clone/fetch (even if
    that git call itself failed) so no credential is left in
    <local_path>/.git/config once this function returns. SSH-form auth
    never embeds a credential in the URL (it's carried via
    GIT_SSH_COMMAND), so no scrubbing is needed for it.
    """
    auth_url, env = resolve_auth(repo_url, token_env_var, ssh_key_env_var)
    token_injected = auth_url != repo_url

    if not local_path.exists():
        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            run_git(
                ["clone", "--branch", branch, "--single-branch", auth_url, str(local_path)],
                env=env,
            )
        finally:
            if token_injected and (local_path / ".git").exists():
                _scrub_origin_url(local_path, repo_url)
    else:
        if token_injected:
            # Re-inject the token into origin's URL for this fetch only —
            # a prior run's finally block already scrubbed it back to
            # repo_url, so origin has no credential to fetch with otherwise.
            _set_origin_url(local_path, auth_url)
        try:
            run_git(["fetch", "origin", branch], cwd=local_path, env=env)
        finally:
            if token_injected:
                _scrub_origin_url(local_path, repo_url)
        run_git(["checkout", branch], cwd=local_path, env=env)
        run_git(["reset", "--hard", f"origin/{branch}"], cwd=local_path, env=env)
    return local_path


def get_commit_sha(local_path: Path) -> str:
    return run_git(["rev-parse", "HEAD"], cwd=local_path)


def commit_and_push(
    local_path: Path,
    message: str,
    branch: str,
    *,
    token_env_var: str = "DOCS_REPO_GIT_TOKEN",
    ssh_key_env_var: str = "DOCS_REPO_GIT_SSH_KEY_PATH",
) -> bool:
    """Stage everything in local_path, commit if there are changes, and
    push to origin/<branch>.

    Returns True if a commit was made and pushed, False if the working
    tree was already clean (nothing to publish — a safe no-op, not an
    error) — in that case auth is never resolved, since there's nothing
    to push.

    Auth for the push is resolved fresh from the current 'origin' URL,
    mirroring clone_or_update_repo's token-injection/scrub structure
    exactly: if HTTPS token auth is used, the token-bearing URL only ever
    touches the 'origin' remote transiently for this push, then is
    scrubbed back to the token-free URL immediately after (even if the
    push itself failed) so no credential is left sitting in
    <local_path>/.git/config once this function returns. SSH-form auth
    never embeds a credential in the URL (it's carried via
    GIT_SSH_COMMAND for just this push's subprocess call), so no
    scrubbing is needed for it.
    """
    run_git(["add", "-A"], cwd=local_path)
    status = run_git(["status", "--porcelain"], cwd=local_path)
    if not status:
        return False
    run_git(["commit", "-m", message], cwd=local_path)

    origin_url = run_git(["remote", "get-url", "origin"], cwd=local_path)
    auth_url, env = resolve_auth(origin_url, token_env_var, ssh_key_env_var)
    token_injected = auth_url != origin_url

    if token_injected:
        _set_origin_url(local_path, auth_url)
    try:
        run_git(["push", "origin", branch], cwd=local_path, env=env)
    finally:
        if token_injected:
            _scrub_origin_url(local_path, origin_url)
    return True
