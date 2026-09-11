#!/usr/bin/env python3
"""
Qlik Cloud Metadata Extractor
==============================
Connects to Qlik Cloud via the REST API and extracts app metadata,
load scripts, data model structures, measures, dimensions, and connections
— without exposing any production data.

Output is designed to be fed to an AI (Claude, etc.) for documentation generation.

Usage:
    python qlik_cloud_extractor.py \
        --tenant your-tenant.eu.qlikcloud.com \
        --api-key YOUR_API_KEY \
        --output ./qlik_metadata.json

Requirements:
    Python 3.8+
    pip install requests   (only external dependency)

API Key Setup:
    1. Go to Qlik Cloud Management Console → API keys
    2. Create a key with "Admin" or at minimum read access to apps
    3. Pass it via --api-key or set env var QLIK_API_KEY
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from typing import Any
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library is required. Install with:")
    print("  pip install requests")
    sys.exit(1)

from dotenv import load_dotenv

# Load variables from the .env file into the system environment
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------


class QlikCloudClient:
    """Lightweight Qlik Cloud REST API client."""

    def __init__(self, tenant_url: str, api_key: str):
        tenant_url = tenant_url.removeprefix("https://").removeprefix("http://")
        self.base_url = f"https://{tenant_url}"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _get(self, path: str, params: dict | None = None) -> Any:
        """Make a GET request with retry logic."""
        url = urljoin(self.base_url, path)
        retries = 3
        for attempt in range(retries):
            try:
                resp = self.session.get(url, params=params, timeout=30)
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 5))
                    logger.warning(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    logger.error(
                        f"Request failed after {retries} attempts: {url} — {e}"
                    )
                    return None
                time.sleep(2**attempt)
        logger.error(f"Request failed after {retries} attempts (rate limited): {url}")
        return None

    def _get_text(self, path: str) -> str | None:
        """GET request expecting plain text (e.g., load scripts), with retry."""
        url = urljoin(self.base_url, path)
        retries = 3
        for attempt in range(retries):
            try:
                resp = self.session.get(url, timeout=30)
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 5))
                    logger.warning(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                # Script endpoint may return JSON with a "script" field
                try:
                    data = resp.json()
                    if isinstance(data, dict) and "script" in data:
                        return data["script"]
                    return json.dumps(data)
                except json.JSONDecodeError, ValueError:
                    return resp.text
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    logger.error(
                        f"Request failed after {retries} attempts: {url} — {e}"
                    )
                    return None
                time.sleep(2**attempt)
        logger.error(f"Request failed after {retries} attempts (rate limited): {url}")
        return None

    # --- Spaces ---

    def list_spaces(self) -> list[dict]:
        """List all spaces in the tenant."""
        spaces = []
        path, params = "/api/v1/spaces", {"limit": 100}
        while True:
            data = self._get(path, params=params)
            if not data or "data" not in data:
                break
            spaces.extend(data["data"])
            next_link = data.get("links", {}).get("next", {})
            href = next_link.get("href") if isinstance(next_link, dict) else None
            if not href:
                break
            if not href.startswith(("/", "http")):
                logger.warning(
                    f"Unexpected pagination href shape, stopping early: {href!r}"
                )
                break
            # href already contains the next-page query string — request it
            # directly rather than nesting it as a param of the first page.
            path, params = href, None
        return spaces

    # --- Apps ---

    def list_apps(self) -> list[dict]:
        """List all apps (items of type 'app') in the tenant."""
        items = []
        path, params = "/api/v1/items", {"limit": 100, "resourceType": "app"}
        while True:
            data = self._get(path, params=params)
            if not data or "data" not in data:
                break
            items.extend(data["data"])
            next_link = data.get("links", {}).get("next", {})
            href = next_link.get("href") if isinstance(next_link, dict) else None
            if not href:
                break
            if not href.startswith(("/", "http")):
                logger.warning(
                    f"Unexpected pagination href shape, stopping early: {href!r}"
                )
                break
            # href already contains the next-page query string — request it
            # directly rather than nesting it as a param of the first page.
            path, params = href, None
        return items

    def get_app_details(self, app_id: str) -> dict | None:
        """Get detailed metadata for a single app."""
        return self._get(f"/api/v1/apps/{app_id}")

    def get_app_script(self, app_id: str) -> str | None:
        """Get the load script for an app."""
        return self._get_text(f"/api/v1/apps/{app_id}/script")

    def get_app_media(self, app_id: str) -> dict | None:
        """Get media list (thumbnails etc.) for an app — structural only."""
        return self._get(f"/api/v1/apps/{app_id}/media/list")

    # --- Data connections ---

    def list_data_connections(self, space_id: str | None = None) -> list[dict]:
        """List data connections visible to the API key."""
        params = {"limit": 100}
        if space_id:
            params["spaceId"] = space_id
        data = self._get("/api/v1/data-connections", params=params)
        if data and "data" in data:
            return data["data"]
        return []

    # --- Reload tasks (scheduling) ---

    def list_reload_tasks(self, app_id: str | None = None) -> list[dict]:
        """List reload tasks (schedules)."""
        params = {"limit": 100}
        if app_id:
            params["appId"] = app_id
        data = self._get("/api/v1/reload-tasks", params=params)
        if data and "data" in data:
            return data["data"]
        return []


# ---------------------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------------------

# Connection properties that may contain credentials
SENSITIVE_CONN_PROPS = {
    "password",
    "pwd",
    "secret",
    "token",
    "apikey",
    "api_key",
    "access_token",
    "private_key",
    "client_secret",
}


# Inline credential tokens (e.g. "PWD=...;", "UID=...;") that can appear
# embedded inside a connection string value, regardless of the field's name.
_CREDENTIAL_TOKEN_PATTERN = re.compile(
    r"(?i)\b(pwd|password|uid|user\s*id|apikey|api_key|token|secret)\s*=\s*[^;]*"
)


def redact_credential_tokens(value: str) -> str:
    """Redact inline credential tokens from a connection-string-like value."""
    return _CREDENTIAL_TOKEN_PATTERN.sub(
        lambda m: f"{m.group(1)}=***REDACTED***", value
    )


def sanitize_connection(conn: dict) -> dict:
    """Remove credential fields from a data connection."""
    safe = {}
    for key, value in conn.items():
        lower_key = key.lower()
        if any(s in lower_key for s in SENSITIVE_CONN_PROPS):
            safe[key] = "***REDACTED***"
        elif isinstance(value, dict):
            safe[key] = sanitize_connection(value)
        elif isinstance(value, str):
            # Connection strings (e.g. connect statements) can embed
            # credentials inline even when the field name itself is benign.
            safe[key] = redact_credential_tokens(value)
        else:
            safe[key] = value
    return safe


def parse_load_script_sections(script: str) -> list[dict]:
    """
    Break a Qlik load script into named sections (tabs).
    Qlik uses '///$tab <TabName>' markers to delimit sections.
    """
    if not script:
        return [{"name": "Main", "content": script or ""}]

    sections = []
    current_name = "Main"
    current_lines = []

    for line in script.splitlines():
        stripped = line.strip()
        if stripped.startswith("///$tab "):
            if current_lines or current_name != "Main":
                sections.append(
                    {
                        "name": current_name,
                        "content": "\n".join(current_lines),
                    }
                )
            current_name = stripped[len("///$tab ") :].strip()
            current_lines = []
        else:
            current_lines.append(line)

    sections.append(
        {
            "name": current_name,
            "content": "\n".join(current_lines),
        }
    )

    return sections


def extract_tables_from_script(script: str) -> list[dict]:
    """
    Best-effort extraction of table names and their source queries
    from a Qlik load script. Does NOT execute anything.
    """
    tables = []

    # Simpler pattern: look for STORE ... INTO
    store_pattern = re.compile(
        r"STORE\s+\[?(\w+)\]?\s+INTO\s+(.+?)\s*;",
        re.IGNORECASE | re.MULTILINE,
    )

    lines = script.splitlines() if script else []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Check for table label (TableName:)
        match = re.match(r"^\[?(\w[\w\s]*?)\]?\s*:\s*$", line)
        if match:
            table_name = match.group(1).strip()
            # Collect the load statement that follows
            load_lines = []
            i += 1
            while i < len(lines):
                load_lines.append(lines[i])
                if lines[i].rstrip().endswith(";"):
                    break
                i += 1
            tables.append(
                {
                    "name": table_name,
                    "load_statement_preview": "\n".join(
                        load_lines[:20]
                    ),  # first 20 lines
                }
            )
        i += 1

    # Also capture STORE statements
    if script:
        for match in store_pattern.finditer(script):
            tables.append(
                {
                    "name": match.group(1),
                    "store_target": match.group(2).strip(),
                }
            )

    return tables


def extract_app_metadata(client: QlikCloudClient, app_item: dict) -> dict:
    """Extract full metadata for a single Qlik app."""
    app_id = app_item.get("resourceId", app_item.get("id", ""))
    name = app_item.get("name", "Unknown")

    logger.info(f"  Extracting app: {name} ({app_id})")

    app_data = {
        "id": app_id,
        "name": name,
        "description": app_item.get("description", ""),
        "space_id": app_item.get("spaceId", ""),
        "owner_id": app_item.get("ownerId", ""),
        "created_at": app_item.get("createdAt", ""),
        "updated_at": app_item.get("updatedAt", ""),
        "load_script": None,
        "script_sections": [],
        "extracted_tables": [],
        "reload_tasks": [],
    }

    # Get detailed app info
    details = client.get_app_details(app_id)
    if details and "attributes" in details:
        attrs = details["attributes"]
        app_data["description"] = app_data["description"] or attrs.get(
            "description", ""
        )
        app_data["last_reload_time"] = attrs.get("lastReloadTime", "")
        app_data["published"] = attrs.get("published", False)
        app_data["publish_time"] = attrs.get("publishTime", "")

    # Get load script
    script = client.get_app_script(app_id)
    if script:
        app_data["load_script"] = script
        app_data["script_sections"] = parse_load_script_sections(script)
        app_data["extracted_tables"] = extract_tables_from_script(script)

    # Get reload schedules
    tasks = client.list_reload_tasks(app_id)
    for task in tasks:
        app_data["reload_tasks"].append(
            {
                "id": task.get("id"),
                "name": task.get("name", ""),
                "state": task.get("state", ""),
                "schedule": task.get("schedule", {}),
                "last_execution": task.get("lastExecution", {}),
            }
        )

    return app_data


def extract_all(
    tenant_url: str,
    api_key: str,
    app_filter: list[str] | None = None,
) -> dict:
    """Main extraction: connect to Qlik Cloud and pull all metadata."""
    client = QlikCloudClient(tenant_url, api_key)

    from datetime import UTC, datetime

    metadata = {
        "tenant": tenant_url,
        "extraction_date": datetime.now(UTC).isoformat(),
        "spaces": [],
        "apps": [],
        "data_connections": [],
        "summary": {},
    }

    # Spaces
    logger.info("Fetching spaces...")
    spaces = client.list_spaces()
    for space in spaces:
        metadata["spaces"].append(
            {
                "id": space.get("id"),
                "name": space.get("name"),
                "type": space.get("type"),
                "description": space.get("description", ""),
                "owner_id": space.get("ownerId", ""),
            }
        )
    logger.info(f"  Found {len(spaces)} spaces")

    # Apps
    logger.info("Fetching apps...")
    app_items = client.list_apps()
    logger.info(f"  Found {len(app_items)} apps")

    for item in app_items:
        app_name = item.get("name", "")
        # Apply filter if provided
        if app_filter and app_name not in app_filter:
            continue
        app_meta = extract_app_metadata(client, item)
        metadata["apps"].append(app_meta)
        # Avoid rate-limiting
        time.sleep(0.5)

    # Data connections
    logger.info("Fetching data connections...")
    connections = client.list_data_connections()
    for conn in connections:
        metadata["data_connections"].append(
            sanitize_connection(
                {
                    "id": conn.get("id"),
                    "name": conn.get("qName", conn.get("name", "")),
                    "type": conn.get("qType", conn.get("type", "")),
                    "connection_string": conn.get("qConnectStatement", ""),
                    "space_id": conn.get("spaceId", ""),
                    "owner_id": conn.get("ownerId", ""),
                }
            )
        )
    logger.info(f"  Found {len(connections)} data connections")

    metadata["summary"] = {
        "total_spaces": len(metadata["spaces"]),
        "total_apps": len(metadata["apps"]),
        "total_data_connections": len(metadata["data_connections"]),
        "total_reload_tasks": sum(
            len(a.get("reload_tasks", [])) for a in metadata["apps"]
        ),
    }

    return metadata


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Extract Qlik Cloud metadata for AI documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python qlik_cloud_extractor.py --tenant acme.eu.qlikcloud.com --api-key abc123
  python qlik_cloud_extractor.py --tenant acme.us.qlikcloud.com --output qlik_meta.json
  python qlik_cloud_extractor.py --tenant acme.us.qlikcloud.com --apps "Sales,Finance"

The output JSON contains ONLY implementation metadata (load scripts,
app configurations, data model structures, connection targets, and schedules).
No production data is included. Credentials in data connections are
automatically redacted.
        """,
    )
    parser.add_argument(
        "--tenant",
        "-t",
        default=os.environ.get("QLIK_TENANT_URL"),
        help="Qlik Cloud tenant hostname (e.g., acme.eu.qlikcloud.com) "
        "(or set QLIK_TENANT_URL env var)",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        default=os.environ.get("QLIK_API_KEY"),
        help="Qlik Cloud API key (or set QLIK_API_KEY env var)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.environ.get("QLIK_METADATA_PATH", "qlik_metadata.json"),
        help="Output JSON file path (default: qlik_metadata.json, "
        "or set QLIK_METADATA_PATH env var)",
    )
    parser.add_argument(
        "--apps",
        default=None,
        help="Comma-separated list of app names to extract (default: all)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output",
    )

    args = parser.parse_args()

    if os.environ.get("QLIK_EXTRACTOR_ENABLED", "false").strip().lower() not in (
        "1",
        "true",
        "yes",
    ):
        logger.info(
            "Qlik Cloud extraction is disabled by default. Set "
            "QLIK_EXTRACTOR_ENABLED=true to enable this extractor."
        )
        return

    if not args.tenant:
        logger.error(
            "Tenant required. Pass via --tenant or set QLIK_TENANT_URL env var."
        )
        sys.exit(1)

    if not args.api_key:
        logger.error(
            "API key required. Pass via --api-key or set QLIK_API_KEY env var.\n"
            "Create one in Qlik Cloud: Management Console → API keys"
        )
        sys.exit(1)

    app_filter = None
    if args.apps:
        app_filter = [a.strip() for a in args.apps.split(",")]

    logger.info(f"Connecting to Qlik Cloud: {args.tenant}")
    metadata = extract_all(args.tenant, args.api_key, app_filter)

    indent = 2 if args.pretty else None
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=indent, ensure_ascii=False)

    logger.info(f"Metadata written to: {args.output}")
    logger.info(
        f"Summary: {metadata['summary']['total_apps']} apps, "
        f"{metadata['summary']['total_data_connections']} connections, "
        f"{metadata['summary']['total_reload_tasks']} reload tasks"
    )


if __name__ == "__main__":
    main()
