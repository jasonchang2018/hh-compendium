# Talend Job: Master_Special_Info_Text_Load

## Overview

This job loads "special info" account flags (mail-return flags, web arrangement flags, last call date, and a couple of IDs) from a shared folder into Snowflake. It follows the project's standard load pattern: truncate the staging table, read the newest matching source file, load into staging, merge into the permanent table via a stored procedure, then archive and delete the source file.

## Detail table

| Field | Value |
|---|---|
| Job name | Master_Special_Info_Text_Load |
| Version | 0.1 |
| Project | LATITUDE |
| Author | jmach@harriscollect.com |
| Created | 2024-11-27T09:56:03.432-0800 |
| Last Modified | 2025-10-01T10:09:11.453-0700 |

## Step-by-step data flow

1. **Set up.** `tPrejob_1` starts the job; `tJava_2` appends today's date to `context.archiveDir` and opens a log file; `tSetKeystore_1` configures the SSL client keystore; `tDBConnection_1` opens the Snowflake connection.
2. **Find the file.** `tFileList_1` lists files in `context.sourceDir` (skipping `.txt` files); the match becomes `context.filePath` (`tJava_1`).
3. **Read and reshape.** `tFileInputDelimited_1` reads the file using the repository schema "invmgmt" — pipe-delimited (`|~|`/`|$|`), US-ASCII encoding, header row present. `tMap_1` maps its columns (`number`, `LastMailReturnFlagDate`, `WEBArrangementFlag`, `lastcalldate`, `id`) onto the target schema (`NUMBER`, `LASTMAILRETURNFLAGDATE`, `WEBARRANGEMENTFLAG`, `LASTCALLDATE`, `ID`, plus `LOAD_DT`).
4. **Load staging.** The mapped rows flow directly into `tDBOutput_1`, which inserts them into `MASTER_SPECIAL_INFO_TXT` (no row counter on this path).
5. **Merge and clean up — in parallel.** `tParallelize_1` splits into:
   - **Merge branch:** `tDBRow_2` runs `CALL MERGE_TXT_INTO_MASTER_SPECIAL_INFO();`. No `tDie`/`tWarn` check follows it.
   - **Cleanup branch:** the source file is listed again, archived (`tFileArchive_1`), then separately listed and deleted (`tFileDelete_1`, `FAILON` false).
6. **Staging truncate.** `tDBRow_1` runs `TRUNCATE TABLE MASTER_SPECIAL_INFO_TXT;` and, on success, triggers `tFileList_1` — this is wired as an independent starting subjob rather than chained explicitly before step 2 in this metadata, but functionally runs the truncate before the file is processed.

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> SetLog["tJava_2<br/>Set archive path + start log"] --> Keystore["tSetKeystore_1"] --> Connect["tDBConnection_1"]
    Truncate["tDBRow_1<br/>TRUNCATE MASTER_SPECIAL_INFO_TXT"] --> ListFiles1["tFileList_1<br/>Find source file"]
    ListFiles1 -->|iterate| SetPath["tJava_1"] --> ReadFile["tFileInputDelimited_1"]
    ListFiles1 --> Parallel["tParallelize_1"]
    ReadFile -->|flow| Map["tMap_1<br/>Map columns"] --> Insert["tDBOutput_1<br/>INSERT into staging"]
    Parallel --> Merge["tDBRow_2<br/>CALL MERGE_TXT_INTO_MASTER_SPECIAL_INFO()"] & ListFiles2["tFileList_2"]
    ListFiles2 -->|iterate| SetPath2["tJava_3"] --> Archive["tFileArchive_1"]
    ListFiles2 --> ListFiles3["tFileList_3"]
    ListFiles3 -->|iterate| SetPath3["tJava_4"] --> Delete["tFileDelete_1"]
```

## Settings tables

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.filePath` | Reads whichever file `tFileList_1` found. |
| Schema | Repository schema "invmgmt" | Uses a shared, pre-defined column layout. |
| FIELDSEPARATOR / ROWSEPARATOR | `\|~\|` / `\|$\|` | The project's standard pipe-delimited format. |
| CSVROWSEPARATOR | `\r\n` | Underlying line ending within each row. |
| ENCODING | US-ASCII | Plain ASCII, not ISO-8859-15. |
| DIE_ON_ERROR | false | A malformed row is rejected rather than failing the job (rejects captured via the `customer` reject schema). |

### Target: `tDBOutput_1`

| Setting | Value | What it means |
|---|---|---|
| Table | MASTER_SPECIAL_INFO_TXT | Staging table written to. |
| Output action | INSERT | Adds rows only. |
| Table action | NONE | Structure untouched — truncation is the separate `tDBRow_1` step. |

### Merge step: `tDBRow_2`

| Setting | Value | What it means |
|---|---|---|
| Query | `CALL MERGE_TXT_INTO_MASTER_SPECIAL_INFO();` | Snowflake stored procedure folding staged rows into the permanent table. Body not visible in this metadata. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none — no `tRunJob` links found.
- **Context variables used:** `context.sourceDir`, `context.archiveDir`, `context.filePath`, `context.fileName`, `context.logDir`, `context.keystorePath` (all `Directories_0.1`).
- **Snowflake connection:** uses the shared connection object, not `LEGACY_DW_*` context variables directly.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tPrejob` / `tParallelize` | Setup-before-main-flow, and concurrent branches (see `job_Address_Text_Load.md`). |
| `tFileList` | Lists files in a folder to loop over (see `job_Address_Text_Load.md`). |
| `tFileInputDelimited` | Reads a delimited text file row by row (see `job_Address_Text_Load.md`). |
| `tMap` | Maps/transforms columns (see `job_Address_Text_Load.md`). |
| `tSnowflakeOutput` (`tDBOutput`) | Writes rows into Snowflake (see `job_Address_Text_Load.md`). |
| `tSnowflakeRow` (`tDBRow`) | Runs a single SQL statement — `TRUNCATE` and `CALL <procedure>` here (see `job_Address_Text_Load.md`). |
| `tJava` | Custom Java code for small tasks (see `job_Address_Text_Load.md`). |
| `tFileArchive` | Zips a file into an archive location (see `job_Address_Text_Load.md`). |
| `tFileDelete` | Deletes a file from disk (see `job_Address_Text_Load.md`). |
| `tSetKeystore` | Configures the SSL keystore for the Snowflake connection (see `job_Address_Text_Load.md`). |

## Issues observed

- **Hardcoded machine-specific paths**: `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, `tFileDelete_1.DIRECTORY`/`PATH`, and `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE` are all fixed `C:/Talend-Studio-20211109_1610-V8.0.1/...` or `C:/clientTrustStore.trustStore` paths rather than context variables — the same pattern flagged project-wide.
- **No row counter (`tFlowMeter`)** on the load path — load volume for this job isn't captured in the same monitoring stream as jobs that do have one.
- **No explicit error handling on the merge step** — no `tDie`/`tWarn` reacting to whether `MERGE_TXT_INTO_MASTER_SPECIAL_INFO()` succeeded.
- **The merge procedure's own logic is outside Talend** — its body isn't part of this metadata.
