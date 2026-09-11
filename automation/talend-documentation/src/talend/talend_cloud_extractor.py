#!/usr/bin/env python3
"""
Talend Cloud Management Console Metadata Extractor
====================================================
Connects to the Talend Cloud Management Console (TMC) REST API and extracts
task definitions, schedules/triggers, and recent execution history — read
only, no production data, no job/task mutation.

Output is designed to be fed to an AI (Claude, etc.) for documentation
generation, alongside talend_metadata.json and qlik_metadata.json.

Usage:
    python talend_cloud_extractor.py \
        --base-url https://api.eu.cloud.talend.com \
        --access-token YOUR_TOKEN \
        --output ./talend_cloud_metadata.json

Requirements:
    Python 3.8+
    pip install requests   (only external dependency)

Access Token Setup:
    Talend Cloud portal -> your username (top-right) -> Profile preferences ->
    Personal access tokens -> Add token. Pass it via --access-token or set
    env var TALEND_STUDIO_ACCESS_TOKEN.
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library is required. Install with:")
    print("  pip install requests")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------

# Task parameter names that may carry credentials (passed to the underlying
# Studio job as context variables). Name-based only — values are never
# inspected. Duplicated independently from talend_extractor.py's and
# qlik_cloud_extractor.py's own sensitive-name sets, by design (see CLAUDE.md).
SENSITIVE_TASK_PARAM_NAMES = {
    "password",
    "pass",
    "pwd",
    "secret",
    "token",
    "apikey",
    "api_key",
    "access_token",
    "refresh_token",
    "private_key",
    "client_secret",
    "auth",
    "credential",
}


def sanitize_task_parameters(parameters: dict) -> dict:
    """Redact any task parameter whose name matches a known credential keyword."""
    safe = {}
    for key, value in parameters.items():
        lower_key = key.lower()
        if any(s in lower_key for s in SENSITIVE_TASK_PARAM_NAMES):
            safe[key] = "***REDACTED***"
        else:
            safe[key] = value
    return safe


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------


class TalendCloudClient:
    """Lightweight Talend Cloud Management Console REST API client."""

    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _get(
        self,
        path: str,
        params: dict | None = None,
        tolerate_404: bool = False,
    ) -> Any:
        """Make a GET request with retry logic.

        When tolerate_404 is True, a 404 response returns None instead of
        being treated as an error — used for per-task sub-resources
        (schedule/executions) that legitimately don't exist for every task.
        """
        url = urljoin(self.base_url, path.lstrip("/"))
        retries = 3
        for attempt in range(retries):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                if resp.status_code in (401, 403):
                    logger.error(
                        f"Authentication failed ({resp.status_code}) calling {url}. "
                        "Check --access-token / TALEND_STUDIO_ACCESS_TOKEN and its permissions."
                    )
                    sys.exit(1)
                if resp.status_code == 404 and tolerate_404:
                    return None
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 5))
                    logger.warning(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    logger.warning(
                        f"Request failed after {retries} attempts: {url} — {e}"
                    )
                    return None
                time.sleep(2**attempt)
        return None

    # --- Workspaces ---

    def list_workspaces(self) -> list[dict]:
        """List all workspaces visible to the access token."""
        data = self._get("/orchestration/workspaces")
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        return []

    # --- Tasks ---

    def list_tasks(self, workspace_id: str) -> list[dict]:
        """List tasks in a workspace."""
        data = self._get(
            "/processing/executables/tasks", params={"workspaceId": workspace_id}
        )
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        return []

    def get_task(self, task_id: str) -> dict | None:
        """Get full task detail: name, workspace, artifact, parameters, version."""
        return self._get(f"/processing/executables/tasks/{task_id}", tolerate_404=True)

    def get_task_schedule(self, task_id: str) -> dict | None:
        """Get a task's schedule/triggers. None if the task has no schedule."""
        return self._get(
            f"/processing/executables/tasks/{task_id}/schedule", tolerate_404=True
        )

    def get_task_executions(self, task_id: str, last_days: int) -> list[dict]:
        """Get recent execution history for a task."""
        data = self._get(
            f"/processing/executables/tasks/{task_id}/executions",
            params={"lastDays": last_days},
            tolerate_404=True,
        )
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        return []


# ---------------------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------------------


def extract_task(client: TalendCloudClient, task_id: str, execution_days: int) -> dict | None:
    """Extract full metadata for a single Talend Cloud task.

    The task list endpoint only returns an id (`executable`) — name, workspace,
    artifact, and parameters live on the per-task detail endpoint, so this
    fetches that detail first. Returns None if the task detail is gone by the
    time we ask (404) — tolerated, not fatal.
    """
    detail = client.get_task(task_id)
    if detail is None:
        logger.warning(f"Task {task_id} detail unavailable (404) — skipping")
        return None

    name = detail.get("name", "Unknown")
    logger.info(f"  Extracting task: {name} ({task_id})")

    workspace = detail.get("workspace", {}) or {}
    environment = workspace.get("environment", {}) or {}
    artifact = detail.get("artifact", {}) or {}

    schedule = client.get_task_schedule(task_id)
    executions = client.get_task_executions(task_id, execution_days)

    return {
        "id": task_id,
        "name": name,
        "workspace_id": workspace.get("id", ""),
        "environment_id": environment.get("id", ""),
        "artifact_name": artifact.get("name", ""),
        "artifact_version": artifact.get("version", ""),
        "parameters": sanitize_task_parameters(detail.get("parameters", {}) or {}),
        "schedule": schedule,
        "recent_executions": [
            {
                "execution_id": e.get("executionId", ""),
                "status": e.get("executionStatus", e.get("status", "")),
                "start_time": e.get("startTimestamp", ""),
                "finish_time": e.get("finishTimestamp", ""),
            }
            for e in executions
        ],
    }


def extract_all(client: TalendCloudClient, execution_days: int) -> dict:
    """Main extraction: connect to Talend Cloud and pull all task/schedule metadata."""
    metadata = {
        "base_url": client.base_url.rstrip("/"),
        "extraction_date": datetime.now(UTC).isoformat(),
        "workspaces": [],
        "tasks": [],
        "summary": {},
    }

    logger.info("Fetching workspaces...")
    workspaces = client.list_workspaces()
    for ws in workspaces:
        environment = ws.get("environment", {}) or {}
        metadata["workspaces"].append(
            {
                "id": ws.get("id", ""),
                "name": ws.get("name", ""),
                "environment_id": environment.get("id", ""),
            }
        )
    logger.info(f"  Found {len(workspaces)} workspaces")

    for ws in workspaces:
        ws_id = ws.get("id", "")
        task_summaries = client.list_tasks(ws_id)
        logger.info(f"  Found {len(task_summaries)} tasks in workspace {ws.get('name', ws_id)}")
        for task_summary in task_summaries:
            task_id = task_summary.get("executable", task_summary.get("id", ""))
            if not task_id:
                continue
            task_data = extract_task(client, task_id, execution_days)
            if task_data is not None:
                metadata["tasks"].append(task_data)
            time.sleep(0.2)

    metadata["summary"] = {
        "total_workspaces": len(metadata["workspaces"]),
        "total_tasks": len(metadata["tasks"]),
        "total_scheduled_tasks": sum(1 for t in metadata["tasks"] if t["schedule"]),
    }

    return metadata


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Extract Talend Cloud Management Console task/schedule metadata for AI documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python talend_cloud_extractor.py --base-url https://api.eu.cloud.talend.com --access-token abc123
  python talend_cloud_extractor.py --base-url https://api.us.cloud.talend.com --output talend_cloud_meta.json

The output JSON contains ONLY task definitions, schedules/triggers, and
recent execution history — read-only, no job/task mutation. Parameters
matching known credential keywords are automatically redacted.
        """,
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("TALEND_CLOUD_BASE_URL"),
        help="Talend Cloud API base URL (e.g. https://api.eu.cloud.talend.com) "
        "(or set TALEND_CLOUD_BASE_URL env var)",
    )
    parser.add_argument(
        "--access-token",
        default=os.environ.get("TALEND_STUDIO_ACCESS_TOKEN"),
        help="Talend Cloud personal/service access token "
        "(or set TALEND_STUDIO_ACCESS_TOKEN env var)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.environ.get("TALEND_CLOUD_METADATA_PATH", "talend_cloud_metadata.json"),
        help="Output JSON file path (default: talend_cloud_metadata.json, "
        "or set TALEND_CLOUD_METADATA_PATH env var)",
    )
    parser.add_argument(
        "--execution-days",
        type=int,
        default=7,
        help="Days of execution history to fetch per task (default: 7)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output",
    )

    args = parser.parse_args()

    if os.environ.get("TALEND_CLOUD_EXTRACTOR_ENABLED", "false").strip().lower() not in (
        "1",
        "true",
        "yes",
    ):
        logger.info(
            "Talend Cloud extraction is disabled by default. Set "
            "TALEND_CLOUD_EXTRACTOR_ENABLED=true to enable this extractor."
        )
        return

    if not args.base_url:
        logger.error(
            "Base URL required. Pass via --base-url or set TALEND_CLOUD_BASE_URL env var."
        )
        sys.exit(1)

    if not args.access_token:
        logger.error(
            "Access token required. Pass via --access-token or set "
            "TALEND_STUDIO_ACCESS_TOKEN env var.\n"
            "Create one in Talend Cloud: Profile preferences -> Personal access tokens"
        )
        sys.exit(1)

    logger.info(f"Connecting to Talend Cloud: {args.base_url}")
    client = TalendCloudClient(args.base_url, args.access_token)
    metadata = extract_all(client, args.execution_days)

    indent = 2 if args.pretty else None
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=indent, ensure_ascii=False)

    logger.info(f"Metadata written to: {args.output}")
    logger.info(
        f"Summary: {metadata['summary']['total_workspaces']} workspaces, "
        f"{metadata['summary']['total_tasks']} tasks, "
        f"{metadata['summary']['total_scheduled_tasks']} scheduled"
    )


if __name__ == "__main__":
    main()
