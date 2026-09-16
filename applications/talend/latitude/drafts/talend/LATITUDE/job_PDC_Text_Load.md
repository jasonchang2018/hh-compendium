# Talend Job: PDC_Text_Load

## Overview

This job follows the project's standard text-load pattern exactly: it watches a shared folder for a new post-dated-check (PDC) file, loads it into a Snowflake staging table, merges the staged rows into the permanent table via a stored procedure, and then archives and deletes the source file. It has no `tDie`/`tWarn` reacting to the merge outcome.

## Detail table

| Field | Value |
|---|---|
| Job name | PDC_Text_Load |
| Version | 0.1 |
| Project | LATITUDE |
| Author | jmach@harriscollect.com |
| Created | 2024-11-27T11:19:28.352-0800 |
| Last Modified | 2025-09-25T08:24:12.084-0700 |

## Step-by-step data flow

1. **Set up.** `tPrejob_1` triggers `tDBConnection_1` (Snowflake connect); separately, `tJava_2` appends today's date to `context.archiveDir` and starts a log file, then hands off to `tSetKeystore_1`.
2. **Empty the staging table.** `tDBRow_1` runs `TRUNCATE TABLE PDC_TXT;` (unqualified — no `LIQUID_STAGING.` prefix).
3. **Find the file.** `tFileList_1` lists files in `context.sourceDir`, skipping `.txt` files. `tJava_1` captures the match into `context.filePath`.
4. **Read and reshape.** `tFileInputDelimited_1` reads the file as pipe-delimited (`|~|`/`|$|`), US-ASCII-encoded, with a header row (`DIE_ON_ERROR = false`). `tMap_1` maps ~44 PDC columns (check number, deposit/hold flags, amount, surcharge, payment-vendor token, arrangement ID, etc.) onto the target schema, adding `LOAD_DT`.
5. **Load staging.** Mapped rows flow into `tDBOutput_1`, which inserts them into `PDC_TXT` (`INSERT`, no table-structure changes).
6. **Merge into the permanent table — in parallel with cleanup.** `tParallelize_1` splits into:
   - **Merge branch:** `tDBRow_2` runs `CALL MERGE_TXT_INTO_PDC();`.
   - **Cleanup branch:** the source file is re-listed, archived (`tFileArchive_1`, zipped into `context.archiveDir/<filename>.zip`), and — via a separate file-list/capture — deleted (`tFileDelete_1`).

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> Connect["tDBConnection_1"]
    SetLog["tJava_2<br/>Set archive path + start log"] --> Keystore["tSetKeystore_1"]
    Truncate["tDBRow_1<br/>TRUNCATE PDC_TXT"] --> ListFiles1["tFileList_1<br/>Find newest source file"]
    ListFiles1 -->|iterate| SetPath["tJava_1<br/>Capture file path"] --> ReadFile["tFileInputDelimited_1<br/>Read pipe-delimited file"]
    ReadFile -->|flow| Map["tMap_1<br/>Map columns to PDC schema"] --> Insert["tDBOutput_1<br/>INSERT into staging"]
    ListFiles1 --> Parallel["tParallelize_1"]
    Parallel --> ListFiles2["tFileList_2"] & Merge["tDBRow_2<br/>CALL MERGE_TXT_INTO_PDC()"]
    ListFiles2 -->|iterate| SetPath2["tJava_3"] --> Archive["tFileArchive_1<br/>Zip into archive dir"]
    ListFiles2 --> ListFiles3["tFileList_3"]
    ListFiles3 -->|iterate| SetPath3["tJava_4"] --> Delete["tFileDelete_1<br/>Delete source file"]
```

## Settings tables

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.filePath` | Reads whichever file `tFileList_1` found. |
| FIELDSEPARATOR / ROWSEPARATOR | `\|~\|` / `\|$\|` | Standard custom-delimited format. |
| HEADER | 1 | First line is a header row. |
| ENCODING | US-ASCII | Not ISO-8859-15. |
| DIE_ON_ERROR | false | Malformed rows are routed to the reject schema rather than failing the job outright. |

### Target: `tDBOutput_1`

| Setting | Value | What it means |
|---|---|---|
| Table | PDC_TXT | Staging table for post-dated-check records. |
| Output action | INSERT | Adds rows only. |
| Table action | NONE | No structural changes; truncation handled by `tDBRow_1`. |

### Merge step: `tDBRow_2`

| Setting | Value | What it means |
|---|---|---|
| Query | `CALL MERGE_TXT_INTO_PDC();` | Snowflake stored procedure that folds staged rows into the permanent PDC table; logic is outside Talend. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none — no `tRunJob` links found.
- **Context variables used:** `context.sourceDir`, `context.archiveDir`, `context.filePath`, `context.logDir` (all `Directories_0.1`). It uses the shared Snowflake connection object (`tDBConnection_1`), not `LEGACY_DW_0.1` variables — no `LEGACY_DW_` entries appear in `context_vars_referenced`.
- **Hardcoded values found:** `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, `tFileDelete_1.DIRECTORY`/`PATH` — the same `C:/Talend-Studio-20211109_1610-V8.0.1/...` machine-specific paths seen in most jobs. Note that `tSetKeystore_1`'s truststore path also appears among the project-wide hardcoded findings for this job.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tPrejob` / `tParallelize` | Job-flow control (see `job_Address_Text_Load.md`). |
| `tFileList` | Lists files in a folder to loop over (see `job_Address_Text_Load.md`). |
| `tFileInputDelimited` | Reads a delimited text file row by row (see `job_Address_Text_Load.md`). |
| `tMap` | Maps/transforms input columns to output columns (see `job_Address_Text_Load.md`). |
| `tDBOutput` / `tSnowflakeOutput` | Writes rows into a Snowflake table (see `job_Address_Text_Load.md`). |
| `tDBRow` / `tSnowflakeRow` | Runs a single SQL statement against Snowflake (see `job_Address_Text_Load.md`). |
| `tJava` / `tJavaRow` | Custom Java code snippets (see `job_Address_Text_Load.md`). |
| `tFileArchive` | Zips a file into an archive location (see `job_Address_Text_Load.md`). |
| `tFileDelete` | Deletes a file from disk (see `job_Address_Text_Load.md`). |
| `tSetKeystore` | Configures the SSL keystore for the Snowflake connection (see `job_Address_Text_Load.md`). |

## Issues observed

- **File encoding is US-ASCII**, not ISO-8859-15 like `Address_Text_Load` — worth confirming this is intentional for PDC data.
- **The `TRUNCATE` statement is unqualified** (`PDC_TXT` rather than `LIQUID_STAGING.PDC_TXT`), relying on the Snowflake connection's default schema — same pattern flagged in `CBR_Metro2_Accounts_Table_Text_Load`.
- **No `tDie`/`tWarn` on the merge step** — a failed merge surfaces only as a generic Talend error.
- **Standard hardcoded machine-specific paths** present across `tFileInputDelimited_1`, `tFileArchive_1`, `tFileDelete_1`, and `tSetKeystore_1` — the same project-wide pattern.
