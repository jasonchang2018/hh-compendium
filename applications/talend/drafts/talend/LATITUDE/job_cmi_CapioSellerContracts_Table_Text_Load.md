# Talend Job: cmi_CapioSellerContracts_Table_Text_Load

## Overview

This job loads Capio seller-contract reference data (seller name, contract ID/name/description, bid and purchase dates, placement phase, customer, and an attorney-general flag) from a shared folder into Snowflake, following the project's standard truncate-load-merge-archive pattern (see `job_Address_Text_Load.md`). Unlike most peers, it is configured to fail immediately (`DIE_ON_ERROR: true`) if the source file can't be parsed, rather than continuing quietly. It has no scheduling information in this metadata — something outside Talend decides when it runs.

## Detail table

| Field | Value |
|---|---|
| Job name | cmi_CapioSellerContracts_Table_Text_Load |
| Version | 0.1 |
| Project | LATITUDE |
| Author | jmach@harriscollect.com |
| Created | 2024-10-29T12:47:43.495-0700 |
| Last Modified | 2025-09-29T10:31:47.689-0700 |

## Step-by-step data flow

1. **Set up.** `tPrejob_1` starts the job; `tJava_3` appends today's date to `context.archiveDir` and opens a log file; `tSetKeystore_1` configures the SSL client keystore; `tDBConnection_1` opens the Snowflake connection.
2. **Empty the staging table.** In a separate, parallel start point, `tDBRow_1` runs `TRUNCATE TABLE CMI_CAPIOSELLERCONTRACTS_TXT;`.
3. **Find and read the file.** `tFileList_1` lists files in `context.sourceDir` (skipping `.txt`); `tJava_1` captures the found path into `context.filePath`; `tFileInputDelimited_1` reads it as a pipe-delimited, US-ASCII-encoded file (using the repository schema named `capslr`) with a header row. This component has `DIE_ON_ERROR` set to `true` — a malformed row here fails the job rather than being skipped or logged.
4. **Transform and load.** `tMap_1` maps the file's columns (ID, seller name, contract ID/name/description, file bid date, purchase date, placement phase, customer, MN attorney general flag) onto the `CMI_CAPIOSELLERCONTRACTS_TXT` schema, adding `LOAD_DT`. The mapped rows go directly into `tDBOutput_1`, which inserts them into Snowflake.
5. **Merge and clean up — in parallel.** `tParallelize_1` splits into two branches once the file has been listed:
   - **Merge branch:** `tDBRow_2` calls `CALL MERGE_TXT_INTO_CMI_CAPIOSELLERCONTRACTS();`.
   - **Cleanup branch:** the source file is listed again and archived (`tFileArchive_1`, zipped into `context.archiveDir`); it's also listed a third time and deleted (`tFileDelete_1`).

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> SetLog["tJava_3<br/>Set archive path + start log"] --> Keystore["tSetKeystore_1"] --> Connect["tDBConnection_1"]
    Truncate["tDBRow_1<br/>TRUNCATE CMI_CAPIOSELLERCONTRACTS_TXT"] --> ListFiles1["tFileList_1<br/>Find newest source file"]
    ListFiles1 -->|iterate| SetPath["tJava_1<br/>Capture file path"]
    ListFiles1 --> Parallel["tParallelize_1"]
    SetPath --> ReadFile["tFileInputDelimited_1<br/>Read pipe-delimited file<br/>(DIE_ON_ERROR=true)"]
    ReadFile -->|flow| Map["tMap_1<br/>Map columns"] --> Insert["tDBOutput_1<br/>INSERT into staging"]
    Parallel --> Merge["tDBRow_2<br/>CALL MERGE_TXT_INTO_CMI_CAPIOSELLERCONTRACTS()"] & ListFiles2["tFileList_2"]
    ListFiles2 -->|iterate| SetPath2["tJava_2"] --> Archive["tFileArchive_1<br/>Zip into archive dir"]
    ListFiles2 --> ListFiles3["tFileList_3"]
    ListFiles3 -->|iterate| SetPath3["tJava_4"] --> Delete["tFileDelete_1<br/>Delete source file"]
```

## Settings tables

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.filePath` | Reads whichever file `tFileList_1` just found. |
| FIELDSEPARATOR / ROWSEPARATOR | `\|~\|` / `\|$\|` | The project's standard pipe-delimited format. |
| HEADER | 1 | First line is a header, not data. |
| ENCODING | US-ASCII | Plain ASCII, not ISO-8859-15. |
| DIE_ON_ERROR | **true** | If a row fails to parse against the schema, the job stops immediately rather than continuing — differs from most peers (e.g., `Address_Text_Load`, `Phones_Master_Table_Text_Load`), which set this to `false`. |
| SCHEMA:REPOSITORY_SCHEMA_TYPE | `capslr` (repository schema) | Uses a centrally-defined column layout. |
| EXCLUDEFILEMASK (on `tFileList_1`) | `*.txt` | `.txt` files are skipped. |

### Target: `tDBOutput_1`

| Setting | Value | What it means |
|---|---|---|
| Table | CMI_CAPIOSELLERCONTRACTS_TXT | Loads the staging copy of the seller-contracts table. |
| Output action | INSERT | Adds rows only. |
| Table action | NONE | Truncation is handled separately by `tDBRow_1`. |

### Merge step: `tDBRow_2`

| Setting | Value | What it means |
|---|---|---|
| Query | `CALL MERGE_TXT_INTO_CMI_CAPIOSELLERCONTRACTS();` | Folds staged rows into the permanent table; its own logic lives in Snowflake. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none found — no `tRunJob` links.
- **Context variables used:** `context.sourceDir`, `context.archiveDir`, `context.filePath`, `context.fileName`, `context.logDir`, `context.keystorePath` (all `Directories_0.1`).
- **LEGACY_DW usage:** none — this job uses the shared Snowflake connection object, not `LEGACY_DW_0.1` variables directly.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tPrejob` / `tParallelize` | Job-flow control. (see `job_Address_Text_Load.md`) |
| `tFileList` | Lists files in a folder so the job can loop over them. (see `job_Address_Text_Load.md`) |
| `tFileInputDelimited` | Reads a delimited text file row by row. (see `job_Address_Text_Load.md`) |
| `tMap` | Maps/transforms columns from input to output. (see `job_Address_Text_Load.md`) |
| `tDBOutput` / `tSnowflakeOutput` | Writes rows into a Snowflake table. (see `job_Address_Text_Load.md`) |
| `tDBRow` / `tSnowflakeRow` | Runs a single SQL statement — used here for `TRUNCATE` and `CALL <procedure>`. (see `job_Address_Text_Load.md`) |
| `tJava` | A small block of custom Java code. (see `job_Address_Text_Load.md`) |
| `tFileArchive` | Compresses a file into a `.zip` and archives it. (see `job_Address_Text_Load.md`) |
| `tFileDelete` | Deletes a file from disk. (see `job_Address_Text_Load.md`) |
| `tSetKeystore` | Configures the SSL keystore for the Snowflake connection. (see `job_Address_Text_Load.md`) |

## Issues observed

- **`DIE_ON_ERROR` is `true` on the file reader**, unlike most peer "Text Load" jobs. A single malformed row in the source file will stop the entire job rather than being logged and skipped — worth confirming this is intentional given how small and reference-like this dataset is (contract metadata, not transactional data).
- **No row counter (`tFlowMeter`)** between `tMap_1` and `tDBOutput_1`, unlike some peer jobs.
- **No explicit error handling on the merge step** (no `tDie`/`tWarn`), same as most peers.
- **The merge procedure's own logic is outside Talend**, same caveat as every other job that calls a `MERGE_TXT_INTO_*` procedure.
