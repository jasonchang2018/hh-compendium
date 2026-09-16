# Talend Job: LetterRequest_Table_Text_Load

## Overview

This job loads letter-request records (collection letters queued or sent for accounts — letter type, due date, amount due, processing status, and related IDs) into Snowflake. It follows the standard LATITUDE text-load pattern exactly: truncate the staging table, read and map the source file, insert into staging, merge into the permanent table, then archive and delete the source file.

## Detail table

| Field | Value |
|---|---|
| Job name | LetterRequest_Table_Text_Load |
| Version | 0.1 |
| Project | LATITUDE |
| Author | jmach@harriscollect.com |
| Created | 2024-10-24T08:48:53.448-0700 |
| Last Modified | 2025-09-30T19:55:44.115-0700 |

## Step-by-step data flow

1. **Set up.** `tPrejob_1` triggers `tJava_2`, which appends today's date to `context.archiveDir` and opens a log file; this chains into `tSetKeystore_1` and `tDBConnection_1`.
2. **Empty the staging table.** `tDBRow_1` runs `TRUNCATE TABLE LETTERREQUEST_TXT;` (again, no explicit schema prefix — see Issues observed).
3. **Find the file.** `tFileList_1` lists files in `context.sourceDir` (skipping `*.txt`), with no explicit sort order (`ORDER_BY_NOTHING: true`).
4. **Read and reshape the file.** `tFileInputDelimited_1` reads the file as pipe-delimited (`|~|`/`|$|`), US-ASCII encoded, with a header row, covering letter request ID, account ID, letter/customer codes, due date, amount due, processing method, 24 "SifPmt" fields (payment-schedule-related), and delivery flags. `tMap_1` maps these onto the `LETTERREQUEST_TXT` schema, adding `LOAD_DT`.
5. **Load staging.** Mapped rows flow directly into `tDBOutput_1` (no row-counter component on this path), inserting into `LETTERREQUEST_TXT`.
6. **Merge and clean up — in parallel.** Once the file-list subjob completes, `tParallelize_1` splits into: `tDBRow_2` calling `CALL MERGE_TXT_INTO_LETTERREQUEST();`, and a file-listing chain (`tFileList_2` → archive via `tFileArchive_1`; then `tFileList_3` → delete via `tFileDelete_1`).

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> SetLog["tJava_2<br/>Set archive path + start log"] --> Keystore["tSetKeystore_1"] --> Connect["tDBConnection_1"]
    Truncate["tDBRow_1<br/>TRUNCATE LETTERREQUEST_TXT"] --> ListFiles1["tFileList_1<br/>Find source file"]
    ListFiles1 -->|iterate| SetPath["tJava_1"] --> ReadFile["tFileInputDelimited_1"]
    ListFiles1 --> Parallel["tParallelize_1"]
    ReadFile -->|flow| Map["tMap_1"] --> Insert["tDBOutput_1<br/>INSERT into LETTERREQUEST_TXT"]
    Parallel --> Merge["tDBRow_2<br/>CALL MERGE_TXT_INTO_LETTERREQUEST()"] & ListFiles2["tFileList_2"]
    ListFiles2 -->|iterate| SetPath3["tJava_3"] --> Archive["tFileArchive_1"]
    ListFiles2 --> ListFiles3["tFileList_3"]
    ListFiles3 -->|iterate| SetPath4["tJava_4"] --> Delete["tFileDelete_1"]
```

## Settings tables

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.filePath` | Reads whichever file `tFileList_1` just found. |
| FIELDSEPARATOR / ROWSEPARATOR | `\|~\|` / `\|$\|` | Standard project pipe-delimited format. |
| HEADER | 1 | First line is a header. |
| ENCODING | US-ASCII | Plain ASCII text. |

### Target: `tDBOutput_1`

| Setting | Value | What it means |
|---|---|---|
| Table | LETTERREQUEST_TXT | Staging table for letter requests. |
| Output action | INSERT | Adds rows only — the merge step handles updates. |
| Table action | NONE | Truncation handled separately by `tDBRow_1`. |

### Merge step: `tDBRow_2`

| Setting | Value | What it means |
|---|---|---|
| Query | `CALL MERGE_TXT_INTO_LETTERREQUEST();` | Snowflake procedure that folds staged rows into the permanent `LETTERREQUEST` table. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none found — no `tRunJob` links.
- **Context variables used:** `context.sourceDir`, `context.archiveDir`, `context.filePath`, `context.fileName`, `context.logDir`, `context.keystorePath` (all `Directories_0.1`). Uses the shared Snowflake connection object, not `LEGACY_DW_*` variables directly.
- **Hardcoded values found:** `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, `tFileDelete_1.DIRECTORY`/`PATH`, and `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE` are fixed Windows/local paths rather than context variables.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tPrejob` / `tParallelize` | Setup-before-main-start, concurrent branches (see job_Address_Text_Load.md). |
| `tFileList` | Lists files for the job to loop over (see job_Address_Text_Load.md). |
| `tFileInputDelimited` | Reads a delimited text file (see job_Address_Text_Load.md). |
| `tMap` | Maps/transforms columns (see job_Address_Text_Load.md). |
| `tDBOutput` / `tSnowflakeOutput` | Writes rows into Snowflake (see job_Address_Text_Load.md). |
| `tDBRow` / `tSnowflakeRow` | Runs a single SQL statement (see job_Address_Text_Load.md). |
| `tJava` | Custom Java code block (see job_Address_Text_Load.md). |
| `tFileArchive` | Zips a file into an archive location (see job_Address_Text_Load.md). |
| `tFileDelete` | Deletes a file from disk (see job_Address_Text_Load.md). |
| `tSetKeystore` | Configures the SSL keystore for the Snowflake connection (see job_Address_Text_Load.md). |

## Issues observed

- **The staging truncate doesn't qualify its schema** (`TRUNCATE TABLE LETTERREQUEST_TXT;` with no `LIQUID_STAGING.` prefix) — same pattern seen in `Customer_Table_Text_Load`; likely relies on the connection's default schema, but worth confirming.
- **No row-count logging** — no `tFlowMeter` component between `tMap_1` and `tDBOutput_1`, unlike some peer jobs.
- **`tFileDelete_1.FAILON` is `false`** here, meaning a failed delete of the source file won't fail the job — worth being aware of if source files are unexpectedly reprocessed.
- **Several hardcoded, machine-specific paths** exist — see Dependencies & configuration.
- **The merge procedure's own logic is outside Talend** and not visible in this metadata.
