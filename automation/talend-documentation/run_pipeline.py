#!/usr/bin/env python3
"""Run the full extraction -> documentation -> Word export pipeline in one command.

Runs, in order:
  1. talend_extractor.py        (required)
  2. talend_cloud_extractor.py  (optional; no-ops unless TALEND_CLOUD_EXTRACTOR_ENABLED=true)
  3. qlik_cloud_extractor.py    (optional; no-ops unless QLIK_EXTRACTOR_ENABLED=true)
  4. generate_documentation.py  (required)
  5. enrich_documentation.py    (default on; --skip-enrich to disable)
  6. ai_enrich_documentation.py (opt-in; runs only if AI_ENRICHMENT_ENABLED=true, and requires
                                  ANTHROPIC_API_KEY. Otherwise this step is a human/agent step,
                                  not automated -- prints a suggested next step using the prompt
                                  Step 4 generated)
  7. export_docx.py             (default on; --skip-export to disable)
  8. publish_docs.py            (opt-in only; --publish, requires DOCS_REPO_URL/DOCS_REPO_BRANCH)

Every step reuses each script's own env-var configuration (TALEND_STUDIO_WORKSPACE_PATH,
QLIK_API_KEY, TALEND_CLOUD_EXTRACTOR_ENABLED, etc. — see README) unchanged. This script only
wires the shared file-path env vars (TALEND_METADATA_PATH, QLIK_METADATA_PATH,
TALEND_CLOUD_METADATA_PATH, OUTPUT_DOCUMENTATION_PATH) so every stage reads and writes the
same files without repeating paths on each invocation — the same convention each script
already follows on its own.

A metadata file that a disabled or failed optional extractor never produced is simply not
passed to Steps 4/5 (they already treat a missing --qlik/--talend-cloud file as "not
provided" and proceed without it — no misleading "file not found" warning for the default
case of an extractor that was never enabled).

Usage:
    uv run run_pipeline.py [workspace] [--branch BRANCH] [--output-dir DIR]
                            [--working-dir DIR] [--skip-enrich] [--skip-export] [--publish]
"""

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

SRC = Path(__file__).parent / "src"


def run_step(name: str, script: Path, args: list[str], env: dict, *, required: bool) -> bool:
    """Run one pipeline stage as a subprocess.

    Returns True if it succeeded (or was a disabled no-op, which also exits 0).
    On a non-zero exit: aborts the whole pipeline if `required`, otherwise logs a
    warning and lets the pipeline continue.
    """
    logger.info(f"--- {name} ---")
    result = subprocess.run([sys.executable, str(script), *args], env=env, check=False)
    if result.returncode != 0:
        if required:
            logger.error(f"{name} failed (exit {result.returncode}) — aborting pipeline.")
            sys.exit(result.returncode)
        logger.warning(f"{name} failed (exit {result.returncode}) — continuing; this stage is optional.")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run the full Talend/Qlik extraction and documentation pipeline end to end",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run run_pipeline.py /path/to/talend/workspace
  uv run run_pipeline.py https://github.com/your-org/talend-workspace.git --branch main
  uv run run_pipeline.py --skip-enrich --output-dir ./documentation
        """,
    )
    parser.add_argument(
        "workspace",
        nargs="?",
        default=None,
        help="Talend workspace directory, .zip archive, or git repo URL for Step 1 "
        "(default: read from TALEND_STUDIO_WORKSPACE_PATH env var)",
    )
    parser.add_argument("--branch", default=None, help="Branch, when workspace is a git repo URL")
    parser.add_argument(
        "--working-dir",
        default=os.environ.get("PIPELINE_WORKING_DIR", "full-documentation/output"),
        help="Directory for intermediate JSON metadata (default: full-documentation/output, "
        "or set PIPELINE_WORKING_DIR env var)",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DOCUMENTATION_PATH", "./documentation"),
        help="Directory for generated Markdown/Word documentation (default: ./documentation, "
        "or set OUTPUT_DOCUMENTATION_PATH env var)",
    )
    parser.add_argument("--skip-enrich", action="store_true", help="Skip deterministic enrichment (Step 5)")
    parser.add_argument("--skip-export", action="store_true", help="Skip Word export (Step 7)")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish the final documentation to a docs repo (Step 8) — requires "
        "DOCS_REPO_URL/DOCS_REPO_BRANCH to be set; off by default",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the intermediate JSON files")
    args = parser.parse_args()

    working_dir = Path(args.working_dir)
    working_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["TALEND_METADATA_PATH"] = str(working_dir / "talend_metadata.json")
    env["QLIK_METADATA_PATH"] = str(working_dir / "qlik_metadata.json")
    env["TALEND_CLOUD_METADATA_PATH"] = str(working_dir / "talend_cloud_metadata.json")
    env["OUTPUT_DOCUMENTATION_PATH"] = args.output_dir
    if args.branch:
        env["TALEND_GIT_BRANCH"] = args.branch

    pretty = ["--pretty"] if args.pretty else []

    talend_args = [*pretty, args.workspace] if args.workspace else pretty
    run_step("Step 1: Extract Talend Metadata", SRC / "talend" / "talend_extractor.py", talend_args, env, required=True)

    run_step(
        "Step 2: Extract Talend Cloud Scheduling Metadata",
        SRC / "talend" / "talend_cloud_extractor.py",
        pretty,
        env,
        required=False,
    )
    if not Path(env["TALEND_CLOUD_METADATA_PATH"]).is_file():
        # Same reasoning as the QLIK_METADATA_PATH case below: an explicit empty string,
        # not a missing key, so a stale .env default can't silently reappear.
        env["TALEND_CLOUD_METADATA_PATH"] = ""

    run_step(
        "Step 3: Extract Qlik Cloud Metadata",
        SRC / "qlik" / "qlik_cloud_extractor.py",
        pretty,
        env,
        required=False,
    )
    if not Path(env["QLIK_METADATA_PATH"]).is_file():
        # An empty string, not a missing key: each downstream script also calls its own
        # load_dotenv(), which (with override=False) only fills in a var that's ABSENT from
        # the environment — deleting the key here would let a stale QLIK_METADATA_PATH from
        # .env silently reappear and get treated as this run's Qlik data.
        env["QLIK_METADATA_PATH"] = ""

    run_step(
        "Step 4: Generate Documentation",
        SRC / "documentation" / "generate_documentation.py",
        [],
        env,
        required=True,
    )

    if args.skip_enrich:
        logger.info("Step 5: Deterministic Enrichment — skipped (--skip-enrich)")
    else:
        run_step(
            "Step 5: Deterministic Enrichment",
            SRC / "documentation" / "enrich_documentation.py",
            [],
            env,
            required=False,
        )

    if os.environ.get("AI_ENRICHMENT_ENABLED", "false").strip().lower() in ("1", "true", "yes"):
        run_step(
            "Step 6: AI-Powered Enrichment",
            SRC / "documentation" / "ai_enrich_documentation.py",
            [],
            env,
            required=False,
        )
    else:
        logger.info(
            "Step 6: AI-powered enrichment is a human/agent step and is not automated by this "
            f"script. Run the prompt in {Path(args.output_dir) / 'AI_DOCUMENTATION_PROMPT.md'} "
            "with Claude (or another LLM) for AI-authored narrative sections, then re-run "
            "export_docx.py (or this script with --skip-enrich) to pick up the changes. (Set "
            "AI_ENRICHMENT_ENABLED=true and ANTHROPIC_API_KEY to automate this step instead.)"
        )

    if args.skip_export:
        logger.info("Step 7: Export to Word — skipped (--skip-export)")
    else:
        run_step(
            "Step 7: Export to Word",
            SRC / "documentation" / "export_docx.py",
            [],
            env,
            required=False,
        )

    if args.publish:
        run_step(
            "Step 8: Publish Documentation to a Docs Repo",
            SRC / "documentation" / "publish_docs.py",
            [],
            env,
            required=False,
        )
    else:
        logger.info("Step 8: Publish Documentation to a Docs Repo — skipped (pass --publish to enable)")

    logger.info(f"Pipeline complete. Documentation written to: {args.output_dir}")


if __name__ == "__main__":
    main()
