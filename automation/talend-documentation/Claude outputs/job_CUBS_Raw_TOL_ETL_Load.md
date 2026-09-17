# Talend Job: CUBS_Raw_TOL_ETL_Load

## Overview

Loads CUBS "ETL" credit/collections-scoring extract files for the TOL site — one row per debtor with bureau/collections attributes (bankruptcy disposition codes, revolving/mortgage/auto trade balances, credit-card/available-credit fields, and scoring outputs like `Attune_Score`, `Propen_Score`, `Decile`, `Percentile`) — from `context.sourceDir` into the shared Snowflake raw landing table `CUBS_ETL_RAW_CURRENT`. Every file found in the source directory is loaded, archived, and then deleted in a separate cleanup pass. This job is structurally near-identical to its `CUBS_Raw_CO_ETL_Load`/`CHI`/`DC`/`HH`/`PRE` siblings, but — unlike those four — it reads its input using the **`co_etl` repository schema instead of a `tol_etl` schema**, which appears to be a copy-paste artifact (see Issues observed).

## Detail table

| Field | Value |
|---|---|
| Job name | CUBS_Raw_TOL_ETL_Load |
| Version | 0.1 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2024-04-18T09:19:43.790-0700 |
| Last Modified | 2025-11-12T05:59:47.331-0800 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` → `tJava_1` (`OnComponentOk`) opens a per-run log file at `context.logDir + jobName + "_" + <timestamp> + ".log"` and redirects `System.out`/`System.err` to it → `tSetKeystore_1` (`OnSubjobOk`) configures SSL trust/keystore from `context.keystorePath` (all passwords redacted) → `tDBConnection_1` (`OnSubjobOk`) opens the Snowflake connection. As with `CUBS_Raw_CO_ETL_Load`, **this job has no `tPostjob_1`/`tDBClose` component** — the Snowflake connection is never explicitly closed within this job's own metadata.

**Main load pass** (no incoming trigger connection to `tFileList_1`, so it starts as an independent top-level subjob alongside the setup subjob above):

1. `tFileList_1` lists files in `context.sourceDir`, ordered by modified date ascending. An `EXCLUDEFILEMASK` of `"*.txt"` is configured but `IFEXCLUDE=false`, so the exclusion is never applied — every file in the directory is picked up.
2. For each file (`Iterate`), `tJava_2` sets `context.currentFile`/`fileName`/`filePath` from the `tFileList_1` iteration globals.
3. `tFileInputDelimited_1` (`Iterate`) reads that file as tab-delimited, ISO-8859-15 encoded, header row present, using repository schema `"...- co_etl"` — **the same schema label used by `CUBS_Raw_CO_ETL_Load`**, not a TOL-specific one (see Issues observed). `DIE_ON_ERROR=false`; `TRIMALL=false`.
4. `tMap_1` (`row1`, FLOW) re-maps the source columns **positionally** onto a generic 80-column target shape (`FILENAME`, `FILEDATE`, `COL1`...`COL80`).
5. `tFlowMeter_2` (`etl`, FLOW) counts rows passing through (label left at the default `"MyLabel"`).
6. `tDBOutput_1` (`row2`, FLOW) inserts the rows into Snowflake `CUBS_ETL_RAW_CURRENT` (`INSERT`, `tableAction=NONE`) — the same shared raw landing table used by all site `_ETL_Load` jobs.
7. On success (`OnComponentOk`), `tFileArchive_1` archives the just-processed file (`context.filePath`) to `context.archiveDir + "/" + <YYYYMMDD> + "/" + context.fileName + ".tar.gz"` (password redacted).

**Cleanup pass** (triggered by `tFileList_1`'s `OnSubjobOk`, i.e. only after every file from the main load pass has finished processing):

8. `tFileList_2` re-lists the same `context.sourceDir` directory (same unapplied `EXCLUDEFILEMASK`/`IFEXCLUDE` mismatch as step 1).
9. For each file found (`Iterate`), `tJava_3` sets `context.currentFile`/`fileName`/`filePath` again.
10. `tFileDelete_1` (`Iterate`) deletes that file from disk.
11. On success (`OnComponentOk`), `tJava_4` logs the delete outcome (`CURRENT_STATUS`, `DELETE_PATH`, error message).

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> OpenLog["tJava_1<br/>Open per-run log file"] -->|OnSubjobOk| Keystore["tSetKeystore_1<br/>Configure SSL"] -->|OnSubjobOk| Connect["tDBConnection_1<br/>Open Snowflake connection<br/>(never explicitly closed)"]

    FileList1["tFileList_1<br/>List files in sourceDir<br/>(*.txt exclusion not applied)"] -->|Iterate| SetVars1["tJava_2<br/>Set currentFile/fileName/filePath"]
    SetVars1 -->|Iterate| ReadCSV["tFileInputDelimited_1<br/>Read tab-delimited file<br/>(schema: co_etl — see Issues)"]
    ReadCSV -->|row1| Map["tMap_1<br/>Flatten columns to COL1..COL80"]
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
| SCHEMA (main) | Repository schema `"...- co_etl"` (GUID `_jsSQMHyoEe2c-IsTynWu2Q`) | Same schema GUID and label used by `CUBS_Raw_CO_ETL_Load` — **not** a TOL-specific schema. See Issues observed. |
| DIE_ON_ERROR | `false` | Malformed rows don't fail the job... |
| Reject flow | Not wired | ...but no connection routes rejected rows anywhere — silently dropped, same pattern documented across this job family. |
| TEMP_DIR | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace"` | Hardcoded developer-workstation path — see Dependencies & configuration. |

### Target: `tDBOutput_1` (`tSnowflakeOutput`)

| Setting | Value | What it means |
|---|---|---|
| Table | `CUBS_ETL_RAW_CURRENT` | Destination raw landing table — the same table name used by all site `_ETL_Load` jobs in this family (CO/CHI/DC/HH/PRE/TOL), differentiated only by `FILENAME`/`FILEDATE` values on each row, not by a separate table or site column. |
| Output action | `INSERT` | Appends rows; no truncate step precedes it in this job. |
| Table action | `NONE` | Table structure is not altered by this job. |

### `tFileArchive_1`

| Setting | Value | What it means |
|---|---|---|
| SOURCE | `context.filePath` | The directory of the just-loaded file. |
| SOURCE_FILE | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/source.csv"` | Hardcoded developer-workstation default value — see Dependencies & configuration. |
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
- **Called by:** `CUBS_Raw_ETL_Load` (1 call), per `06_dependency_matrix.md` — consistent with the per-site `CUBS_Raw_<Site>_ETL_Load` family documented in `01_system_architecture.md`. Unlike `CO`, TOL has no dedicated `_Master_Load` orchestrator in this metadata.
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

- **This job's input schema is `co_etl`, not a TOL-specific schema.** `tFileInputDelimited_1.SCHEMA:REPOSITORY_SCHEMA_TYPE` is `_jsSQMHyoEe2c-IsTynWu2Q - co_etl` — the exact same repository schema GUID and label used by `CUBS_Raw_CO_ETL_Load`. By contrast, the CHI/DC/HH/PRE siblings in this family each reference their own site-specific schema (`chi_etl`, `dc_etl`, `hh_etl`, `pre_etl` — each with a distinct GUID). This strongly suggests `CUBS_Raw_TOL_ETL_Load` was cloned from `CUBS_Raw_CO_ETL_Load` and the schema reference was never repointed to a TOL-specific one. Whether TOL's actual source-file column layout happens to match CO's (making this harmless) or genuinely differs (which could silently misalign columns or truncate/drop TOL-specific fields) is unable to determine from this metadata — verify directly against a real TOL extract file in Talend Studio.
- **All six site `_ETL_Load` jobs write into the same shared table, `CUBS_ETL_RAW_CURRENT`**, with no site column and `tableAction=NONE`/`INSERT`-only (no truncate). Rows from different sites are distinguished only by `FILENAME`/`FILEDATE`, and multiple sites' extracts can coexist and accumulate in the same table across runs unless something downstream (e.g. the merge/ETL step not visible in this job's own metadata) filters or clears by filename pattern. This is a project-wide pattern across the family, not unique to TOL, but combined with the schema mix-up above it's worth flagging that a schema mismatch here would land bad data directly into the shared table.
- **No `tPostjob_1`/`tDBClose` in this job** — the Snowflake connection opened by `tDBConnection_1` is never explicitly closed within this job's own metadata, the same gap already flagged in `CUBS_Raw_CO_ETL_Load`.
- **`EXCLUDEFILEMASK="*.txt"` is configured but `IFEXCLUDE=false`** on both `tFileList_1` and `tFileList_2` — the mask is never applied, so every file in `context.sourceDir` is processed and later deleted, not just the intended extract format. Same unapplied-mask pattern flagged project-wide (e.g. `ADP_Payroll_Load`, `CUBS_Raw_CO_ETL_Load`).
- **Two-pass list-then-delete design.** `tFileList_2` re-lists `context.sourceDir` from scratch only after the entire main load loop finishes (`OnSubjobOk`), rather than deleting each file immediately after its own successful archive. If a new file lands in `context.sourceDir` in the window between the two listings, it would be picked up and deleted by the cleanup pass without ever having been loaded. Unable to confirm the exposure window from this metadata; verify with the team.
