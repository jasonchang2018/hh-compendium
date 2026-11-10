#!/usr/bin/env python3
"""
AI-Style Documentation Enrichment
===================================
Takes the same talend_metadata.json / qlik_metadata.json as
generate_documentation.py and produces the deeper analytical documents the
AI_DOCUMENTATION_PROMPT.md template asks for: System Architecture,
Job-by-Job Documentation (grouped/summarized rather than one write-up per
job), Qlik App Documentation, Data Lineage Map, Operational Runbook, and a
Dependency Matrix — all derived deterministically from the metadata (no AI
API calls), so it's safe to re-run after any extraction, on any workspace or
tenant, not just this one.

Everything here is inferred from component/connection *shapes* (naming
conventions, source/transform/target component prefixes, tRunJob chains,
context.* references) — never invented. If the metadata doesn't support a
claim, the generated doc says so.

Usage:
    python enrich_documentation.py \
        --talend talend_metadata.json \
        --qlik qlik_metadata.json \
        --output ./documentation/

Requirements:
    Python 3.8+ (standard library only, except python-dotenv for .env loading)
"""

import argparse
import json
import logging
import os
import re
import sys
from collections import defaultdict
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


# ---------------------------------------------------------------------------
# Component classification (Talend's own naming convention — stable across
# any workspace, not specific to this dataset)
# ---------------------------------------------------------------------------

INPUT_PREFIXES = (
    "tFileInput", "tMysqlInput", "tFixedFlowInput", "tRowGenerator",
    "tFileFetch", "tMysqlRow", "tMSSqlInput", "tDBInput",
    # Talend Component Kit types carry no "t" prefix (e.g. SnowflakeInput)
    "SnowflakeInput",
)
OUTPUT_PREFIXES = (
    "tFileOutput", "tMysqlOutput", "tCreateTable", "tMSSqlOutput", "tDBOutput",
    "SnowflakeOutput",
)
TRANSFORM_TYPES = {
    "tMap", "tFilterRow", "tAggregateRow", "tUniqRow", "tFuzzyMatch",
    "tSortRow", "tJoin", "tIntervalMatch", "tAddCRC", "tMysqlSCD",
    "tELTMysqlInput", "tELTMysqlOutput", "tELTMysqlMap",
}
RISK_TYPES = {"tDie", "tWarn"}
CODE_TYPES = {"tJava", "tJavaRow", "tJavaFlex", "tGroovy", "tGroovyFile"}
LOG_ONLY_TYPES = {"tLogRow", "tMsgBox", "tLogCatcher"}

# Matches component-type names like tMysqlInput/tPostgresqlOutput/tOracleConnection
# and captures the DB family ("Mysql", "Postgresql", "Oracle", ...) generically.
DB_FAMILY_RE = re.compile(r"^t([A-Za-z]+?)(Input|Output|Connection|Row|SCD)$")


def mermaid_id(name: str) -> str:
    """Sanitize a job/component name for safe use as a Mermaid node id."""
    return "n_" + re.sub(r"[^A-Za-z0-9_]", "_", name)


# ---------------------------------------------------------------------------
# Per-job analysis
# ---------------------------------------------------------------------------

def analyze_job(job: dict) -> dict:
    """Classify a job's kind and infer a grounded one-line description."""
    comps = job.get("components", [])
    types = [c["component_type"] for c in comps]
    type_set = set(types)
    name_norm = job["name"].lower()

    deps = []
    for c in comps:
        if c["component_type"] == "tRunJob":
            for p in c.get("parameters", []):
                if p["name"] == "PROCESS" and p.get("value"):
                    deps.append(p["value"])

    risks = []
    if type_set & RISK_TYPES:
        risks.append(f"Uses error-handling/demo components: {sorted(type_set & RISK_TYPES)}")
    if type_set & CODE_TYPES:
        risks.append(
            f"Embeds custom code components ({sorted(type_set & CODE_TYPES)}) "
            "— logic not visible from metadata alone"
        )
    if any(p.get("value") == "***REDACTED***" for c in comps for p in c.get("parameters", [])):
        risks.append(
            "Has a credential-like parameter (redacted in extraction) — "
            "verify the secret is managed properly, not hardcoded in the job"
        )
    if not comps:
        risks.append("No components extracted — job may be empty, broken, or a folder placeholder")

    has_input = any(t.startswith(INPUT_PREFIXES) for t in types)
    has_output = any(t.startswith(OUTPUT_PREFIXES) for t in types)
    is_component_demo = any(name_norm == t.lower() for t in type_set)

    if is_component_demo:
        matched = next(t for t in type_set if name_norm == t.lower())
        kind = "component-demo"
        desc = (
            f"Job whose name and sole component match (`{matched}`) — "
            "characteristic of a Talend Studio tutorial job demonstrating "
            "one component in isolation, not a production data flow."
        )
    elif deps:
        kind = "orchestration"
        desc = f"Orchestration job — invokes child job(s) via tRunJob: {', '.join(sorted(set(deps)))}."
    elif has_input and has_output:
        kind = "etl-pipeline"
        sources = sorted({t for t in types if t.startswith(INPUT_PREFIXES)})
        targets = sorted({t for t in types if t.startswith(OUTPUT_PREFIXES)})
        transforms = sorted(type_set & TRANSFORM_TYPES)
        desc = (
            f"Reads via {sources}"
            + (f", transforms via {transforms}" if transforms else "")
            + f", writes via {targets}."
        )
    elif has_input and not has_output:
        kind = "read-only / preview"
        sources = sorted({t for t in types if t.startswith(INPUT_PREFIXES)})
        if type_set & LOG_ONLY_TYPES:
            desc = (
                f"Reads via {sources} and logs/previews output only (no "
                "persisted target) — likely a debug or demo job, not a "
                "production data flow."
            )
        else:
            desc = f"Reads via {sources}; no output target found in the extracted metadata."
    elif type_set and type_set <= CODE_TYPES:
        kind = "code-only"
        desc = (
            "Runs custom code only (Java/Groovy) — no file/DB source or "
            "target components. Purpose not determinable beyond the "
            "component list; verify with team."
        )
    elif not comps:
        kind = "empty"
        desc = "Unable to determine from metadata — no components extracted for this job."
    else:
        kind = "utility"
        desc = f"Utility/demo job using: {sorted(type_set)}. Not a source-to-target data pipeline."

    return {
        "name": job["name"],
        "project": job.get("project", ""),
        "kind": kind,
        "desc": desc,
        "deps": sorted(set(deps)),
        "risks": risks,
        "component_types": sorted(type_set),
    }


def all_jobs_flat(talend: dict) -> list:
    jobs = []
    for proj in talend.get("projects", []):
        jobs.extend(proj.get("jobs", []))
    return jobs


def find_context_jobs(jobs: list) -> list:
    """Jobs whose component parameters reference context.* variables."""
    found = set()
    for job in jobs:
        for c in job.get("components", []):
            for p in c.get("parameters", []):
                if "context." in (p.get("value") or ""):
                    found.add(job["name"])
                    break
    return sorted(found)


def correlate_db_connections(jobs: list, db_connections: list) -> tuple:
    """Match component-type DB families (regex-derived) against defined
    connections by substring match on connection name/db_type. Generic —
    works for MySQL, Postgres, Oracle, etc., not hardcoded to one DB."""
    family_jobs = defaultdict(set)
    for job in jobs:
        for c in job.get("components", []):
            m = DB_FAMILY_RE.match(c["component_type"])
            if m:
                family_jobs[m.group(1)].add(job["name"])

    matches = []
    matched_families = set()
    for conn in db_connections:
        label = (conn.get("db_type") or "") + " " + conn.get("name", "")
        family = next((f for f in family_jobs if f.lower() in label.lower()), None)
        jobs_for_conn = sorted(family_jobs[family]) if family else []
        if family:
            matched_families.add(family)
        matches.append({"connection": conn["name"], "family": family, "jobs": jobs_for_conn})

    unmatched = {f: sorted(js) for f, js in family_jobs.items() if f not in matched_families}
    return matches, unmatched


def correlate_cloud_tasks(jobs: list, cloud_tasks: list) -> tuple:
    """Match Talend Cloud tasks (from talend_cloud_extractor.py) to Studio
    jobs by artifact/task name (case-insensitive exact match). Returns
    (matched, unmatched_task_names). Matched entries carry the schedule/
    execution data alongside the Studio job name so callers don't need to
    re-look-up the task."""
    job_names = {j["name"].lower(): j["name"] for j in jobs}

    matched = []
    unmatched = []
    for task in cloud_tasks:
        task_name = task.get("name", "")
        candidates = [task.get("artifact_name", ""), task_name]
        job_name = next(
            (job_names[c.lower()] for c in candidates if c and c.lower() in job_names),
            None,
        )
        if job_name:
            matched.append(
                {
                    "job": job_name,
                    "task_name": task_name,
                    "schedule": task.get("schedule"),
                    "recent_executions": task.get("recent_executions", []),
                }
            )
        else:
            unmatched.append(task_name or task.get("artifact_name", "unknown"))

    return matched, unmatched


def summarize_schedule(schedule) -> str:
    """One-line human summary of a Talend Cloud task's schedule/triggers."""
    triggers = schedule.get("triggers", []) if isinstance(schedule, dict) else []
    if not triggers:
        return "No schedule (manual/webhook)"
    parts = []
    for t in triggers:
        ttype = t.get("type", "?")
        expr = t.get("expression", "")
        parts.append(f"{ttype} `{expr}`" if expr else ttype)
    return "; ".join(parts)


def summarize_last_execution(executions: list) -> str:
    """One-line summary of the most recent execution, if any."""
    if not executions:
        return "No recent executions"
    latest = max(executions, key=lambda e: e.get("start_time", ""))
    return f"{latest.get('status', 'unknown')} ({latest.get('start_time', 'unknown')})"


def format_cloud_task_row(match: dict) -> str:
    """Markdown table row for one job -> Talend Cloud task match."""
    return (
        f"| `{match['job']}` | `{match['task_name']}` | "
        f"{summarize_schedule(match['schedule'])} | "
        f"{summarize_last_execution(match['recent_executions'])} |"
    )


# ---------------------------------------------------------------------------
# Demo-workspace heuristic (data-driven — not hardcoded to any one dataset)
# ---------------------------------------------------------------------------

def detect_demo_signals(talend: dict, qlik: dict, analysis: list) -> list:
    """Return a list of grounded evidence strings if this extraction looks
    like a Studio tutorial workspace / empty trial tenant rather than a real
    production platform. Empty list means no such signal was found."""
    evidence = []

    if analysis:
        demo_count = sum(1 for a in analysis if a["kind"] == "component-demo")
        ratio = demo_count / len(analysis)
        if ratio > 0.3:
            evidence.append(
                f"{demo_count}/{len(analysis)} jobs ({ratio:.0%}) are named "
                "identically to the single Talend component they contain — "
                "consistent with Talend Studio's bundled tutorial project"
            )

    if talend:
        db_conns = [c for proj in talend.get("projects", []) for c in proj.get("database_connections", [])]
        if db_conns and all(
            not any(c.get(f) for f in ("db_type", "host", "port", "database", "schema"))
            for c in db_conns
        ):
            evidence.append(
                f"All {len(db_conns)} defined DB connection(s) have empty "
                "host/port/database/schema fields — not configured for real use"
            )

    if qlik is not None and qlik.get("summary", {}).get("total_apps", 0) == 0:
        evidence.append("Qlik Cloud tenant has 0 apps")

    return evidence


def build_caveat(workspace_hint: str, evidence: list) -> str:
    if not evidence:
        return ""
    bullet_list = "; ".join(evidence)
    return (
        f"> **Data-source caveat:** This documentation is generated from "
        f"metadata extracted from `{workspace_hint}`. Signals found in the "
        f"data suggest it may not represent a real production platform: "
        f"{bullet_list}. The documents below describe exactly what is "
        f"present in the extracted metadata; treat any \"production\" "
        f"framing with that in mind and verify with the team before "
        f"relying on it operationally.\n"
    )


# ---------------------------------------------------------------------------
# Document generators
# ---------------------------------------------------------------------------

def generate_architecture_doc(talend: dict, qlik: dict, analysis: list, caveat: str) -> str:
    lines = ["# System Architecture Document", "", caveat, "## What actually exists", ""]
    lines += ["| Layer | Observed state |", "|---|---|"]

    if talend:
        projects = talend.get("projects", [])
        proj_summary = ", ".join(f"`{p['name']}` ({len(p.get('jobs', []))} jobs)" for p in projects)
        lines.append(f"| Talend Studio workspace | {len(projects)} project(s) — {proj_summary} |")
        db_conns = [c for p in projects for c in p.get("database_connections", [])]
        lines.append(f"| Database connections | {len(db_conns)} defined: {', '.join(c['name'] for c in db_conns) or '—'} |")
        ctx_groups = [g for p in projects for g in p.get("context_groups", [])]
        ctx_jobs = find_context_jobs(all_jobs_flat(talend))
        lines.append(
            f"| Context variables | {len(ctx_groups)} group(s): "
            f"{', '.join(g['name'] for g in ctx_groups) or '—'} — used by "
            f"{len(ctx_jobs)}/{len(all_jobs_flat(talend))} jobs |"
        )

    if qlik:
        spaces = qlik.get("spaces", [])
        apps = qlik.get("apps", [])
        conns = qlik.get("data_connections", [])
        lines.append(
            f"| Qlik Cloud tenant | {len(spaces)} space(s), **{len(apps)} app(s)**, "
            f"{len(conns)} data connection(s) |"
        )
    lines.append("")

    if talend:
        by_kind = defaultdict(list)
        for a in analysis:
            by_kind[a["kind"]].append(a)
        lines += ["## Observed data flow (Mermaid)", "", "```mermaid", "graph LR"]
        lines.append("    subgraph TalendStudio[Talend Studio]")
        for kind in ("component-demo", "etl-pipeline", "orchestration", "read-only / preview", "utility", "code-only"):
            if by_kind[kind]:
                lines.append(f"        {mermaid_id(kind)}[\"{len(by_kind[kind])} {kind} job(s)\"]")
        lines.append("    end")
        if qlik:
            apps_n = len(qlik.get("apps", []))
            lines.append(f'    QlikTenant["Qlik Cloud tenant<br/>{len(qlik.get("spaces", []))} spaces, {apps_n} apps"]')
            if apps_n == 0:
                lines.append("    TalendStudio -.->|no configured app/link found| QlikTenant")
            else:
                lines.append("    TalendStudio --> QlikTenant")
        lines.append("```")
        lines.append("")

    lines.append(
        "This diagram reflects only what the extracted metadata shows — "
        "reload schedules, real connection targets, and any app-to-warehouse "
        "linkage must come from re-running the extractors once those are "
        "configured."
    )
    lines.append("")
    return "\n".join(lines)


def generate_job_doc(talend: dict, analysis: list, caveat: str, cloud_matched: list | None = None) -> str:
    jobs = all_jobs_flat(talend)
    lines = ["# Job-by-Job Documentation", "", caveat]
    lines.append(
        f"{len(jobs)} job(s) across {len(talend.get('projects', []))} project(s). "
        "Grouped by inferred kind rather than one write-up per job, so "
        "large sets of near-identical tutorial/demo jobs don't drown out "
        "the jobs that actually move data."
    )
    lines.append("")

    by_kind = defaultdict(list)
    for a in analysis:
        by_kind[a["kind"]].append(a)

    kind_desc = {
        "etl-pipeline": "Has both a source and a target component — the jobs that resemble a real data pipeline",
        "orchestration": "Calls other jobs via tRunJob",
        "read-only / preview": "Reads data but only logs/previews it — no persisted output",
        "utility": "Neither a clear pipeline nor a named component match",
        "component-demo": "Job name matches the one Talend component it exercises",
        "code-only": "Custom Java/Groovy code only, no source/target components",
        "empty": "No components extracted",
    }
    lines += ["## Kind breakdown", "", "| Kind | Count | What it means |", "|---|---|---|"]
    for k in sorted(by_kind, key=lambda k: -len(by_kind[k])):
        lines.append(f"| {k} | {len(by_kind[k])} | {kind_desc.get(k, '')} |")
    lines.append("")

    if by_kind["etl-pipeline"]:
        lines += ["## ETL-pipeline jobs (source→transform→target)", "", "| Job | Project | Description | Risk flags |", "|---|---|---|---|"]
        for a in sorted(by_kind["etl-pipeline"], key=lambda x: x["name"]):
            lines.append(f"| `{a['name']}` | {a['project']} | {a['desc']} | {'; '.join(a['risks']) or '—'} |")
        lines.append("")

    if by_kind["orchestration"]:
        lines += ["## Orchestration jobs (tRunJob chains)", "", "| Job | Calls | Risk flags |", "|---|---|---|"]
        for a in sorted(by_kind["orchestration"], key=lambda x: x["name"]):
            lines.append(f"| `{a['name']}` | {', '.join(a['deps'])} | {'; '.join(a['risks']) or '—'} |")
        lines.append("")

    for kind, title in (("read-only / preview", "Read-only / preview jobs"), ("utility", "Utility jobs"), ("code-only", "Code-only jobs")):
        if by_kind[kind]:
            lines += [f"## {title}", "", "| Job | Description |", "|---|---|"]
            for a in sorted(by_kind[kind], key=lambda x: x["name"]):
                lines.append(f"| `{a['name']}` | {a['desc']} |")
            lines.append("")

    if by_kind["component-demo"]:
        lines += [
            f"## Component-demo jobs ({len(by_kind['component-demo'])})",
            "",
            "Each is a tutorial job whose sole purpose is demonstrating the named component.",
            "",
            "| Job (= component demonstrated) |",
            "|---|",
        ]
        for a in sorted(by_kind["component-demo"], key=lambda x: x["name"]):
            lines.append(f"| `{a['name']}` |")
        lines.append("")

    if cloud_matched:
        lines += [
            "## Talend Cloud schedules",
            "",
            "Jobs matched to a deployed Talend Cloud task by artifact name:",
            "",
            "| Job | Cloud task | Schedule | Last execution |",
            "|---|---|---|---|",
        ]
        for m in sorted(cloud_matched, key=lambda x: x["job"]):
            lines.append(format_cloud_task_row(m))
        lines.append("")

    return "\n".join(lines)


def generate_qlik_app_doc(qlik: dict) -> str:
    apps = qlik.get("apps", [])
    lines = ["# Qlik Cloud App Documentation", ""]
    if not apps:
        lines.append(
            f"**Apps: 0.** Tenant `{qlik.get('tenant', 'unknown')}` has no "
            f"apps as of {qlik.get('extraction_date', 'unknown')}. There is "
            "nothing to document at the app level yet."
        )
    else:
        for app in apps:
            lines.append(f"## {app.get('name', 'Unknown')}")
            lines.append(f"- ID: `{app.get('id', 'N/A')}`")
            lines.append(f"- Last reload: {app.get('last_reload_time', 'N/A')}")
            lines.append(f"- Reload tasks: {len(app.get('reload_tasks', []))}")
            lines.append("")
    lines.append("")

    lines += ["## Spaces", "", "| Space | Type | Description |", "|---|---|---|"]
    for s in qlik.get("spaces", []):
        lines.append(f"| {s['name']} | {s['type']} | {s.get('description') or '—'} |")
    lines.append("")

    conns = qlik.get("data_connections", [])
    lines += ["## Data connections", "", "| Connection | Type | Connect statement | Note |", "|---|---|---|---|"]
    name_counts = defaultdict(int)
    for c in conns:
        name_counts[c["name"]] += 1
    for c in conns:
        note = "⚠ Duplicate name across connections" if name_counts[c["name"]] > 1 else "—"
        lines.append(f"| {c['name']} | {c['type']} | `{c.get('connection_string', '')}` | {note} |")
    lines.append("")
    if any(n > 1 for n in name_counts.values()):
        lines.append(
            "**Flag:** multiple data connections share the same display "
            "name — verify these are intentional per-space defaults and "
            "not leftover duplicates before building on top of them."
        )
        lines.append("")
    return "\n".join(lines)


def generate_lineage_doc(talend: dict, analysis: list, caveat: str) -> str:
    jobs = all_jobs_flat(talend)
    by_name = {j["name"]: j for j in jobs}
    pipeline_jobs = [a for a in analysis if a["kind"] == "etl-pipeline"]

    lines = ["# Data Lineage Map", "", caveat]
    if not pipeline_jobs:
        lines.append("No jobs with both a source and a target component were found — no lineage to map.")
        return "\n".join(lines)

    lines.append(
        f"Intra-job lineage for the {len(pipeline_jobs)} job(s) with a "
        "source→target shape. No cross-job or Talend→Qlik lineage is "
        "derivable from this metadata alone — that requires a real "
        "downstream Qlik app whose load script references these targets."
    )
    lines += ["", "```mermaid", "graph LR"]
    for a in sorted(pipeline_jobs, key=lambda x: x["name"]):
        job = by_name[a["name"]]
        types = [c["component_type"] for c in job.get("components", [])]
        sources = sorted({t for t in types if t.startswith(INPUT_PREFIXES)})
        targets = sorted({t for t in types if t.startswith(OUTPUT_PREFIXES)})
        node = mermaid_id(a["name"])
        for s in sources:
            lines.append(f'    {mermaid_id(s + a["name"])}["{s}"] --> {node}["{a["name"]}"]')
        for t in targets:
            lines.append(f'    {node} --> {mermaid_id(t + a["name"])}["{t}"]')
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def generate_runbook_doc(
    talend: dict, qlik: dict, analysis: list, caveat: str, has_cloud_data: bool = False
) -> str:
    lines = ["# Operational Runbook", "", caveat]
    if has_cloud_data:
        lines.append(
            "## Scope limitation\n\n"
            "Talend Studio job *definitions* and Qlik reload tasks are read "
            "directly; Talend Cloud task schedules/executions come from a "
            "separate `talend_cloud_extractor.py` run, matched to Studio "
            "jobs by artifact name (see 02_job_documentation.md and "
            "06_dependency_matrix.md). This section covers what "
            "monitoring/restart guidance the definitions and cloud "
            "schedule data together imply.\n"
        )
    else:
        lines.append(
            "## Scope limitation\n\n"
            "This extraction contains no scheduling/execution metadata — "
            "`talend_extractor.py` reads job *definitions* only (not Talend "
            "Administration Center execution plans), and Qlik reload tasks are "
            "read directly from the tenant. Run `talend_cloud_extractor.py` and "
            "pass its output via --talend-cloud for schedule/execution info. "
            "This section covers what monitoring/restart guidance the "
            "definitions themselves imply.\n"
        )

    if talend:
        risky = [a for a in analysis if "tDie" in a["component_types"] or "tWarn" in a["component_types"]]
        if risky:
            lines += ["## Jobs with explicit failure/warning logic", "", "| Job | Components | Guidance |", "|---|---|---|"]
            for a in risky:
                flagged = [t for t in a["component_types"] if t in ("tDie", "tWarn")]
                lines.append(f"| `{a['name']}` | {flagged} | Check Talend job execution logs for the triggering condition before retrying |")
            lines.append("")

        orch = [a for a in analysis if a["kind"] == "orchestration"]
        if orch:
            lines += [
                "## Orchestration chains (restart order matters)", "",
                "If a parent job fails, its child job(s) won't run — restart the parent unless the child's inputs are otherwise confirmed satisfied.",
                "", "| Parent job | Child job(s) |", "|---|---|",
            ]
            for a in orch:
                lines.append(f"| `{a['name']}` | {', '.join(a['deps'])} |")
            lines.append("")

        db_conns = [c for p in talend.get("projects", []) for c in p.get("database_connections", [])]
        unconfigured = [c for c in db_conns if not any(c.get(f) for f in ("host", "port", "database"))]
        if unconfigured:
            lines.append(
                "## Database connections needing configuration\n\n"
                + "\n".join(f"- `{c['name']}` — host/port/database blank in the repository entry; configure in Talend Studio before any dependent job can run against real data." for c in unconfigured)
                + "\n"
            )

    if qlik is not None:
        n_apps = len(qlik.get("apps", []))
        n_tasks = qlik.get("summary", {}).get("total_reload_tasks", 0)
        lines.append(
            f"## Qlik Cloud side\n\n{n_apps} app(s), {n_tasks} reload task(s). "
            + ("Nothing to monitor yet." if n_apps == 0 else "See per-app reload schedule in 03_qlik_app_documentation.md.")
            + "\n"
        )

    return "\n".join(lines)


def generate_dependency_matrix_doc(
    talend: dict, cloud_matched: list | None = None, cloud_unmatched: list | None = None
) -> str:
    cloud_matched = cloud_matched or []
    cloud_unmatched = cloud_unmatched or []
    jobs = all_jobs_flat(talend)
    db_conns = [c for p in talend.get("projects", []) for c in p.get("database_connections", [])]
    ctx_groups = [g for p in talend.get("projects", []) for g in p.get("context_groups", [])]

    lines = ["# Dependency Matrix", ""]
    lines.append(
        "## Tooling note\n\n"
        "`talend_extractor.py`'s `JobMetadata.context_groups` field is "
        "defined but never populated by the extractor. Context-variable "
        "usage below is instead inferred by scanning component parameter "
        "values for `context.` references — a reasonable proxy, but it may "
        "miss indirect usage (e.g. variables passed through tRunJob context "
        "propagation).\n"
    )

    if db_conns:
        matches, unmatched = correlate_db_connections(jobs, db_conns)
        lines.append("## Jobs → database connection\n")
        for m in matches:
            if m["family"]:
                lines.append(
                    f"**{len(m['jobs'])} job(s)** likely use `{m['connection']}` "
                    f"(matched component family `{m['family']}`):\n"
                )
                lines += [f"- `{j}`" for j in m["jobs"]]
            else:
                lines.append(f"`{m['connection']}` — no component family in the job set correlates to this connection's name.")
            lines.append("")
        for fam, js in unmatched.items():
            lines.append(f"**{len(js)} job(s)** use `{fam}`-family components with no matching defined connection:\n")
            lines += [f"- `{j}`" for j in js]
            lines.append("")

    if ctx_groups:
        ctx_jobs = find_context_jobs(jobs)
        group_names = ", ".join(g["name"] for g in ctx_groups)
        lines.append(f"## Jobs → context group ({group_names})\n")
        lines.append(f"**{len(ctx_jobs)} job(s)** reference `context.*` in a component parameter:\n")
        lines += [f"- `{j}`" for j in ctx_jobs]
        lines.append("")

    if cloud_matched or cloud_unmatched:
        lines.append("## Job → Talend Cloud task\n")
        if cloud_matched:
            lines += ["| Job | Cloud task | Schedule | Last execution |", "|---|---|---|---|"]
            for m in sorted(cloud_matched, key=lambda x: x["job"]):
                lines.append(format_cloud_task_row(m))
            lines.append("")
        if cloud_unmatched:
            lines.append(f"**{len(cloud_unmatched)} Talend Cloud task(s)** have no matching Studio job name:\n")
            lines += [f"- `{t}`" for t in sorted(cloud_unmatched)]
            lines.append("")

    lines.append("## Job → job (tRunJob orchestration)\n")
    lines.append("```mermaid")
    lines.append("graph TD")
    for job in jobs:
        for c in job.get("components", []):
            if c["component_type"] == "tRunJob":
                for p in c.get("parameters", []):
                    if p["name"] == "PROCESS" and p.get("value"):
                        lines.append(f"    {mermaid_id(job['name'])} --> {mermaid_id(p['value'])}")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate deterministic AI-style enrichment documents "
                     "(architecture, job analysis, lineage, runbook, "
                     "dependency matrix) from extracted metadata",
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
        "--talend-cloud",
        default=os.environ.get("TALEND_CLOUD_METADATA_PATH"),
        help="Path to talend_cloud_metadata.json (from talend_cloud_extractor.py, "
             "or set TALEND_CLOUD_METADATA_PATH env var). Optional — tasks are "
             "linked to Studio jobs by artifact name; if linking fails for any "
             "reason, a warning is logged and the rest of the documents are "
             "still generated.",
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

    analysis = [analyze_job(j) for j in all_jobs_flat(talend)] if talend else []
    if talend:
        workspace_hint = talend.get("workspace_path", "unknown")
    elif qlik:
        workspace_hint = qlik.get("tenant", "unknown")
    else:
        workspace_hint = "unknown"
    evidence = detect_demo_signals(talend, qlik, analysis)
    caveat = build_caveat(workspace_hint, evidence)

    cloud_matched, cloud_unmatched = [], []
    if args.talend_cloud:
        try:
            talend_cloud = load_json(args.talend_cloud)
            cloud_tasks = talend_cloud.get("tasks", []) if talend_cloud else []
            if talend:
                cloud_matched, cloud_unmatched = correlate_cloud_tasks(all_jobs_flat(talend), cloud_tasks)
            else:
                logger.warning(
                    "--talend-cloud provided but no --talend metadata to link "
                    "against — skipping linking"
                )
        except Exception as e:  # noqa: BLE001 -- a bad/malformed cloud file must not abort the run
            logger.warning(f"Talend Cloud task linking failed: {e} — continuing without it")
            cloud_matched, cloud_unmatched = [], []

    files_written = []

    def write(name, content):
        path = output_dir / name
        path.write_text(content, encoding="utf-8")
        files_written.append(str(path))

    write("01_system_architecture.md", generate_architecture_doc(talend, qlik, analysis, caveat))
    if talend:
        write("02_job_documentation.md", generate_job_doc(talend, analysis, caveat, cloud_matched))
    if qlik:
        write("03_qlik_app_documentation.md", generate_qlik_app_doc(qlik))
    if talend:
        write("04_data_lineage_map.md", generate_lineage_doc(talend, analysis, caveat))
    has_cloud_data = bool(cloud_matched or cloud_unmatched)
    write("05_operational_runbook.md", generate_runbook_doc(talend, qlik, analysis, caveat, has_cloud_data))
    if talend:
        write("06_dependency_matrix.md", generate_dependency_matrix_doc(talend, cloud_matched, cloud_unmatched))

    logger.info(f"Enrichment documents generated: {len(files_written)} files in {output_dir}/")
    for f in files_written:
        logger.info(f"  {f}")


if __name__ == "__main__":
    main()
