# Qlik + Talend Documentation Toolkit

Automated metadata extraction and documentation generation for a Qlik Cloud + Talend Studio/Cloud data platform. Designed for situations where the original developer is unavailable and no documentation exists.

## What This Toolkit Does

1. **Extracts implementation metadata** (job definitions, load scripts, schemas, connections) — never production data
2. **Generates structured Markdown documentation** from the extracted metadata
3. **Provides an AI prompt template** for enriching the documentation with Claude or another LLM
4. **Exports everything to Word** (`.docx`), with Mermaid diagrams rendered as embedded images

## Security Guarantees

- **No production data is extracted.** Only job definitions, component configurations, load scripts, and connection targets are captured.
- **Credentials are automatically redacted.** Any parameter matching known credential patterns (password, token, secret, etc.) is replaced with `***REDACTED***`.
- **Scripts run inside your network.** Nothing is sent externally — you control when and how the output reaches an AI — with one opt-in exception: `publish_docs.py` (Step 8) pushes the generated `documentation/` tree to the docs repo you configure via `--docs-repo-url`.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager (installs and pins the Python version from `.python-version` automatically)
- Access to the Talend Studio workspace directory (local filesystem)
- A Qlik Cloud API key with read access (Management Console → API keys)
- `git` CLI installed and available on `PATH` (needed for git-repo input to `talend_extractor.py` and for the optional docs-publish stage)
- For the optional docs-publish stage (`publish_docs.py`): a git identity configured in the environment it runs in (`git config user.name`/`user.email`, either globally or via `GIT_AUTHOR_NAME`/`GIT_AUTHOR_EMAIL`/`GIT_COMMITTER_NAME`/`GIT_COMMITTER_EMAIL` env vars) — otherwise the commit step fails with "Author identity unknown"

Install dependencies (`requests` for the Qlik extractor, `python-docx`/`mermaidx` for the Word exporter, `python-dotenv` for `.env` loading, `ruff` for lint):

```bash
uv sync
```

`uv run` below executes each script inside that managed environment — no manual venv activation needed.

## Quick Start

### Run the Whole Pipeline at Once

`run_pipeline.py` runs Steps 1–5, 7, and (opt-in) 8 below in one command — Talend extraction, the optional Talend Cloud/Qlik extractors (only if their env vars enable them), Markdown generation, deterministic enrichment, and Word export:

```bash
uv run run_pipeline.py /path/to/talend/workspace
```

Step 6 (AI-powered enrichment) is opt-in: set `AI_ENRICHMENT_ENABLED=true` (and `ANTHROPIC_API_KEY`) to have it run automatically as part of this command; otherwise it stays a human/agent step and the command above just prints where to find the prompt once it's done. Use `--skip-enrich`/`--skip-export` to omit a stage, or `--publish` to also push the result to a docs repo (requires `DOCS_REPO_URL`/`DOCS_REPO_BRANCH`). Run `uv run run_pipeline.py --help` for the full flag list, or follow the steps below individually for finer control over each stage's options.

### Step 1: Extract Talend Metadata

```bash
# Point to the Talend Studio workspace directory
uv run src/talend/talend_extractor.py /path/to/talend/workspace \
    --output talend_metadata.json \
    --pretty
```

The workspace directory is typically where Talend Studio stores projects. Look for a directory containing subdirectories with `process/` folders inside them.

Common locations:

- Windows: `C:\Users\<user>\talend-workspace\`
- Linux/Mac: `~/talend-workspace/`
- Or wherever the previous developer configured their Studio workspace

The workspace path can also be set via env var instead of passing it as an argument:

```bash
export TALEND_STUDIO_WORKSPACE_PATH="/path/to/talend/workspace"
uv run src/talend/talend_extractor.py --output talend_metadata.json --pretty
```

#### Archive input, instead of a directory

You can also point the extractor directly at a Talend Studio project export `.zip` — it validates, unpacks, and extracts it using the exact same parsing logic as the directory path above:

```bash
uv run src/talend/talend_extractor.py /path/to/talend-project.zip \
    --output talend_metadata.json \
    --working-dir full-documentation/working \
    --report-output full-documentation/output/extraction-report.json
```

#### Git repo input, instead of a directory or archive

You can also point the extractor at a git repo URL — it clones (or, on a rerun, fetches and hard-resets) the given branch into a working directory, then extracts it using the exact same parsing logic as the directory and archive paths above. A git URL is detected automatically (`https://`, `ssh://`, `git://`, `file://`, or scp-style `git@host:org/repo.git`) — no separate flag needed to opt in, but `--branch` is required.

| Flag                    | Env var                          | Default                                            | Purpose                                                           |
| ------------------------ | --------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------ |
| `--branch`               | `TALEND_GIT_BRANCH`               | _(none — required for a git URL)_                   | Branch to clone/checkout                                          |
| `--git-token-env-var`    | `TALEND_GIT_TOKEN_ENV_VAR`        | `TALEND_GIT_TOKEN`                                 | Name of the env var holding an HTTPS auth token                  |
| `--git-ssh-key-env-var`  | `TALEND_GIT_SSH_KEY_PATH_ENV_VAR` | `TALEND_GIT_SSH_KEY_PATH`                          | Name of the env var holding an SSH private key path               |
| `--working-dir`          | `TALEND_ARCHIVE_WORKING_DIR`      | `full-documentation/working`                       | Directory to clone into (shared with archive mode's unpack dir)   |
| `--report-output`        | `TALEND_EXTRACTION_REPORT_PATH`   | `full-documentation/output/extraction-report.json` | Where to write `extraction-report.json`                          |

HTTPS + token auth — the token is read from the env var named by `--git-token-env-var` (default `TALEND_GIT_TOKEN`), never passed on the command line:

```bash
export TALEND_GIT_TOKEN="your-token-here"

uv run src/talend/talend_extractor.py https://github.com/your-org/talend-workspace.git \
    --branch main \
    --output talend_metadata.json \
    --pretty
```

SSH key auth — the key path is read from the env var named by `--git-ssh-key-env-var` (default `TALEND_GIT_SSH_KEY_PATH`):

```bash
export TALEND_GIT_SSH_KEY_PATH="$HOME/.ssh/id_ed25519"

uv run src/talend/talend_extractor.py git@github.com:your-org/talend-workspace.git \
    --branch main \
    --output talend_metadata.json \
    --pretty
```

Both the repo URL (with any embedded credential redacted) and the resolved commit SHA are recorded in `extraction-report.json` — see below. Only `https://` (token) and `ssh://`/scp-style (SSH key) are supported in production; `file://` is recognized only to let local self-checks point at a local bare repo.

Every run — workspace directory, archive, or git repo — also writes an **extraction report**: archive SHA-256 checksum (archive mode only), git repo URL/branch/commit SHA (git mode only — `repo_url` has any embedded token redacted; all three are `null` under directory or archive mode), per-job status (`SUCCESS` / `PARTIAL` / `FAILED` / `SKIPPED_DUPLICATE`), and any unsupported artifact folders found (`joblets/`, `routes/`, `code/routines/` — not yet parsed). Default location: `full-documentation/output/extraction-report.json` (override with `--report-output` or `TALEND_EXTRACTION_REPORT_PATH`).

### Step 2: Extract Talend Cloud Scheduling Metadata (optional)

If jobs are deployed as Tasks in Talend Cloud Management Console (TMC), this pulls task definitions, schedules/triggers, and recent execution history — separately from the Studio workspace extraction above, since Studio has no visibility into how a deployed job is actually scheduled.

**Disabled by default.** This extractor is opt-in: it exits immediately unless `TALEND_CLOUD_EXTRACTOR_ENABLED=true` is set — so running it unattended (e.g. in a scheduled job alongside the other extractors) is a safe no-op until you explicitly turn it on.

```bash
export TALEND_CLOUD_EXTRACTOR_ENABLED="true"
export TALEND_CLOUD_BASE_URL="https://api.eu.cloud.talend.com"
export TALEND_STUDIO_ACCESS_TOKEN="your-personal-access-token"

uv run src/talend/talend_cloud_extractor.py \
    --output talend_cloud_metadata.json \
    --pretty
```

Generate a personal access token in the Talend Cloud portal: your username (top-right) → Profile preferences → Personal access tokens → Add token. `--base-url` is the full regional API URL (`https://api.<eu|us|ap|au|us-west>.cloud.talend.com`) — no region-code shorthand.

This output is standalone — `generate_documentation.py` doesn't consume it yet (see [Extending](#extending)). Feed `talend_cloud_metadata.json` to the AI enrichment step (Step 6) alongside the other two JSON files if you want schedule/execution info reflected in the generated docs.

### Step 3: Extract Qlik Cloud Metadata (optional)

**Disabled by default.** This extractor is opt-in: it exits immediately unless `QLIK_EXTRACTOR_ENABLED=true` is set — so running it unattended (e.g. in a scheduled job alongside the other extractors) is a safe no-op until you explicitly turn it on. If you skip this step, Steps 4/5 proceed with Talend metadata only (see the note under Step 4).

```bash
# Set your API key and tenant (or pass via --api-key / --tenant)
export QLIK_EXTRACTOR_ENABLED="true"
export QLIK_API_KEY="your-api-key-here"
export QLIK_TENANT_URL="your-tenant.eu.qlikcloud.com"

uv run src/qlik/qlik_cloud_extractor.py \
    --output qlik_metadata.json \
    --pretty
```

To extract only specific apps:

```bash
uv run src/qlik/qlik_cloud_extractor.py \
    --tenant your-tenant.eu.qlikcloud.com \
    --apps "Sales Dashboard,Finance Report" \
    --output qlik_metadata.json
```

### Step 4: Generate Documentation

```bash
uv run src/documentation/generate_documentation.py \
    --talend talend_metadata.json \
    --qlik qlik_metadata.json \
    --output ./documentation/
```

(`talend_cloud_metadata.json` from Step 2 isn't consumed here — the Markdown skeleton this step produces doesn't include a scheduling section. Feed it to Step 5's deterministic enrichment instead, which does link it in.)

`--qlik` is optional here too, matching Step 3's opt-in default: if you skipped Step 3 (or `qlik_metadata.json` is missing or malformed for any other reason), this step logs a warning and generates Talend-only documentation instead of failing.

This creates:

```
documentation/
├── 00_system_overview.md          # Architecture and data flow
├── AI_DOCUMENTATION_PROMPT.md     # Prompt for AI enrichment
├── talend/
│   └── <ProjectName>/
│       ├── job_<JobName>.md       # Per-job documentation
│       ├── database_connections.md
│       └── context_groups.md
└── qlik/
    ├── app_<AppName>.md           # Per-app documentation
    └── data_connections.md
```

### Step 5: Deterministic Enrichment (optional)

`src/documentation/enrich_documentation.py` adds the deeper analytical documents the AI prompt
template asks for — without calling any AI. It groups jobs by inferred kind
(real ETL pipeline vs. component-demo tutorial job vs. orchestration, etc.),
correlates DB connections to the jobs likely using them, and maps
`tRunJob`/context-variable dependencies. It also auto-detects and flags
workspaces/tenants that look like Talend's bundled demo project or an empty
trial tenant, so the generated docs don't misrepresent test data as a real
production platform.

```bash
uv run src/documentation/enrich_documentation.py \
    --talend talend_metadata.json \
    --qlik qlik_metadata.json \
    --output ./documentation/
```

Pass `--talend-cloud talend_cloud_metadata.json` (optional) to also link each Talend Cloud task (Step 2) back to its Studio job by artifact name — surfaced in `02_job_documentation.md` (per-job schedule) and `06_dependency_matrix.md` (job↔task table, plus any cloud tasks with no matching job). Linking is best-effort: a missing or malformed `--talend-cloud` file logs a warning and the other five documents are generated normally.

`--qlik` is likewise best-effort: a missing or malformed `qlik_metadata.json` (e.g. because Step 3 was skipped) logs a warning and enrichment proceeds with Talend metadata only — `03_qlik_app_documentation.md` is simply omitted in that case, and the other four documents are generated normally.

Adds to `documentation/`:

```
├── 01_system_architecture.md      # What actually exists + Mermaid diagram
├── 02_job_documentation.md        # Jobs grouped by kind, with risk flags
├── 03_qlik_app_documentation.md   # Per-app detail, or "0 apps" if empty
├── 04_data_lineage_map.md         # Intra-job source→target lineage
├── 05_operational_runbook.md      # Failure points, restart order, gaps
└── 06_dependency_matrix.md        # Job↔connection, job↔context, job↔job
```

### Step 6: AI-Powered Enrichment

Take the generated documentation (or the raw JSON files) and feed them to Claude — either automatically (recommended, if you have an Anthropic API key) or by hand.

#### Automated (opt-in)

**Disabled by default.** `src/documentation/ai_enrich_documentation.py` calls Claude directly — one API call per document (per Talend job, per Qlik app, and once each for the four system-level docs) — using the existing content from Steps 4/5 as ground truth, and overwrites `01_system_architecture.md`, every `talend/<ProjectName>/job_<JobName>.md`, every `qlik/app_<AppName>.md`, `04_data_lineage_map.md`, `05_operational_runbook.md`, and `06_dependency_matrix.md` with narrative versions in place. It exits immediately unless `AI_ENRICHMENT_ENABLED=true` is set — so running it unattended is a safe no-op until you explicitly turn it on. Requires Steps 4 and 5 to have already run (it reads their output as input, and errors clearly if a target file doesn't exist yet).

```bash
export AI_ENRICHMENT_ENABLED="true"
export ANTHROPIC_API_KEY="sk-ant-..."

# Preview how many API calls would be made, without calling the API or writing anything
uv run src/documentation/ai_enrich_documentation.py --dry-run

# Then actually run it
uv run src/documentation/ai_enrich_documentation.py \
    --talend talend_metadata.json \
    --qlik qlik_metadata.json \
    --output ./documentation/
```

Model/token/temperature settings live in `config/llm.yaml` (tracked, no secrets — the API key is always read from `ANTHROPIC_API_KEY` only):

```yaml
llm:
  provider: anthropic
  model: claude-sonnet-5
  max_tokens: 4096
  temperature: 0.2
```

Override the model for a single run with `--model`, or the config file path with `--config` / `AI_ENRICHMENT_CONFIG`. A failure on any one document (job, app, or system-level doc) is logged and skipped — the previous file content is left in place, and the run continues with the rest; the exit code is non-zero only if at least one document failed.

#### Manual (fallback, or if you don't have an Anthropic API key)

**Running in a CLI coding agent (Claude Code, etc.) from the repository root** — the prompt in `AI_DOCUMENTATION_PROMPT.md` now tells Claude exactly which file each document belongs in (e.g. `01_system_architecture.md`, `talend/<ProjectName>/job_<JobName>.md`); just run the prompt and it writes each document directly into `documentation/` for you — no manual copy/paste step:

1. Open the prompt file: `documentation/AI_DOCUMENTATION_PROMPT.md`
2. Run its "Prompt Template" content, with `talend_metadata.json`/`qlik_metadata.json` in context
3. Claude writes each generated document straight to its listed file path under `documentation/`

**Running in a plain chat/API session with no file access** (claude.ai, the API, etc.):

1. Upload `talend_metadata.json` and `qlik_metadata.json`
2. Use the prompt from `AI_DOCUMENTATION_PROMPT.md`
3. Claude will print each document under a heading matching its file path
4. Save each one back into the matching file under `documentation/` by hand

### Step 7: Export to Word (optional)

Run this **last**, after any AI-authored Markdown has been saved back into `documentation/`. Converts every `.md` file in the tree into a `.docx` file under a mirrored `documentation/docx/` subtree:

```bash
uv run src/documentation/export_docx.py documentation/
```

Headings, paragraphs, lists, and tables become native Word elements. Every fenced ` ```mermaid ` block is rendered to a PNG and embedded as a picture — no separate diagram files, no manual conversion, and nothing is written to disk except the finished `.docx` files.

### Step 8: Publish Documentation to a Docs Repo (optional)

If the generated documentation should live in its own repo — separate from this toolkit's source, with its own history — `publish_docs.py` clones (or updates) that repo, replaces its contents with the current `documentation/` tree, commits, and pushes. It publishes `documentation/` (the finished output), not `full-documentation/` (this toolkit's scratch/working space) — run it last, after Step 7, so the `docx/` subtree it publishes is up to date too.

```bash
export DOCS_REPO_URL="https://github.com/your-org/docs-repo.git"
export DOCS_REPO_BRANCH="main"
export DOCS_REPO_GIT_TOKEN="your-token-here"

# Preview what would change first
uv run src/documentation/publish_docs.py --dry-run

# Then actually commit and push
uv run src/documentation/publish_docs.py
```

| Flag                     | Env var                             | Default                                | Purpose                                                          |
| ------------------------- | ------------------------------------ | ----------------------------------------- | ------------------------------------------------------------------ |
| `--docs-repo-url`         | `DOCS_REPO_URL`                     | _(none — required)_                    | Git URL of the docs repo to publish into                         |
| `--branch`                | `DOCS_REPO_BRANCH`                  | _(none — required)_                    | Branch to publish to                                              |
| `--local-path`            | `DOCS_REPO_LOCAL_PATH`              | `full-documentation/docs-repo-working` | Local working directory for the cloned docs repo                  |
| `--source-dir`            | `DOCS_REPO_SOURCE_DIR`              | `documentation`                        | Directory whose contents get published                            |
| `--project-subdir`        | `DOCS_REPO_PROJECT_SUBDIR`          | `""` (docs repo root)                  | Subdirectory within the docs repo to publish into                 |
| `--git-token-env-var`     | `DOCS_REPO_GIT_TOKEN_ENV_VAR`       | `DOCS_REPO_GIT_TOKEN`                  | Name of the env var holding an HTTPS auth token for the docs repo |
| `--git-ssh-key-env-var`   | `DOCS_REPO_GIT_SSH_KEY_PATH_ENV_VAR` | `DOCS_REPO_GIT_SSH_KEY_PATH`           | Name of the env var holding an SSH private key path for the docs repo |
| `--commit-message`        | `DOCS_REPO_COMMIT_MESSAGE`          | auto-generated                         | Commit message (defaults to `docs: update documentation (<date>)`, suffixed with the source commit SHA when the last extraction ran in git mode) |
| `--dry-run`               | —                                    | off                                     | Copy files and print what would change, but don't commit or push  |

SSH-key auth for the docs repo works the same way as Mode C above: set `DOCS_REPO_GIT_SSH_KEY_PATH` to a private key path and use an `ssh://` or scp-style (`git@host:org/repo.git`) `--docs-repo-url`. Publishing replaces the destination's contents wholesale (except its `.git` directory) before copying `documentation/` back in, so files removed from `documentation/` since the last publish are also removed from the docs repo. Pushing is skipped (a safe no-op) if there's nothing new to commit.

## What Each Script Extracts

### src/talend/talend_extractor.py

| Extracted                                              | NOT Extracted               |
| ------------------------------------------------------ | --------------------------- |
| Job names and descriptions                             | Production data             |
| Component types and configurations                     | Actual database contents    |
| Schema definitions (column names, types)               | Row-level data              |
| Data flow connections between components               | Passwords/tokens (redacted) |
| Context variables (names, types)                       | Encrypted values            |
| Database connection targets (host, port, DB)           | Query result sets           |
| Job author (Talend user login), created/modified dates | —                           |

### src/qlik/qlik_cloud_extractor.py

| Extracted                           | NOT Extracted             |
| ----------------------------------- | ------------------------- |
| App names and descriptions          | Dashboard data values     |
| Load scripts (SQL, transformations) | User-specific data        |
| Data connection names and types     | API keys (redacted)       |
| Reload task schedules               | Session tokens            |
| Space and ownership info            | Actual query results      |
| Table names from load scripts       | Bookmarks/selections data |

### src/talend/talend_cloud_extractor.py

| Extracted                                     | NOT Extracted                                      |
| --------------------------------------------- | -------------------------------------------------- |
| Task names, workspace/environment names       | Production data                                    |
| Schedules/triggers (cron, interval, enabled)  | Job/task mutation (read-only, never writes)        |
| Recent execution history (status, timestamps) | Row-level execution logs                           |
| Task parameters (context variables)           | Parameters matching credential keywords (redacted) |
| Deployed artifact name/version                | Passwords/tokens (redacted)                        |

## Troubleshooting

### "No Talend projects found"

The script looks for subdirectories containing a `process/` folder. Make sure you're pointing to the workspace root, not a project subdirectory.

### Qlik API returns 401

Your API key may have expired or lack sufficient permissions. Create a new key in Management Console → API keys with at minimum "Developer" role.

### Qlik API returns 429

The script has built-in retry with backoff. If it persists, add `time.sleep(1)` between app extractions or use `--apps` to extract in batches.

### Large workspace takes too long

For workspaces with 100+ jobs, consider extracting one project at a time or filtering by modification date.

## Extending

- **Add Snowflake metadata**: Write a similar extractor using the Snowflake Python connector to pull table schemas, views, and stored procedures from `INFORMATION_SCHEMA`.
- **External scheduler support**: If jobs are also orchestrated via a non-Talend scheduler (Airflow, Control-M), a similar standalone extractor could pull those schedules too.
- **Automate updates**: Run the extractors on a schedule (cron, Task Scheduler) and regenerate docs whenever the system changes.
