# Talend Job: cmi_renkim_ReturnHistory_Text_Load

## Overview

This job loads returned-mail history records (an NCOA/address-move tracking feed — original address, forwarding/NCOA address, letter address, move type, return reason, and processing result) into Snowflake. It follows the standard truncate → load → merge → archive/delete pattern used across the project's text-load jobs.

## Detail table

| Field | Value |
|---|---|
| Job name | cmi_renkim_ReturnHistory_Text_Load |
| Version | 0.1 |
| Project | LATITUDE |
| Author | jmach@harriscollect.com |
| Created | 2024-11-06T10:21:21.321-0800 |
| Last Modified | 2025-09-29T21:40:53.679-0700 |

## Step-by-step data flow

1. **Set up.** `tPrejob_1` starts the job; `tJava_2` sets the dated archive path and opens the log; `tSetKeystore_1` configures the SSL keystore; `tDBConnection_1` opens the Snowflake connection.
2. **Empty the staging table.** `tDBRow_1` runs `TRUNCATE TABLE CMI_RENKIM_RETURNHISTORY_TXT;` — no schema qualifier (see Issues observed).
3. **Find the file.** `tFileList_1` lists files in `context.sourceDir` (skipping `.txt`) with no explicit sort order (`ORDER_BY_NOTHING`=true). The match becomes `context.filePath` (`tJava_1`).
4. **Read and reshape.** `tFileInputDelimited_1` reads the file as pipe-delimited (`|~|`/`|$|`), US-ASCII encoded, with a header row. `tMap_1` maps the file's ~30 columns (record ID, dates, original/NCOA/letter addresses, e-notice fields, return reason, process result, PDF URL) plus `LOAD_DT` onto the `CMI_RENKIM_RETURNHISTORY_TXT` schema.
5. **Load staging.** The mapped rows flow directly into `tDBOutput_1` (no row-counter component here), which inserts them into the staging table.
6. **Merge and cleanup — in parallel.** `tParallelize_1` splits into:
   - **Merge branch:** `tDBRow_2` runs `CALL MERGE_TXT_INTO_CMI_RENKIM_RETURNHISTORY();`. No `tDie`/`tWarn` reacts to the result.
   - **Cleanup branch:** the file is listed again, archived as a `.zip` into `context.archiveDir` (`tFileArchive_1`), and deleted (`tFileDelete_1`, with `FAILON`=true).

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> SetLog["tJava_2<br/>Set archive path + start log"] --> Keystore["tSetKeystore_1"] --> Connect["tDBConnection_1"]
    Truncate["tDBRow_1<br/>TRUNCATE CMI_RENKIM_RETURNHISTORY_TXT"] --> ListFiles1["tFileList_1<br/>Find first file (no sort)"]
    ListFiles1 -->|iterate| SetPath["tJava_1"] --> ReadFile["tFileInputDelimited_1"]
    ListFiles1 --> Parallel["tParallelize_1"]
    ReadFile -->|flow| Map["tMap_1"] --> Insert["tDBOutput_1<br/>INSERT into staging"]
    Parallel --> ListFiles2["tFileList_2"] & Merge["tDBRow_2<br/>CALL MERGE_TXT_INTO_CMI_RENKIM_RETURNHISTORY()"]
    ListFiles2 -->|iterate| SetPath2["tJava_3"] --> Archive["tFileArchive_1"]
    ListFiles2 --> ListFiles3["tFileList_3"]
    ListFiles3 -->|iterate| SetPath3["tJava_4"] --> Delete["tFileDelete_1"]
```

## Settings tables

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.filePath` | Reads whichever file `tFileList_1` just found. |
| FIELDSEPARATOR / ROWSEPARATOR | `\|~\|` / `\|$\|` | Standard pipe-delimited format. |
| CSVROWSEPARATOR | `\r\n` | Fallback row separator (inert since `CSV_OPTION` is false). |
| ENCODING | US-ASCII | Matches `Carrier_Text_Load`/`Insurance_Text_Load`. |
| SCHEMA_REJECT | repository schema `"customer"` | Mismatched — same copy-paste artifact seen in `Carrier_Text_Load`, `Result_Table_Text_Load`, and `cmi_Dialer_Plan_History_Table_Text_Load`. |
| ORDER_BY_NOTHING (on `tFileList_1`) | true | No sort order applied — whichever file the filesystem returns first is used, same as `Result_Table_Text_Load`. |
| EXCLUDEFILEMASK (on `tFileList_1`) | `*.txt` | `.txt` files skipped. |

### Target: `tDBOutput_1`

| Setting | Value | What it means |
|---|---|---|
| Table | CMI_RENKIM_RETURNHISTORY_TXT | Loads rows into this table. |
| Output action | INSERT | Adds rows only. |
| Table action | NONE | No table create/drop/truncate here. |

### Truncate & merge: `tDBRow_1` / `tDBRow_2`

| Setting | Value | What it means |
|---|---|---|
| Query (`tDBRow_1`) | `TRUNCATE TABLE CMI_RENKIM_RETURNHISTORY_TXT;` | Empties staging — no schema prefix, relying on the connection's default schema, same pattern as `Result_Table_Text_Load`. |
| Query (`tDBRow_2`) | `CALL MERGE_TXT_INTO_CMI_RENKIM_RETURNHISTORY();` | Folds staged rows into the permanent table; naming matches the table name, unlike `Result_Table_Text_Load`'s mismatch. |

### Cleanup: `tFileDelete_1`

| Setting | Value | What it means |
|---|---|---|
| FAILON | true | A failed delete fails the job — matches `DeskChangeHistory_Text_Load`/`Users_Text_Load`. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none found — no `tRunJob` links.
- **Context variables used:** `context.sourceDir`, `context.archiveDir`, `context.filePath`, `context.fileName`, `context.logDir`, `context.keystorePath` (all `Directories_0.1`). Uses the shared Snowflake connection object, not `LEGACY_DW_0.1` directly.
- **Hardcoded values found:** `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, `tFileDelete_1.DIRECTORY`/`PATH`, and `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE` — the same fixed Windows paths seen project-wide.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tPrejob` / `tParallelize` | Job-flow control (see `job_Address_Text_Load.md`). |
| `tFileList` | Lists files to loop over (see `job_Address_Text_Load.md`). |
| `tFileInputDelimited` | Reads a delimited text file (see `job_Address_Text_Load.md`). |
| `tMap` | Maps/transforms columns (see `job_Address_Text_Load.md`). |
| `tDBOutput` / `tSnowflakeOutput` | Writes rows to Snowflake (see `job_Address_Text_Load.md`). |
| `tDBRow` / `tSnowflakeRow` | Runs a single SQL statement (see `job_Address_Text_Load.md`). |
| `tJava` | Custom Java code blocks (see `job_Address_Text_Load.md`). |
| `tFileArchive` | Zips a file into an archive location (see `job_Address_Text_Load.md`). |
| `tFileDelete` | Deletes a file from disk (see `job_Address_Text_Load.md`). |
| `tSetKeystore` | Configures the SSL keystore for Snowflake (see `job_Address_Text_Load.md`). |

## Issues observed

- **The truncate statement has no schema qualifier** (`TRUNCATE TABLE CMI_RENKIM_RETURNHISTORY_TXT;`), same category of finding as `Result_Table_Text_Load` and `cmi_Dialer_Plan_History_Table_Text_Load` — relies on the connection's default schema rather than being explicit.
- **File is picked with no sort order** (`ORDER_BY_NOTHING`=true) rather than by last-modified date — same finding as `Result_Table_Text_Load`; if more than one matching file is present, which one is processed is effectively arbitrary.
- **Reject-schema mismatch** ("customer" reject schema) — same copy-paste artifact flagged in `Carrier_Text_Load`, `Result_Table_Text_Load`, and `cmi_Dialer_Plan_History_Table_Text_Load` — four jobs now show this same leftover reference, reinforcing that they share a common template origin.
- **No row-counter (`tFlowMeter`) between the map and the load**, unlike several peer jobs.
- **No merge-result checking** — no `tDie`/`tWarn` reacts to the merge outcome.
- **Hardcoded, machine-specific paths** exist alongside the parameterized ones — the same project-wide pattern.
