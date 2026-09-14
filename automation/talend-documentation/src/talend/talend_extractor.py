#!/usr/bin/env python3
"""
Talend Studio Workspace Metadata Extractor
===========================================
Walks a Talend Studio workspace directory and extracts all job metadata
(components, connections, schemas, context variables, DB connections)
into structured JSON — without exposing any production data.

Output is designed to be fed to an AI (Claude, etc.) for documentation generation.

Usage:
    python talend_extractor.py /path/to/talend/workspace --output ./talend_metadata.json

Requirements:
    Python 3.8+ (standard library only — no pip installs needed)
"""

import argparse
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from git_repo import (
    GitAccessError,
    clone_or_update_repo,
    get_commit_sha,
    is_git_url,
    redact_repo_url,
)

# Load variables from the .env file into the system environment
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class ComponentParameter:
    name: str
    value: str
    field_type: str = ""


@dataclass
class SchemaColumn:
    name: str
    data_type: str
    nullable: bool = True
    length: int | None = None
    precision: int | None = None
    comment: str = ""


@dataclass
class Component:
    unique_name: str
    component_type: str
    label: str = ""
    parameters: list = field(default_factory=list)
    schema_columns: list = field(default_factory=list)


@dataclass
class Connection:
    source: str
    target: str
    connector_name: str
    connection_type: str
    label: str = ""
    order: int = 0


@dataclass
class ContextVariable:
    name: str
    value: str
    var_type: str = ""
    comment: str = ""
    prompt: str = ""


@dataclass
class ContextGroup:
    name: str
    variables: list = field(default_factory=list)


@dataclass
class JobMetadata:
    name: str
    purpose: str = ""
    description: str = ""
    version: str = ""
    project: str = ""
    job_type: str = "Standard"
    framework: str = ""
    author: str = ""
    created_date: str = ""
    modified_date: str = ""
    components: list = field(default_factory=list)
    connections: list = field(default_factory=list)
    context_groups: list = field(default_factory=list)
    subjobs: list = field(default_factory=list)
    file_path: str = ""


@dataclass
class DatabaseConnection:
    name: str
    db_type: str = ""
    host: str = ""
    port: str = ""
    database: str = ""
    schema: str = ""
    additional_params: str = ""
    # NOTE: credentials are deliberately excluded


@dataclass
class WorkspaceMetadata:
    workspace_path: str
    projects: list = field(default_factory=list)
    extraction_date: str = ""


# ---------------------------------------------------------------------------
# Sensitive-value filter
# ---------------------------------------------------------------------------

# Parameter names that may contain credentials or sensitive data.
# NOTE: bare "key" is deliberately excluded — Talend ETL parameters commonly
# use it for non-secret settings (dedup key, sort key, primary key), which a
# bare substring match would over-redact. Compound credential-key terms
# (apikey, api_key, private_key) are still matched explicitly below.
SENSITIVE_PARAM_NAMES = {
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
    "jdbc_url",
}


def is_sensitive_param(name: str) -> bool:
    """Check if a parameter name likely holds a credential."""
    lower = name.lower()
    return any(s in lower for s in SENSITIVE_PARAM_NAMES)


def sanitize_value(name: str, value: str) -> str:
    """Replace sensitive values with a placeholder."""
    if is_sensitive_param(name):
        return "***REDACTED***"
    return value


# ---------------------------------------------------------------------------
# XML parsing helpers
# ---------------------------------------------------------------------------


def safe_get(element: ET.Element, attr: str, default: str = "") -> str:
    """Safely get an XML attribute, distinguishing missing from empty."""
    value = element.get(attr)
    return value if value is not None else default


def safe_int(value: str, default: int | None = None) -> int | None:
    """Parse an XML attribute as an int, tolerating non-numeric values."""
    try:
        return int(value) or None
    except TypeError, ValueError:
        return default


def parse_schema_columns(component_elem: ET.Element) -> list[SchemaColumn]:
    """Extract schema/column definitions from a component node."""
    columns = []
    for metadata in component_elem.findall(".//metadata"):
        for column in metadata.findall("column"):
            col = SchemaColumn(
                name=safe_get(column, "name"),
                data_type=safe_get(column, "type", "id_String"),
                nullable=safe_get(column, "nullable", "true").lower() == "true",
                length=safe_int(safe_get(column, "length", "0")),
                precision=safe_int(safe_get(column, "precision", "0")),
                comment=safe_get(column, "comment"),
            )
            columns.append(col)
    return columns


def parse_component(node_elem: ET.Element) -> Component:
    """Parse a <node> element into a Component."""
    unique_name = safe_get(node_elem, "componentName")
    component_type = safe_get(node_elem, "componentName")

    # Try to find the UNIQUE_NAME and LABEL parameters
    u_name = unique_name
    label = ""
    params = []

    for ep in node_elem.findall("elementParameter"):
        p_name = safe_get(ep, "name")
        p_value = safe_get(ep, "value")
        p_field = safe_get(ep, "field")

        if p_name == "UNIQUE_NAME":
            u_name = p_value
        elif p_name == "LABEL":
            label = p_value

        # Capture non-sensitive configuration parameters
        if p_value and p_name not in ("UNIQUE_NAME",):
            params.append(
                ComponentParameter(
                    name=p_name,
                    value=sanitize_value(p_name, p_value),
                    field_type=p_field,
                )
            )

    schema_cols = parse_schema_columns(node_elem)

    return Component(
        unique_name=u_name,
        component_type=component_type,
        label=label,
        parameters=[asdict(p) for p in params],
        schema_columns=[asdict(c) for c in schema_cols],
    )


def parse_connection(conn_elem: ET.Element) -> Connection:
    """Parse a <connection> element."""
    return Connection(
        source=safe_get(conn_elem, "source"),
        target=safe_get(conn_elem, "target"),
        connector_name=safe_get(conn_elem, "connectorName"),
        connection_type=safe_get(conn_elem, "type"),
        label=safe_get(conn_elem, "label"),
        order=safe_int(safe_get(conn_elem, "outputId", "0"), default=0) or 0,
    )


# ---------------------------------------------------------------------------
# Archive handling (Mode B)
# ---------------------------------------------------------------------------


def validate_archive(archive_path: Path) -> None:
    """Validate that archive_path is a readable, uncorrupted zip file. Exits on failure."""
    if not zipfile.is_zipfile(archive_path):
        logger.error(f"Not a valid zip archive: {archive_path}")
        sys.exit(1)
    with zipfile.ZipFile(archive_path) as zf:
        bad_member = zf.testzip()
        if bad_member is not None:
            logger.error(f"Corrupted archive: {archive_path} (bad member: {bad_member})")
            sys.exit(1)


def compute_sha256(path: Path) -> str:
    """Compute the SHA-256 checksum of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unpack_archive(archive_path: Path, working_dir: Path) -> Path:
    """Unpack a validated zip archive into <working_dir>/<archive-stem>/, overwriting any prior extraction."""
    target = working_dir / archive_path.stem
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path) as zf:
        zf.extractall(target)
    return target


def job_name_from_stem(stem: str) -> str:
    """Strip Talend's version suffix from an item filename stem (e.g. 'MyJob_0.1' -> 'MyJob')."""
    return re.sub(r"_\d+\.\d+$", "", stem)


class WarningCollector(logging.Handler):
    """Collects WARNING+ messages logged while parsing a single job, for the extraction report."""

    def __init__(self):
        super().__init__(level=logging.WARNING)
        self.records: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record.getMessage())


# Known top-level project folders this extractor does not walk yet (§4.1).
# Fixed, documented list — not a heuristic scan for "unrecognized" folders.
UNSUPPORTED_ARTIFACT_FOLDERS = {
    "joblets": "joblets/ (joblets not yet extracted)",
    "routes": "routes/ (routes not yet extracted)",
    "code/routines": "code/routines/ (standalone routine .java files not extracted)",
}


def detect_unsupported_artifacts(project_dir: Path) -> list[str]:
    """List known-but-unwalked top-level project folders that are present on disk."""
    found = []
    for rel_path, description in UNSUPPORTED_ARTIFACT_FOLDERS.items():
        if (project_dir / rel_path).is_dir():
            found.append(description)

    metadata_dir = project_dir / "metadata"
    if metadata_dir.is_dir():
        for entry in sorted(metadata_dir.iterdir()):
            if entry.is_dir() and entry.name != "connections":
                found.append(f"metadata/{entry.name}/ (file metadata not yet extracted)")

    return found


# ---------------------------------------------------------------------------
# Job parsing
# ---------------------------------------------------------------------------


def parse_job_item(item_path: Path, project_name: str) -> JobMetadata | None:
    """Parse a Talend .item file and return structured job metadata."""
    try:
        tree = ET.parse(item_path)
        root = tree.getroot()
    except ET.ParseError as e:
        logger.warning(f"Failed to parse XML: {item_path} — {e}")
        return None

    base_name = job_name_from_stem(item_path.stem)

    job = JobMetadata(
        name=base_name,
        project=project_name,
        file_path=str(item_path),
    )

    # Parse components (nodes)
    for node in root.findall(".//node"):
        comp = parse_component(node)
        job.components.append(asdict(comp))

    # Parse connections
    for conn in root.findall(".//connection"):
        parsed = parse_connection(conn)
        job.connections.append(asdict(parsed))

    # Parse subjobs
    for subjob in root.findall(".//subjob"):
        subjob_info = {
            "name": safe_get(subjob, "name", ""),
            "components": [],
        }
        for node in subjob.findall("node"):
            subjob_info["components"].append(safe_get(node, "componentName"))
        if subjob_info["name"] or subjob_info["components"]:
            job.subjobs.append(subjob_info)

    return job


def parse_project_users(project_dir: Path) -> dict[str, str]:
    """Map Talend user xmi:id -> login, read once per project from talend.project."""
    users = {}
    project_file = project_dir / "talend.project"
    if not project_file.is_file():
        return users
    try:
        tree = ET.parse(project_file)
        root = tree.getroot()
    except ET.ParseError:
        return users

    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "User":
            xmi_id = elem.get("{http://www.omg.org/XMI}id", "")
            login = safe_get(elem, "login")
            if xmi_id and login:
                users[xmi_id] = login

    return users


def parse_job_properties(
    props_path: Path, job: JobMetadata, users: dict[str, str] | None = None
) -> None:
    """Enrich a JobMetadata object with data from the .properties file."""
    try:
        tree = ET.parse(props_path)
        root = tree.getroot()
    except ET.ParseError:
        return

    # Properties files use TalendProperties namespace — try with and without.
    # purpose/description/version/jobType live as attributes on the nested
    # <Property> element, not on the root <XMI> element.
    property_elem = None
    for child in root:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag == "Property":
            property_elem = child
            break

    if property_elem is not None:
        job.purpose = safe_get(property_elem, "purpose")
        job.description = safe_get(property_elem, "description")
        job.version = safe_get(property_elem, "version")
        job.job_type = safe_get(property_elem, "jobType", "Standard")

    # Try nested property elements
    for prop in root.iter():
        tag = prop.tag.split("}")[-1] if "}" in prop.tag else prop.tag
        if tag == "purpose" and prop.text:
            job.purpose = prop.text.strip()
        elif tag == "description" and prop.text:
            job.description = prop.text.strip()
        elif tag == "version" and prop.text:
            job.version = prop.text.strip()
        elif tag == "author":
            href = safe_get(prop, "href")
            user_id = href.rsplit("#", 1)[-1] if "#" in href else ""
            job.author = (users or {}).get(user_id, "")
        elif tag == "additionalProperties":
            key = safe_get(prop, "key")
            value = safe_get(prop, "value")
            if key == "created_date":
                job.created_date = value
            elif key == "modified_date":
                job.modified_date = value


def parse_context_group(ctx_path: Path) -> ContextGroup | None:
    """Parse a context group XML file."""
    try:
        tree = ET.parse(ctx_path)
        root = tree.getroot()
    except ET.ParseError:
        return None

    group_name = ctx_path.stem
    group = ContextGroup(name=group_name)

    for param in root.iter():
        tag = param.tag.split("}")[-1] if "}" in param.tag else param.tag
        if tag == "contextParameter" or tag == "listParams":
            var = ContextVariable(
                name=safe_get(param, "name"),
                value=sanitize_value(
                    safe_get(param, "name"),
                    safe_get(param, "value"),
                ),
                var_type=safe_get(param, "type"),
                comment=safe_get(param, "comment"),
                prompt=safe_get(param, "prompt"),
            )
            if var.name:
                group.variables.append(asdict(var))

    return group


def parse_db_connection(conn_path: Path) -> DatabaseConnection | None:
    """Parse a database connection metadata XML file."""
    try:
        tree = ET.parse(conn_path)
        root = tree.getroot()
    except ET.ParseError:
        return None

    conn = DatabaseConnection(
        name=conn_path.stem,
        db_type=safe_get(root, "DatabaseType") or safe_get(root, "dbType", ""),
        host=safe_get(root, "ServerName") or safe_get(root, "server", ""),
        port=safe_get(root, "Port") or safe_get(root, "port", ""),
        database=safe_get(root, "SID") or safe_get(root, "dbName", ""),
        schema=safe_get(root, "Schema") or safe_get(root, "uiSchema", ""),
        additional_params=safe_get(root, "AdditionalParams")
        or safe_get(root, "additionalParams", ""),
    )

    # Also search child elements for connection properties
    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag in ("DatabaseConnection", "connection"):
            conn.db_type = conn.db_type or safe_get(elem, "databaseType", "")
            conn.host = conn.host or safe_get(elem, "serverName", "")
            conn.port = conn.port or safe_get(elem, "port", "")
            conn.database = conn.database or safe_get(elem, "datasourceName", "")
            conn.schema = conn.schema or safe_get(elem, "uiSchema", "")

    return conn


# ---------------------------------------------------------------------------
# Workspace walker
# ---------------------------------------------------------------------------


def find_projects(workspace_path: Path) -> list[str]:
    """Discover Talend projects in the workspace."""
    projects = []
    for entry in sorted(workspace_path.iterdir()):
        # A Talend project typically has a 'process' subdirectory
        if (
            entry.is_dir()
            and not entry.name.startswith(".")
            and ((entry / "process").is_dir() or (entry / "poms").is_dir())
        ):
            projects.append(entry.name)
    if not projects and (workspace_path / "process").is_dir():
        # Maybe the workspace path IS the project
        projects.append(workspace_path.name)
    return projects


def extract_project(workspace_path: Path, project_name: str) -> tuple[dict, list[dict], list[str]]:
    """Extract all metadata for a single Talend project.

    Returns (project_data, job_reports, unsupported_artifacts). job_reports
    and unsupported_artifacts feed the extraction report (not part of
    talend_metadata.json).
    """
    project_dir = workspace_path / project_name
    if not project_dir.is_dir():
        project_dir = workspace_path  # workspace IS the project

    project_data = {
        "name": project_name,
        "jobs": [],
        "context_groups": [],
        "database_connections": [],
    }
    job_reports = []

    # --- Jobs ---
    process_dir = project_dir / "process"
    if process_dir.is_dir():
        users = parse_project_users(project_dir)
        seen_jobs = {}
        for item_file in sorted(process_dir.rglob("*.item")):
            base_name = job_name_from_stem(item_file.stem)
            collector = WarningCollector()
            logger.addHandler(collector)
            duplicate = False
            try:
                job = parse_job_item(item_file, project_name)
                if job is not None:
                    if job.name in seen_jobs:
                        logger.warning(
                            f"  Duplicate job name '{job.name}' at {item_file} "
                            f"(already captured from {seen_jobs[job.name]}) — skipping"
                        )
                        duplicate = True
                    else:
                        seen_jobs[job.name] = item_file
                        props_file = item_file.with_suffix(".properties")
                        if props_file.exists():
                            parse_job_properties(props_file, job, users)
                        project_data["jobs"].append(asdict(job))
            finally:
                logger.removeHandler(collector)

            if job is None:
                job_reports.append(
                    {"name": base_name, "status": "FAILED", "warnings": collector.records}
                )
            elif duplicate:
                job_reports.append(
                    {"name": job.name, "status": "SKIPPED_DUPLICATE", "warnings": collector.records}
                )
            else:
                status = "PARTIAL" if collector.records else "SUCCESS"
                job_reports.append(
                    {"name": job.name, "status": status, "warnings": collector.records}
                )

    # --- Context groups ---
    context_dir = project_dir / "context"
    if context_dir.is_dir():
        for ctx_file in sorted(context_dir.rglob("*.item")):
            group = parse_context_group(ctx_file)
            if group:
                project_data["context_groups"].append(asdict(group))

    # --- Database connections ---
    metadata_dir = project_dir / "metadata" / "connections"
    if not metadata_dir.is_dir():
        metadata_dir = project_dir / "metadata"
    if metadata_dir.is_dir():
        for conn_file in sorted(metadata_dir.rglob("*.item")):
            conn = parse_db_connection(conn_file)
            if conn and conn.name:
                project_data["database_connections"].append(asdict(conn))

    unsupported = detect_unsupported_artifacts(project_dir)

    logger.info(
        f"  Project '{project_name}': "
        f"{len(project_data['jobs'])} jobs, "
        f"{len(project_data['context_groups'])} context groups, "
        f"{len(project_data['database_connections'])} DB connections"
    )

    return project_data, job_reports, unsupported


def extract_workspace(workspace_path: str) -> tuple[dict, list[dict], list[str]]:
    """Main extraction: walk the entire workspace and return (metadata, job_reports, unsupported_artifacts)."""
    ws = Path(workspace_path).resolve()
    if not ws.is_dir():
        logger.error(f"Workspace path does not exist: {ws}")
        sys.exit(1)

    from datetime import UTC, datetime

    metadata = {
        "workspace_path": str(ws),
        "extraction_date": datetime.now(UTC).isoformat(),
        "projects": [],
        "summary": {},
    }

    projects = find_projects(ws)
    if not projects:
        logger.error(
            f"No Talend projects found in {ws}. "
            "Expected subdirectories with a 'process/' folder."
        )
        sys.exit(1)

    logger.info(f"Found {len(projects)} project(s) in workspace: {projects}")

    total_jobs = 0
    total_connections = 0
    total_contexts = 0
    all_job_reports = []
    all_unsupported = []

    for project_name in projects:
        project_data, job_reports, unsupported = extract_project(ws, project_name)
        metadata["projects"].append(project_data)
        total_jobs += len(project_data["jobs"])
        total_connections += len(project_data["database_connections"])
        total_contexts += len(project_data["context_groups"])
        all_job_reports.extend(job_reports)
        all_unsupported.extend(unsupported)

    metadata["summary"] = {
        "total_projects": len(projects),
        "total_jobs": total_jobs,
        "total_database_connections": total_connections,
        "total_context_groups": total_contexts,
    }

    return metadata, all_job_reports, all_unsupported


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Extract Talend Studio workspace metadata for AI documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python talend_extractor.py /path/to/workspace
  python talend_extractor.py /path/to/workspace --output talend_metadata.json
  python talend_extractor.py /path/to/workspace --pretty

The output JSON contains ONLY implementation metadata (job definitions,
component configurations, schemas, and connection targets). No production
data or credentials are included — sensitive parameters are automatically
redacted.
        """,
    )
    parser.add_argument(
        "workspace",
        nargs="?",
        default=os.environ.get("TALEND_STUDIO_WORKSPACE_PATH"),
        help="Path to the Talend Studio workspace directory "
        "(or set TALEND_STUDIO_WORKSPACE_PATH env var)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.environ.get("TALEND_METADATA_PATH", "talend_metadata.json"),
        help="Output JSON file path (default: talend_metadata.json, "
        "or set TALEND_METADATA_PATH env var)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output",
    )
    parser.add_argument(
        "--working-dir",
        default=os.environ.get("TALEND_ARCHIVE_WORKING_DIR", "full-documentation/working"),
        help="Directory to unpack a .zip archive (Mode B) or clone a git repo (Mode C) into "
        "(default: full-documentation/working, or set TALEND_ARCHIVE_WORKING_DIR env var)",
    )
    parser.add_argument(
        "--report-output",
        default=os.environ.get(
            "TALEND_EXTRACTION_REPORT_PATH", "full-documentation/output/extraction-report.json"
        ),
        help="Path to write the extraction report JSON (default: "
        "full-documentation/output/extraction-report.json, or set "
        "TALEND_EXTRACTION_REPORT_PATH env var)",
    )
    parser.add_argument(
        "--branch",
        default=os.environ.get("TALEND_GIT_BRANCH"),
        help="Branch to clone/checkout for a git-repo input (Mode C). "
        "Required when `workspace` is a git URL, or set TALEND_GIT_BRANCH env var.",
    )
    parser.add_argument(
        "--git-token-env-var",
        default=os.environ.get("TALEND_GIT_TOKEN_ENV_VAR", "TALEND_GIT_TOKEN"),
        help="Name of the env var holding an HTTPS auth token for Mode C "
        "(default: TALEND_GIT_TOKEN, or set TALEND_GIT_TOKEN_ENV_VAR env var)",
    )
    parser.add_argument(
        "--git-ssh-key-env-var",
        default=os.environ.get("TALEND_GIT_SSH_KEY_PATH_ENV_VAR", "TALEND_GIT_SSH_KEY_PATH"),
        help="Name of the env var holding an SSH private key path for Mode C "
        "(default: TALEND_GIT_SSH_KEY_PATH, or set TALEND_GIT_SSH_KEY_PATH_ENV_VAR env var)",
    )

    args = parser.parse_args()

    if not args.workspace:
        logger.error(
            "Workspace path required. Pass it as an argument or "
            "set TALEND_STUDIO_WORKSPACE_PATH env var."
        )
        sys.exit(1)

    mode = "workspace"
    archive_name = None
    archive_sha256 = None
    repo_url_redacted = None
    branch = None
    commit_sha = None
    extract_from = args.workspace
    workspace_arg = Path(args.workspace)
    if workspace_arg.is_file() and workspace_arg.suffix.lower() == ".zip":
        mode = "archive"
        logger.info(f"Detected archive input: {workspace_arg}")
        validate_archive(workspace_arg)
        archive_name = workspace_arg.name
        archive_sha256 = compute_sha256(workspace_arg)
        logger.info(f"Archive SHA-256: {archive_sha256}")
        unpacked_dir = unpack_archive(workspace_arg, Path(args.working_dir))
        extract_from = str(unpacked_dir)
    elif not workspace_arg.is_dir() and is_git_url(args.workspace):
        mode = "git"
        if not args.branch:
            logger.error(
                "A git repo input requires --branch (or TALEND_GIT_BRANCH env var)."
            )
            sys.exit(1)
        logger.info(f"Detected git repo input: {redact_repo_url(args.workspace)}")
        repo_slug = args.workspace.rstrip("/").rsplit("/", 1)[-1]
        repo_slug = repo_slug.removesuffix(".git")
        target = Path(args.working_dir) / repo_slug
        try:
            clone_or_update_repo(
                args.workspace,
                args.branch,
                target,
                token_env_var=args.git_token_env_var,
                ssh_key_env_var=args.git_ssh_key_env_var,
            )
            commit_sha = get_commit_sha(target)
        except GitAccessError as e:
            logger.error(str(e))
            sys.exit(1)
        repo_url_redacted = redact_repo_url(args.workspace)
        branch = args.branch
        logger.info(f"Cloned at commit {commit_sha}")
        extract_from = str(target)

    logger.info(f"Extracting metadata from: {extract_from}")
    metadata, job_reports, unsupported_artifacts = extract_workspace(extract_from)

    indent = 2 if args.pretty else None
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=indent, ensure_ascii=False)

    report = {
        "mode": mode,
        "archive_name": archive_name,
        "archive_sha256": archive_sha256,
        "repo_url": repo_url_redacted,
        "branch": branch,
        "commit_sha": commit_sha,
        "extraction_date": metadata["extraction_date"],
        "jobs": job_reports,
        "unsupported_artifacts": unsupported_artifacts,
    }
    report_path = Path(args.report_output)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"Metadata written to: {args.output}")
    logger.info(f"Extraction report written to: {report_path}")
    logger.info(
        f"Summary: {metadata['summary']['total_jobs']} jobs, "
        f"{metadata['summary']['total_database_connections']} DB connections, "
        f"{metadata['summary']['total_context_groups']} context groups"
    )


if __name__ == "__main__":
    main()
