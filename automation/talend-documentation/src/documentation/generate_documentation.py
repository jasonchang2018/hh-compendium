#!/usr/bin/env python3
"""
AI Documentation Generator
===========================
Takes the JSON output from talend_extractor.py and qlik_cloud_extractor.py
and produces structured Markdown documentation ready for AI review and
enrichment, or for direct use as a technical reference.

This script generates documentation WITHOUT calling any AI API — it creates
a structured Markdown skeleton from the metadata. You then feed the output
to Claude (or another LLM) for narrative enrichment, flow diagrams, and
operational guidance.

Usage:
    python generate_documentation.py \
        --talend talend_metadata.json \
        --qlik qlik_metadata.json \
        --output ./documentation/

Requirements:
    Python 3.8+ (standard library only)
"""

import argparse
import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv

# Load variables from the .env file into the system environment
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_json(path: str) -> dict:
    """Load and return a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_filename(name: str) -> str:
    """Sanitize a string for safe use as a filesystem path component."""
    return (
        "".join(c if c.isalnum() or c in "-_ " else "_" for c in name)
        .strip()
        .replace(" ", "_")
    )


# ---------------------------------------------------------------------------
# Documentation generators
# ---------------------------------------------------------------------------


def generate_system_overview(talend: dict, qlik: dict) -> str:
    """Generate the top-level system overview document."""
    lines = [
        "# System Overview",
        "",
        f"*Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M')} UTC*",
        "",
        "## Platform Summary",
        "",
        "| Platform | Component | Count |",
        "|----------|-----------|-------|",
    ]

    if talend:
        ts = talend.get("summary", {})
        lines.append(f"| Talend | Projects | {ts.get('total_projects', 0)} |")
        lines.append(f"| Talend | ETL Jobs | {ts.get('total_jobs', 0)} |")
        lines.append(
            f"| Talend | DB Connections | {ts.get('total_database_connections', 0)} |"
        )
        lines.append(
            f"| Talend | Context Groups | {ts.get('total_context_groups', 0)} |"
        )

    if qlik:
        qs = qlik.get("summary", {})
        lines.append(f"| Qlik Cloud | Apps | {qs.get('total_apps', 0)} |")
        lines.append(
            f"| Qlik Cloud | Data Connections | {qs.get('total_data_connections', 0)} |"
        )
        lines.append(
            f"| Qlik Cloud | Reload Tasks | {qs.get('total_reload_tasks', 0)} |"
        )

    lines.extend(
        [
            "",
            "## Architecture",
            "",
            "```mermaid",
            "flowchart LR",
            '    A["Source Systems<br/>(Databases, Files, APIs)"] --> B["Talend ETL Jobs<br/>(Extract, Transform, Load)"]',
            '    B --> C["Snowflake<br/>(Data Warehouse)"]',
            '    C --> D["Qlik Cloud<br/>(Dashboards, Analytics)"]',
            "```",
            "",
            "## Data Flow Summary",
            "",
            "The system follows a standard ETL → Warehouse → BI pattern:",
            "",
            "1. **Talend** extracts data from source systems, applies transformations,",
            "   and loads results into Snowflake.",
            "2. **Snowflake** serves as the central data warehouse.",
            "3. **Qlik Cloud** connects to Snowflake for analytics and reporting.",
            "",
            "---",
            "",
            "*Feed this document along with the detailed job and app documentation*",
            "*to Claude or another AI for narrative enrichment and flow diagrams.*",
        ]
    )

    return "\n".join(lines)


def generate_talend_job_doc(job: dict) -> str:
    """Generate documentation for a single Talend job."""
    job_name = job.get("name", "Unknown")
    lines = [
        f"# Talend Job: {job_name}",
        "",
    ]

    if job.get("purpose") or job.get("description"):
        lines.append("## Purpose")
        lines.append("")
        lines.append(
            job.get("purpose") or job.get("description", "*(No description set)*")
        )
        lines.append("")

    lines.extend(
        [
            f"- **Project**: {job.get('project', 'N/A')}",
            f"- **Version**: {job.get('version', 'N/A')}",
            f"- **Job Type**: {job.get('job_type', 'Standard')}",
            "",
        ]
    )

    if job.get("author") or job.get("created_date") or job.get("modified_date"):
        if job.get("author"):
            lines.append(f"- **Author**: {job['author']}")
        if job.get("created_date"):
            lines.append(f"- **Created**: {job['created_date']}")
        if job.get("modified_date"):
            lines.append(f"- **Last Modified**: {job['modified_date']}")
        lines.append("")

    # Components
    components = job.get("components", [])
    if components:
        lines.append("## Components")
        lines.append("")
        lines.append("| # | Component | Type | Key Parameters |")
        lines.append("|---|-----------|------|----------------|")

        for i, comp in enumerate(components, 1):
            # Extract key parameters (skip internal/UI params)
            skip_params = {
                "UNIQUE_NAME",
                "LABEL",
                "CONNECTION",
                "ACTIVATE",
                "TSTATCATCHER_STATS",
                "HELP",
                "UPDATE_COMPONENTS",
                "IREPORT_PATH",
                "PROPERTY_TYPE",
                "REPOSITORY_PROPERTY_TYPE",
            }
            key_params = [
                p
                for p in comp.get("parameters", [])
                if p["name"] not in skip_params
                and p.get("value")
                and p["value"] != "***REDACTED***"
                and p.get("field_type") not in ("MEMO", "IMAGE", "TECHNICAL")
            ][
                :5
            ]  # Top 5 params

            param_str = (
                ", ".join(f"`{p['name']}`={p['value'][:50]}" for p in key_params)
                if key_params
                else "—"
            )

            lines.append(
                f"| {i} | {comp.get('unique_name', 'Unknown')} | "
                f"`{comp.get('component_type', 'Unknown')}` | {param_str} |"
            )

        lines.append("")

    # Schema columns
    components_with_schema = [c for c in components if c.get("schema_columns")]
    if components_with_schema:
        lines.append("## Schemas")
        lines.append("")
        for comp in components_with_schema:
            lines.append(f"### {comp.get('unique_name', 'Unknown')}")
            lines.append("")
            lines.append("| Column | Type | Nullable | Length |")
            lines.append("|--------|------|----------|--------|")
            for col in comp["schema_columns"]:
                lines.append(
                    f"| {col['name']} | {col['data_type']} | "
                    f"{'Yes' if col.get('nullable') else 'No'} | "
                    f"{col.get('length') or '—'} |"
                )
            lines.append("")

    # Data flow (connections)
    connections = job.get("connections", [])
    if connections:
        lines.append("## Data Flow")
        lines.append("")
        lines.append("```mermaid")
        lines.append("graph LR")
        seen = set()
        for conn in connections:
            src = conn["source"]
            tgt = conn["target"]
            label = conn.get("connector_name", "")
            edge_key = f"{src}->{tgt}"
            if edge_key not in seen:
                seen.add(edge_key)
                if label:
                    lines.append(f"    {src} -->|{label}| {tgt}")
                else:
                    lines.append(f"    {src} --> {tgt}")
        lines.append("```")
        lines.append("")

    # Context variables used
    return "\n".join(lines)


def generate_talend_connections_doc(project: dict) -> str:
    """Generate documentation for database connections in a project."""
    connections = project.get("database_connections", [])
    if not connections:
        return ""

    lines = [
        f"# Database Connections — {project['name']}",
        "",
        "| Connection Name | DB Type | Host | Port | Database | Schema |",
        "|----------------|---------|------|------|----------|--------|",
    ]

    for conn in connections:
        lines.append(
            f"| {conn.get('name', 'Unknown')} | {conn.get('db_type', '—')} | "
            f"{conn.get('host', '—')} | {conn.get('port', '—')} | "
            f"{conn.get('database', '—')} | {conn.get('schema', '—')} |"
        )

    lines.append("")
    return "\n".join(lines)


def generate_talend_contexts_doc(project: dict) -> str:
    """Generate documentation for context groups."""
    groups = project.get("context_groups", [])
    if not groups:
        return ""

    lines = [
        f"# Context Groups — {project['name']}",
        "",
    ]

    for group in groups:
        lines.append(f"## {group['name']}")
        lines.append("")
        if group.get("variables"):
            lines.append("| Variable | Type | Value | Comment |")
            lines.append("|----------|------|-------|---------|")
            for var in group["variables"]:
                val = var.get("value", "")
                if val == "***REDACTED***":
                    val = "*(redacted)*"
                lines.append(
                    f"| {var.get('name', 'Unknown')} | {var.get('var_type', '—')} | "
                    f"`{val[:60]}` | {var.get('comment', '')} |"
                )
            lines.append("")

    return "\n".join(lines)


def generate_qlik_app_doc(app: dict) -> str:
    """Generate documentation for a single Qlik Cloud app."""
    app_name = app.get("name", "Unknown")
    lines = [
        f"# Qlik App: {app_name}",
        "",
    ]

    if app.get("description"):
        lines.append(f"*{app['description']}*")
        lines.append("")

    lines.extend(
        [
            f"- **App ID**: `{app.get('id', 'N/A')}`",
            f"- **Space ID**: `{app.get('space_id', 'N/A')}`",
            f"- **Last Reload**: {app.get('last_reload_time', 'N/A')}",
            f"- **Published**: {app.get('published', 'N/A')}",
            "",
        ]
    )

    # Reload schedules
    tasks = app.get("reload_tasks", [])
    if tasks:
        lines.append("## Reload Schedule")
        lines.append("")
        for task in tasks:
            sched = task.get("schedule", {})
            lines.append(
                f"- **{task.get('name', 'Unnamed')}**: "
                f"State={task.get('state', '?')}, "
                f"Schedule={json.dumps(sched)}"
            )
        lines.append("")

    # Load script sections
    sections = app.get("script_sections", [])
    if sections:
        lines.append("## Load Script")
        lines.append("")
        for section in sections:
            lines.append(f"### Tab: {section['name']}")
            lines.append("")
            content = section.get("content", "").strip()
            if content:
                lines.append("```qlik")
                lines.append(content)
                lines.append("```")
            else:
                lines.append("*(empty section)*")
            lines.append("")

    # Extracted tables
    tables = app.get("extracted_tables", [])
    if tables:
        lines.append("## Tables Loaded")
        lines.append("")
        lines.append("| Table Name | Source / Notes |")
        lines.append("|------------|---------------|")
        for tbl in tables:
            source = tbl.get("store_target", "")
            if not source:
                preview = tbl.get("load_statement_preview", "")
                # Extract first meaningful line as source hint
                for pline in preview.splitlines():
                    stripped = pline.strip()
                    if stripped and not stripped.startswith("//"):
                        source = stripped[:80]
                        break
            lines.append(f"| {tbl.get('name', 'Unknown')} | `{source}` |")
        lines.append("")

    return "\n".join(lines)


def generate_qlik_connections_doc(qlik: dict) -> str:
    """Generate documentation for Qlik Cloud data connections."""
    connections = qlik.get("data_connections", [])
    if not connections:
        return ""

    lines = [
        "# Qlik Cloud Data Connections",
        "",
        "| Connection Name | Type | Space |",
        "|----------------|------|-------|",
    ]

    for conn in connections:
        lines.append(
            f"| {conn.get('name', '—')} | {conn.get('type', '—')} | "
            f"{conn.get('space_id', '—')} |"
        )

    lines.append("")
    return "\n".join(lines)


def generate_ai_prompt(
    output_dir: Path, talend_path: str | None, qlik_path: str | None
) -> str:
    """Generate a prompt template for feeding the docs to an AI."""
    talend_ref = talend_path or "talend_metadata.json"
    qlik_ref = qlik_path or "qlik_metadata.json"
    json_files_lines = "\n".join(
        line
        for line in [
            f"- @{talend_ref} — Talend ETL job definitions (components, connections, schemas, context variables)"
            if talend_path
            else None,
            f"- @{qlik_ref} — Qlik Cloud app metadata (load scripts, data connections, reload schedules)"
            if qlik_path
            else None,
        ]
        if line
    )
    return f"""# AI Documentation Enrichment Prompt

Use this prompt when feeding the extracted metadata to Claude or another AI.

---

## Prompt Template

```
You are a senior data platform engineer and technical writer, experienced in
Talend ETL and Qlik Cloud BI, who specializes in reverse-engineering
undocumented systems from implementation metadata alone. Write for the
engineers who now own this platform: be precise, avoid speculation presented
as fact, and call out anything that looks risky or undocumented-by-design.

I have extracted metadata from our Qlik + Talend data platform. The original
developer has left and there is no documentation. I need you to generate
comprehensive technical documentation from these metadata files.

The attached JSON files contain:
{json_files_lines}

If you have file-write access in this repository (e.g. you are running as
Claude Code or another CLI coding agent, invoked from the repository root),
write each document directly to the file path given with it below,
overwriting that file's existing content, instead of only printing it in
this conversation. If you do not have file-write access (e.g. a plain
chat/API session with no filesystem), print each document under a heading
matching its file path so a human can save it by hand. File paths below are
relative to `{output_dir}/`.

Please generate:

All six documents below should read as plain-English explainers a
non-Talend/non-Qlik engineer could follow — not just restructured metadata.
Where a section below asks for a table, technical term, or diagram, translate
jargon rather than repeating field names verbatim, and ground every claim in
the attached JSON (never invent a name, date, or setting).

1. **System Architecture Document** — **File:** `01_system_architecture.md`
   - **Overview** — one short paragraph on what the platform does end to end
     (sources → Talend ETL → Snowflake → Qlik Cloud).
   - **Detail table** — project/tenant name, total Talend jobs, total DB
     connections, total Qlik apps (use the extracted summary counts; omit a
     row if the metadata has none).
   - **Data flow** — the overall path from sources through Talend ETL into
     Snowflake and out to Qlik dashboards, as a Mermaid diagram.
   - **Glossary** — a short table translating recurring platform terms
     (e.g. Space, Reload task, Context group) into plain English.

2. **Job-by-Job Documentation** — **Files:** one per Talend job, at
   `talend/<ProjectName>/job_<JobName>.md` (same project and job names as in
   @{talend_ref}). For each job, write a plain-English explainer
   using this structure:
   - **Overview** — one short paragraph on what the job does end to end.
   - **Detail table** — Job name, Version, Project, Author, Created, Last
     Modified (use the extracted values; omit a row if the metadata has none
     — never invent a name or date).
   - **Step-by-step data flow** — each stage in plain English (what it reads,
     what it changes, what it writes), not just a component list.
   - **Settings tables** — for each source/target component, show its
     configuration alongside a "what it means" column in plain English.
   - **Dependencies & configuration** — which other jobs it triggers or
     depends on, and which context variables it relies on and why.
   - **Glossary** — a short table translating the Talend component types used
     in this job (e.g. `tMap`, `tFileInputDelimited`) into plain English.
   - **Issues observed** (only if evident from the provided metadata, e.g.
     an unmapped/disconnected column, a missing schema) — state the specific
     evidence for the concern; do not speculate beyond what the metadata shows.

3. **Qlik App Documentation** — **Files:** one per Qlik app, at
   `qlik/app_<AppName>.md` (same app names as in @{qlik_ref}). For
   each app, write a plain-English explainer using this structure:
   - **Overview** — one short paragraph on what the app is for and who it's
     likely for, based on its name/space.
   - **Detail table** — App name, Space, Published status (use extracted
     values; omit a row if the metadata has none).
   - **Data model** — what data it loads and from where, and the
     tables/relationships, in plain English rather than raw load-script text.
   - **Settings table** — data connections and reload schedule, alongside a
     "what it means" column.
   - **Glossary** — a short table translating Qlik-specific terms used (e.g.
     Load script, Resident table, Reload task) into plain English.
   - **Issues observed** (only if evident from the provided metadata) —
     state the specific evidence; do not speculate beyond it.

4. **Data Lineage Map** — **File:** `04_data_lineage_map.md`
   - **Overview** — one short paragraph on how to read the lineage trace
     that follows.
   - **Trace** — source → Talend job → Snowflake table → Qlik app, as a
     Mermaid flowchart, plus a plain-English walkthrough of each hop.
   - **Gaps** — any point in the chain that could not be determined from the
     metadata, stated explicitly as unknown rather than inferred.

5. **Operational Runbook** — **File:** `05_operational_runbook.md`
   - **Overview** — one short paragraph on what this runbook covers.
   - **How-to sections** — numbered, plain-English steps for: monitoring job
     / reload status, restarting a failed job, and troubleshooting the most
     likely failure modes evident from the metadata (e.g. missing schema,
     hardcoded connection values).
   - **Glossary** — a short table translating any ops-specific terms used
     that weren't already covered in the Job or Qlik App glossaries.

6. **Dependency Matrix** — **File:** `06_dependency_matrix.md`
   - **Overview** — one short paragraph on what the matrix shows and how to
     read it.
   - **Matrix table** — which jobs depend on which connections and context
     groups.
   - **Notes** — plain-English callouts for anything in the matrix that
     looks risky (e.g. many jobs sharing one connection, a job with no
     visible dependencies that seems like it should have some).

IMPORTANT:
- Do NOT invent information. If something cannot be determined from the
  metadata, say "Unable to determine from metadata — verify with team."
- Flag any components or patterns that look unusual or risky.
- Identify any hardcoded values that should be parameterized.
```

---

If you're already running as Claude Code (or another CLI coding agent) in
this repository, just run the prompt above directly — it will write the six
documents straight into `{output_dir}/`. Otherwise, copy the prompt above,
attach the JSON files, send it to Claude, and save each document it prints
into the matching file path under `{output_dir}/` by hand.
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate structured documentation from extracted metadata",
    )
    parser.add_argument(
        "--talend",
        default=os.environ.get("TALEND_METADATA_PATH"),
        help="Path to talend_metadata.json (from talend_extractor.py, "
        "or set TALEND_METADATA_PATH env var)",
    )
    parser.add_argument(
        "--qlik",
        default=os.environ.get("QLIK_METADATA_PATH"),
        help="Path to qlik_metadata.json (from qlik_cloud_extractor.py, "
        "or set QLIK_METADATA_PATH env var)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.environ.get("OUTPUT_DOCUMENTATION_PATH", "./documentation"),
        help="Output directory for Markdown files (default: ./documentation/, "
        "or set OUTPUT_DOCUMENTATION_PATH env var)",
    )

    args = parser.parse_args()

    if not args.talend and not args.qlik:
        logger.error("Provide at least one of --talend or --qlik")
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    talend = load_json(args.talend) if args.talend else None
    qlik = None
    if args.qlik:
        try:
            qlik = load_json(args.qlik)
        except Exception as e:  # noqa: BLE001 -- a missing/malformed Qlik file must not abort the run
            logger.warning(f"Could not load --qlik metadata ({e}) — continuing with Talend only")

    files_written = []

    # System overview
    overview = generate_system_overview(talend, qlik)
    path = output_dir / "00_system_overview.md"
    path.write_text(overview, encoding="utf-8")
    files_written.append(str(path))

    # Talend documentation
    if talend:
        for project in talend.get("projects", []):
            proj_dir = output_dir / "talend" / project["name"]
            proj_dir.mkdir(parents=True, exist_ok=True)

            # Per-job documentation
            for job in project.get("jobs", []):
                doc = generate_talend_job_doc(job)
                job_name = safe_filename(job.get("name", "Unknown"))
                job_path = proj_dir / f"job_{job_name}.md"
                job_path.write_text(doc, encoding="utf-8")
                files_written.append(str(job_path))

            # Database connections
            conn_doc = generate_talend_connections_doc(project)
            if conn_doc:
                conn_path = proj_dir / "database_connections.md"
                conn_path.write_text(conn_doc, encoding="utf-8")
                files_written.append(str(conn_path))

            # Context groups
            ctx_doc = generate_talend_contexts_doc(project)
            if ctx_doc:
                ctx_path = proj_dir / "context_groups.md"
                ctx_path.write_text(ctx_doc, encoding="utf-8")
                files_written.append(str(ctx_path))

    # Qlik documentation
    if qlik:
        qlik_dir = output_dir / "qlik"
        qlik_dir.mkdir(parents=True, exist_ok=True)

        for app in qlik.get("apps", []):
            doc = generate_qlik_app_doc(app)
            safe_name = safe_filename(app.get("name", "Unknown"))
            app_path = qlik_dir / f"app_{safe_name}.md"
            app_path.write_text(doc, encoding="utf-8")
            files_written.append(str(app_path))

        conn_doc = generate_qlik_connections_doc(qlik)
        if conn_doc:
            conn_path = qlik_dir / "data_connections.md"
            conn_path.write_text(conn_doc, encoding="utf-8")
            files_written.append(str(conn_path))

    # AI prompt template
    prompt = generate_ai_prompt(output_dir, args.talend, args.qlik)
    prompt_path = output_dir / "AI_DOCUMENTATION_PROMPT.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    files_written.append(str(prompt_path))

    logger.info(f"Documentation generated: {len(files_written)} files in {output_dir}/")
    for f in files_written:
        logger.info(f"  {f}")


if __name__ == "__main__":
    main()
