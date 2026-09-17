# Talend Job: CUBS_Raw_PRE_ETL_Load

## Overview

Loads CUBS "ETL" credit/collections-scoring extract files for the PRE site — one row per debtor with bureau/collections attributes such as bankruptcy disposition codes (`BK7_DISP`, `BK11_DISP`, `BK13_DISP`), revolving/mortgage/auto trade balances, credit-card/available-credit fields, and scoring outputs (`Attune_Score`, `Propen_Score`, `Decile`, `Percentile`) — from every file found in `context.sourceDir` into the Snowflake raw landing table `CUBS_ETL_RAW_CURRENT`. All ~61 named business columns from the source file are flattened into generic `COL1`...`COL80` positions in the target table. Every file found in the source directory is loaded, archived, and then deleted in a separate cleanup pass. This job is structurally and configurationally near-identical to `CUBS_Raw_CO_ETL_Load` — same component wiring, same generic `COL1`-`COL80` target shape, same two-pass list-then-delete cleanup design — differing only in its site-specific repository schema label (`pre_etl` vs. `co_etl`) and, presumably, the context values bound to `sourceDir`/`archiveDir` at runtime (not captured in this metadata). Per `06_dependency_matrix.md`, it is called by the `CUBS_Raw_ETL_Load` parent job, consistent with the per-site `CUBS_Raw_<Site>_ETL_Load` family (CHI/CO/DC/HH/PRE/TOL).

## Detail table

| Field | Value |
|---|---|
| Job name | CUBS_Raw_PRE_ETL_Load |
| Version | 0.1 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2022-12-15T16:47:17.937-0800 |
| Last Modified | 2025-11-11T22:51:50.402-0800 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` → `tJava_1` (`OnComponentOk`) opens a per-run log file at `context.logDir + jobName + "_" + <timestamp> + ".log"` and redirects `System.out`/`System.err` to it → `tSetKeystore_1` (`OnSubjobOk`) configures SSL trust/keystore from `context.keystorePath` (all passwords redacted) → `tDBConnection_1` (`OnSubjobOk`) opens the Snowflake connection. **This job has no `tPostjob_1`/`tDBClose` component at all** — the Snowflake connection is never explicitly closed within this job's own metadata, the same gap documented in `CUBS_Raw_CO_ETL_Load`. See Issues observed.

**Main load pass** (no incoming trigger connection into `tFileList_1`, so per Talend's default semantics it runs as an independent top-level subjob alongside the setup subjob above):

1. `tFileList_1` lists files in `context.sourceDir`, ordered by modified date ascending. An `EXCLUDEFILEMASK` of `"*.txt"` is configured but `IFEXCLUDE` is `false`, so the exclusion never applies — every file in the directory is picked up.
2. For each file (`ITERATE`), `tJava_2` sets `context.currentFile`/`fileName`/`filePath` from the `tFileList_1` iteration globals.
3. `tFileInputDelimited_1` (`ITERATE`) reads that file as tab-delimited, ISO-8859-15 encoded, header row present, using repository schema `"...- pre_etl"` (~61 named bureau/collections-scoring columns). `DIE_ON_ERROR=false`; `TRIMALL=false`.
4. `tMap_1` (`row1`, `FLOW`) re-maps every source column **positionally** onto a generic 80-column target shape (`FILENAME`, `FILEDATE`, `COL1`...`COL80`) — none of the ~61 business column names survive into the target schema.
5. `tFlowMeter_2` (`etl`, `FLOW`) counts rows passing through (label left at the default `"MyLabel"`).
6. `tDBOutput_1` (`row2`, `FLOW`) inserts the rows into Snowflake `CUBS_ETL_RAW_CURRENT` (`INSERT`, `tableAction=NONE` — no truncate/recreate from within this job).
7. On success (`OnComponentOk`), `tFileArchive_1` archives the just-processed file (`context.filePath`) to `context.archiveDir + "/" + <YYYYMMDD> + "/" + context.fileName + ".tar.gz"` (password redacted).

**Cleanup pass** (triggered by `tFileList_1`'s `OnSubjobOk`, i.e. only after every file from the main load pass has finished processing):

8. `tFileList_2` re-lists the same `context.sourceDir` directory (same unapplied `EXCLUDEFILEMASK`/`IFEXCLUDE` mismatch as step 1).
9. For each file found (`ITERATE`), `tJava_3` sets `context.currentFile`/`fileName`/`filePath` again.
10. `tFileDelete_1` (`ITERATE`) deletes that file from disk.
11. On success (`OnComponentOk`), `tJava_4` logs the delete outcome (`CURRENT_STATUS`, `DELETE_PATH`, error message).

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> OpenLog["tJava_1<br/>Open per-run log file"] -->|OnSubjobOk| Keystore["tSetKeystore_1<br/>Configure SSL"] -->|OnSubjobOk| Connect["tDBConnection_1<br/>Open Snowflake connection<br/>(never explicitly closed)"]

    FileList1["tFileList_1<br/>List files in sourceDir<br/>(*.txt exclusion not applied)"] -->|Iterate| SetVars1["tJava_2<br/>Set currentFile/fileName/filePath"]
    SetVars1 -->|Iterate| ReadCSV["tFileInputDelimited_1<br/>Read tab-delimited file<br/>(schema: pre_etl)"]
    ReadCSV -->|row1| Map["tMap_1<br/>Flatten ~61 named cols to COL1..COL80"]
    Map -->|etl| FlowMeter["tFlowMeter_2<br/>Count rows"]
    FlowMeter -->|row2| Insert["tDBOutput_1<br/>INSERT into CUBS_ETL_RAW_CURRENT"]
    Insert -->|OnComponentOk| Archive["tFileArchive_1<br/>Archive file to archiveDir/YYYYMMDD/"]

    FileList1 -->|OnSubjobOk| FileList2["tFileList_2<br/>Re-list sourceDir"]
    FileList2 -->|Iterate| SetVars2["tJava_3<br/>Set currentFile/fileName/filePath"]
    SetVars2 -->|Iterate| Delete["tFileDelete_1<br/>Delete file"]
    Delete -->|OnComponentOk| LogDelete["tJava_4<br/>Log delete status"]
```

## Settings tables

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.currentFile` | The current file from `tFileList_1`'s iteration. |
| FIELDSEPARATOR / ENCODING | `\t` / ISO-8859-15 | Tab-delimited extract, ISO-8859-15 (Latin-9) encoded. |
| HEADER | `1` | One header row skipped. |
| SCHEMA (main) | Repository schema `"_YSgBwHzaEe2c-IsTynWu2Q - pre_etl"` | ~61 named bureau/collections-scoring columns (e.g. `DEBTOR`, `MORT_BAL`, `REV_BAL`, `CCARD`, `AUTO_BAL`, `BK7_DISP`/`BK11_DISP`/`BK13_DISP`, `Attune_Score`, `Propen_Score`, `Decile`, `Percentile`) — identical field set to `CUBS_Raw_CO_ETL_Load`'s `co_etl` schema, just a different site-specific repository label. |
| DIE_ON_ERROR | `false` | Malformed rows don't fail the job... |
| Reject flow | Not wired | ...but no connection routes rejected rows anywhere — silently dropped, same pattern flagged in `ADP_Payroll_Load` and `CUBS_Raw_CO_ETL_Load`. |
| TEMP_DIR | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace"` | Hardcoded developer-workstation path — see Dependencies & configuration. |

### Target: `tDBOutput_1` (`tSnowflakeOutput`)

| Setting | Value | What it means |
|---|---|---|
| Table | `CUBS_ETL_RAW_CURRENT` | Destination raw landing table — the same table name used by `CUBS_Raw_CO_ETL_Load` (and presumably every other site's `_ETL_Load` sibling); no visible site-discriminator column in this metadata. |
| Output action | `INSERT` | Appends rows; no truncate step precedes it in this job. |
| Table action | `NONE` | Table structure is not altered by this job. |

### `tFileArchive_1`

| Setting | Value | What it means |
|---|---|---|
| SOURCE | `context.filePath` | The directory of the just-loaded file. |
| TARGET | `context.archiveDir + "/" + <YYYYMMDD> + "/" + context.fileName + ".tar.gz"` | Per-file, dated archive. |
| PASSWORD | `***REDACTED***` | Archive is password-protected; actual value not present in extracted metadata. |

### `tFileDelete_1` (cleanup pass)

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.currentFile` | File found by the second `tFileList_2` listing. |
| DIRECTORY / PATH | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/delete_folder"` / `"...delete_folder or delete_file"` | Hardcoded developer-workstation defaults — see Dependencies & configuration. |
| FAILON | `false` | A missing/already-deleted file does not fail the job. |

### `tSetKeystore_1`

| Setting | Value | What it means |
|---|---|---|
| SSL_KEYSTORE | `context.keystorePath` | Client keystore path is externalized to context. |
| SSL_TRUSTSERVER_TRUSTSTORE | `"C:/clientTrustStore.trustStore"` | Hardcoded truststore path — not context-driven, unlike the keystore itself. |
| SSL_TRUSTSERVER_PASSWORD / SSL_KEYSTORE_PASSWORD / NEED_CLIENT_AUTH | `***REDACTED***` | Preserved as redacted; real values not present in extracted metadata. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** `runjob_targets` is empty — this job does not call any other job via `tRunJob`.
- **Called by:** `CUBS_Raw_ETL_Load` (1 call), per `06_dependency_matrix.md` — consistent with the per-site `CUBS_Raw_<Site>_ETL_Load` family documented in `01_system_architecture.md`. Unlike `CUBS_Raw_CO_ETL_Load`, this job is **not** also called by `CO_Master_Load` (there is no `PRE_Master_Load` orchestrator in this metadata — see `05_operational_runbook.md`'s note that only `CO` has a dedicated `_Master_Load`).
- **Context variables used:** `archiveDir`, `currentFile`, `fileName`, `filePath`, `keystorePath`, `logDir`, `sourceDir`.
- **5 hardcoded developer-workstation paths** (`tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, `tFileDelete_1.DIRECTORY`/`PATH`, `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE`), all under `C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...` or `C:/clientTrustStore.trustStore` — same project-wide portability risk documented in `05_operational_runbook.md` (210 of 289 jobs share this pattern).

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tPrejob` / `tPostjob` | Talend's guaranteed-first / guaranteed-last subjobs for setup and teardown (this job has no `tPostjob`). |
| `tJava` | Runs a block of custom Java code once. |
| `tFileList` | Lists files in a directory for the job to iterate over one at a time. |
| `tFileInputDelimited` | Reads a delimited (CSV/TSV-style) text file according to a schema. |
| `tMap` | Maps/transforms columns from one schema to another. |
| `tFlowMeter` | Counts rows passing through a point in the flow, for logging/monitoring. |
| `tSnowflakeOutput` / `tSnowflakeConnection` | Write rows to a Snowflake table / open the Snowflake connection used throughout the job. |
| `tFileArchive` / `tFileDelete` | Zip a processed file to an archive location, then delete the original from the source directory. |
| `tSetKeystore` | Configures SSL client keystore/truststore settings ahead of an encrypted database connection. |

## Issues observed

- **This job is a near-exact copy of `CUBS_Raw_CO_ETL_Load`** — identical component wiring, identical `COL1`-`COL80` flattening shape, identical two-pass list-then-delete cleanup design, identical unapplied `EXCLUDEFILEMASK`, identical missing `tPostjob`/`tDBClose`. The only difference visible in this job's own metadata is the repository schema label (`pre_etl` vs. `co_etl`); site differentiation for `sourceDir`/`archiveDir` must come from per-job context-value overrides not captured in this extraction — verify directly in Talend Studio before assuming what actually differs between the CHI/CO/DC/HH/PRE/TOL siblings.
- **No `tPostjob_1`/`tDBClose` in this job.** Same gap as `CUBS_Raw_CO_ETL_Load`: whether the Talend runtime closes the Snowflake connection implicitly at job exit, or this represents a real resource-leak risk across repeated runs, cannot be determined from this metadata; verify with the team.
- **`EXCLUDEFILEMASK="*.txt"` is configured but `IFEXCLUDE=false`** on both `tFileList_1` and `tFileList_2` — the mask is never applied, so every file in `context.sourceDir` is processed and later deleted, not just the intended extract format. Same unapplied-mask pattern flagged in `ADP_Payroll_Load` and `CUBS_Raw_CO_ETL_Load`.
- **Two-pass list-then-delete design.** `tFileList_2` re-lists `context.sourceDir` from scratch only after the entire main load loop finishes (`OnSubjobOk`), rather than deleting each file immediately after its own successful archive. If a new file lands in `context.sourceDir` in the window between the two listings, it would be picked up and deleted by the cleanup pass without ever having been loaded. Unable to confirm the exposure window from this metadata; verify with the team.
- **`tMap_1` discards all ~61 business column names** from the `pre_etl` schema, storing them only as generic `COL1`...`COL80` in `CUBS_ETL_RAW_CURRENT`. Any downstream consumer of that table must already know the column-position-to-business-field mapping from outside this job's own metadata.
- **`tFlowMeter_2`'s label is left at the default `"MyLabel"`**, not renamed for this job — cosmetic only, but makes its log output indistinguishable from any other unrenamed `tFlowMeter` in the project (same as `CUBS_Raw_CO_ETL_Load`).
