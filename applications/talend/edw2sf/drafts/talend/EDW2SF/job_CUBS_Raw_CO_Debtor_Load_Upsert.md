# Talend Job: CUBS_Raw_CO_Debtor_Load_Upsert

## Overview

Loads CUBS collections debtor master-file extracts for the CO site (per-debtor demographic and account fields — name, address, phone, client, agency-code, trip/IOC/letter-cycle flags, etc., per the `CUBS-DEBTOR-CO` repository schema) from a local drop directory into Snowflake. Each file's rows are encrypted (PII fields) in flight, flattened into a generic `COL1`-`COL500` staging schema, and loaded into `CUBS_DEBTOR_RAW_CO_CURRENT` (`UPSERT` output action). Once every file in the batch has loaded, a single `MERGE` statement inserts any not-already-present rows from that staging table into the cross-site raw table `EDWPRODHH.STAGING.CUBS_DEBTOR_RAW`, after which processed source files are archived (as `.tar.gz`) and then deleted from the source directory.

## Detail table

| Field | Value |
|---|---|
| Job name | CUBS_Raw_CO_Debtor_Load_Upsert |
| Version | 0.4 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2024-07-11T11:58:50.212-0700 |
| Last Modified | 2025-09-24T11:09:09.267-0700 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` →(`OnComponentOk`)→ `tJava_4` opens a per-run log file at `context.logDir + context.currentLogon + "_" + jobName + "_" + <timestamp> + ".log"` and redirects `System.out` to it (code truncated at 253 characters in the extracted metadata; remainder not recoverable from this JSON) →(`OnComponentOk`)→ `tDBConnection_1` opens the job's Snowflake connection.

**Main subjob — file-load loop (runs once per file in `context.sourceRoot`):**

1. `tFileList_1` lists files in `context.sourceRoot` (files only, no subdirectories, ordered by... nothing — `ORDER_BY_NOTHING=true`, so no explicit sort order is applied; `EXCLUDEFILEMASK="*.txt"` is configured but no `IFEXCLUDE` flag is present in this component's captured parameters to confirm it's active).
2. `tFileList_1` →(`ITERATE`)→ `tJava_3` copies the current iteration's file path/name/directory from `globalMap` into `context.currentFile` / `context.fileName` / `context.filePath` (code truncated in metadata after the `System.out.println("Proc...` line).
3. →(`ITERATE`)→ `tFileInputDelimited_1` reads the file as delimited text using repository schema `CUBS-DEBTOR-CO` (462 business columns), with `FIELDSEPARATOR="\t"`, `ROWSEPARATOR="\n"`, `HEADER=1`, `ENCODING="ISO-8859-15"` all **hardcoded literals** on this component (not context variables — see Issues observed); `DIE_ON_ERROR=false`. No `SCHEMA_REJECT` parameter is present in this component's metadata at all (unlike the sibling CHI job).
4. →(`FLOW`, link `row1`)→ `tDataEncrypt_1` AES-encrypts the row (secret type, secret key, and password all `***REDACTED***` in source metadata). Its own schema carries only 436 of the 462 upstream columns — see Issues observed.
5. →(`FLOW`, link `row2`)→ `tMap_1` maps the row down to a generic 502-column output shape: `FILENAME`, `FILEDATE`, `COL1`...`COL500` (`DIE_ON_ERROR=true`, so a mapping failure fails the job).
6. →(`FLOW`, link `co`)→ `tDBOutput_2` (`tSnowflakeOutput`) writes to table `CUBS_DEBTOR_RAW_CO_CURRENT` with `outputAction=UPSERT`, `tableAction=NONE`. (No `tFlowMeter` row-counting component is present in this job, unlike the CHI sibling — see Issues observed.)
7. →(`OnComponentOk`)→ `tFileArchive_1` archives the just-processed file to `context.archiveDir + "/" + <today's date CCYYMMDD> + "/" + context.fileName + ".tar.gz"`.

**After the entire file-load loop subjob completes successfully** (not per file): `tFileList_1` →(`OnSubjobOk`)→ `tDBRow_2` (`tSnowflakeRow`) runs a single `MERGE` from `STAGING.CUBS_DEBTOR_RAW_CO_CURRENT` into `EDWPRODHH.STAGING.CUBS_DEBTOR_RAW`, matching on `FILEDATE` + `COL3`, inserting only rows with `WHEN NOT MATCHED` (no `WHEN MATCHED` clause — see Issues observed).

**Cleanup loop (runs after the merge, once per file in `context.sourceRoot` again):**

8. `tDBRow_2` →(`OnSubjobOk`)→ `tFileList_2` re-lists files in `context.sourceRoot` →(`ITERATE`)→ `tJava_2` re-sets `context.currentFile`/`fileName`/`filePath` from this second listing →(`ITERATE`)→ `tFileDelete_1` deletes `context.currentFile` →(`OnComponentOk`)→ `tJava_1` logs the delete status/path/error from `globalMap`.

**Teardown subjob:** `tPostjob_1` →(`OnComponentOk`)→ `tDBClose_1` closes the Snowflake connection.

```mermaid
flowchart TD
    Prejob["tPrejob_1"] -->|OnComponentOk| OpenLog["tJava_4<br/>Open per-run log file"]
    OpenLog -->|OnComponentOk| Connect["tDBConnection_1<br/>Open Snowflake connection"]

    FileList1["tFileList_1<br/>List files in sourceRoot"] -->|Iterate| SetVars1["tJava_3<br/>Set currentFile/fileName/filePath"]
    SetVars1 -->|Iterate| ReadCSV["tFileInputDelimited_1<br/>Read CSV (schema: CUBS-DEBTOR-CO;<br/>hardcoded tab/LF/header/encoding)"]
    ReadCSV -->|row1| Encrypt["tDataEncrypt_1<br/>AES encrypt (436 of 462 cols)"]
    Encrypt -->|row2| Map["tMap_1<br/>Flatten to FILENAME/FILEDATE/COL1-COL500"]
    Map -->|co| Output["tDBOutput_2<br/>UPSERT into CUBS_DEBTOR_RAW_CO_CURRENT"]
    Output -->|OnComponentOk| Archive["tFileArchive_1<br/>Archive file to .tar.gz"]

    FileList1 -->|OnSubjobOk| Merge["tDBRow_2<br/>MERGE staging → EDWPRODHH.STAGING.CUBS_DEBTOR_RAW<br/>(INSERT-only, ON FILEDATE+COL3)"]

    Merge -->|OnSubjobOk| FileList2["tFileList_2<br/>Re-list files in sourceRoot"]
    FileList2 -->|Iterate| SetVars2["tJava_2<br/>Set currentFile/fileName/filePath"]
    SetVars2 -->|Iterate| Delete["tFileDelete_1<br/>Delete currentFile"]
    Delete -->|OnComponentOk| LogDelete["tJava_1<br/>Log delete status"]

    Postjob["tPostjob_1"] -->|OnComponentOk| Close["tDBClose_1<br/>Close Snowflake connection"]
```

## Settings tables

### Source listing: `tFileList_1` / `tFileList_2`

| Setting | Value | What it means |
|---|---|---|
| DIRECTORY | `context.sourceRoot` | Both loops (load and cleanup) scan the same source directory. |
| LIST_MODE | `FILES` | Only files, no subdirectories (`INCLUDSUBDIR=false`). |
| ORDER_BY_NOTHING | `true` | No explicit sort order is applied to the file list (unlike the CHI sibling, which sorts by modified date ascending). |
| EXCLUDEFILEMASK | `"*.txt"` | An exclusion mask is configured, but no `IFEXCLUDE`/enable flag was present in this component's captured parameters to confirm it's active. |

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.currentFile` | The current file from `tFileList_1`'s iteration. |
| FIELDSEPARATOR | `"\t"` | Hardcoded tab-delimited, **not** a context variable — differs from the CHI sibling, which externalizes this to `context.EXPORT_DEBTOR_FieldSeparator`. |
| ROWSEPARATOR | `"\n"` | Hardcoded, same pattern as above. |
| HEADER | `1` | Hardcoded 1 header row. |
| ENCODING | `"ISO-8859-15"` | Hardcoded. |
| SCHEMA (main) | Repository schema `CUBS-DEBTOR-CO` | 462 business columns (`LOGON` through `CELL_PHONE_F83`: demographic, client, agency, trip/IOC/letter-cycle fields) plus `errorCode`/`errorMessage` reject columns. |
| SCHEMA_REJECT | Not present | No `SCHEMA_REJECT` repository-schema parameter appears in this component's captured metadata at all — unlike the CHI sibling, which has one (mismatched to an `HH`-labeled schema). |
| DIE_ON_ERROR | `false` | Malformed rows don't fail the job... |
| Reject flow | Not wired | ...but no connection in this job routes rejected rows anywhere — they are silently dropped. |
| TEMP_DIR | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace"` | Hardcoded developer-workstation path (see `hardcoded_path_findings`). |

### Transform: `tDataEncrypt_1`

| Setting | Value | What it means |
|---|---|---|
| CRYPTO_METHOD | `AES` | Symmetric encryption of column values. |
| SECRET_TYPE / SECRET_KEY / PASSWORD_M1 | `***REDACTED***` | Encryption key material — preserved as redacted, not guessable from this metadata. |
| CRYPTO_FILE_PATH | `context.cryptoPath` | Externalized crypto-config file path (variable not found in any extracted context group — see Issues observed). |
| Schema | 436 columns (`LOGON` ... `XD_ACCT_NUMBER`) | Only the first 436 of the upstream 462 business columns are present in this component's schema; the trailing 26 (`VAL_LTR_DT`, `TRIP_DT_2`, `TRIP_CERT`, `TRIP_ERROR`, `TRIP_RECON`, ..., `LETTERABLE`, `EMAILABLE`, `TEXTABLE`, `CELL_PHONE_F83`) are absent — see Issues observed. |

### Transform: `tMap_1`

| Setting | Value | What it means |
|---|---|---|
| DIE_ON_ERROR | `true` | Any mapping/lookup error here fails the job outright (unlike the upstream file-read step). |
| Output schema | `FILENAME`, `FILEDATE`, `COL1`...`COL500` (502 columns) | Business field names are discarded in favor of a fixed, generically-numbered column layout — matches `tDBOutput_2`'s target schema exactly. |

### Target: `tDBOutput_2` (`tSnowflakeOutput`)

| Setting | Value | What it means |
|---|---|---|
| Table | `CUBS_DEBTOR_RAW_CO_CURRENT` | Per-run staging table for this file batch (CO site). |
| Output action | `UPSERT` | Row-level upsert into the staging table (merge key not shown in this component's own metadata). |
| Table action | `NONE` | Table is not recreated/altered by this job. |
| Schema | `FILENAME`, `FILEDATE`, `COL1`...`COL500`, plus reject-flow columns (`columnName`, `rowNumber`, `category`, `character`, `errorMessage`, `byteOffset`, `line`, `sqlState`, `code`) — `COL3` is the only column marked non-nullable | A reject schema exists on this component, but (per `connections`) no reject flow is wired out of it — see Issues observed. `COL3` being the sole non-nullable column corroborates that it's the merge/business key used downstream. |

### Archive/cleanup: `tFileArchive_1` / `tFileDelete_1`

| Setting | Value | What it means |
|---|---|---|
| TARGET (`tFileArchive_1`) | `context.archiveDir + "/" + TalendDate.getDate("CCYYMMDD") + "/" + context.fileName + ".tar.gz"` | Archives each processed file into a date-stamped subfolder. |
| SOURCE_FILE (`tFileArchive_1`) | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/source.csv"` | Hardcoded developer-workstation path (see `hardcoded_path_findings`); actual `SOURCE` param is `context.filePath`, so this hardcoded value appears to be an unused/default placeholder rather than the active source. |
| ENCRYPT_FILES / PASSWORD (`tFileArchive_1`) | `false` / `***REDACTED***` | Archive encryption is disabled, so the redacted password is configured but not currently used. |
| DIRECTORY / PATH (`tFileDelete_1`) | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/delete_folder"` / `"...delete_folder or delete_file"` | Hardcoded developer-workstation paths (see `hardcoded_path_findings`); actual `FILENAME` param used is `context.currentFile`. |

### Merge step: `tDBRow_2` (`tSnowflakeRow`)

| Setting | Value | What it means |
|---|---|---|
| Query | `MERGE INTO EDWPRODHH.STAGING.CUBS_DEBTOR_RAW AS tgt USING STAGING.CUBS_DEBTOR_RAW_CO_CURRENT AS src ON tgt.FILEDATE = src.FILEDATE AND tgt.COL3 = src.COL3 WHEN NOT MATCHED THEN INSERT (FILENAME, FILEDATE, COL1...COL500) VALUES (src.FILENAME, src.FILEDATE, src.COL1...src.COL500);` | Copies rows not already present (by `FILEDATE`+`COL3`) from the per-run CO staging table into the shared cross-site raw table. There is **no `WHEN MATCHED THEN UPDATE`** clause — see Issues observed. |
| Runs when | `OnSubjobOk` from `tFileList_1` | Fires once after the entire file-load loop finishes successfully, not once per file. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none — `runjob_targets` is empty; this job contains no `tRunJob` components.
- **Called by:** not found as a `tRunJob` target anywhere in `06_dependency_matrix.md`. The matrix shows the `CUBS_Raw_Debtor_Load` orchestrator calling a differently-named job, `CUBS_Raw_CO_Debtor_Load` (without the `_Upsert` suffix), for the CO site — the same is also separately called by `CO_Master_Load`. See Issues observed.
- **Context variables used:** `sourceRoot`, `cryptoPath`, `currentLogon` (none of these three appear in any context group in `_shared_context.json` — the closest named variables, `sourceDir`/`sourceDCDir` in `StandardFolders_0.1`, are different names), plus `archiveDir` and `logDir` (defined in `StandardFolders_0.1`, with two candidate values each — `/archive/`/`/logs/` vs. `C:/Data/`/`C:/Data/` — the metadata doesn't indicate which corresponds to which environment), and `currentFile`, `fileName`, `filePath` (set internally by `tJava_2`/`tJava_3` from `tFileList_*` iteration state). Unlike the CHI sibling, this job does **not** reference any `EXPORT_DEBTOR_*` context variables — its delimiter/header/encoding settings are hardcoded instead (see Issues observed).
- **4 hardcoded developer-workstation paths** (`C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...`) in `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, and `tFileDelete_1.DIRECTORY`/`PATH` — the same portability risk pattern documented project-wide in `05_operational_runbook.md`.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tPrejob` / `tPostjob` | Marks the setup/teardown subjobs that run once before/after the rest of the job, regardless of how many times the main flow iterates. |
| `tSnowflakeConnection` / `tSnowflakeClose` | Opens / closes the Snowflake connection used throughout the job. |
| `tFileList` | Lists files in a directory for the job to iterate over one at a time. |
| `tJava` | Runs a block of custom Java code once (not per row). |
| `tFileInputDelimited` | Reads a delimited (CSV-style) text file according to a schema. |
| `tDataEncrypt` | Encrypts specified column values in the row using a configured algorithm/key. |
| `tMap` | Maps/transforms columns from one schema to another. |
| `tSnowflakeOutput` | Writes rows to a Snowflake table (insert/update/upsert/etc., per `outputAction`). |
| `tSnowflakeRow` | Runs an arbitrary SQL statement (here, a `MERGE`) against Snowflake. |
| `tFileArchive` / `tFileDelete` | Archives a processed file to a compressed location, then deletes the original from the source directory. |

## Issues observed

- **Job name says "Upsert," but the merge is insert-only.** `tDBRow_2`'s `MERGE` statement has a `WHEN NOT MATCHED THEN INSERT` clause and no `WHEN MATCHED THEN UPDATE` clause — rows already present in `EDWPRODHH.STAGING.CUBS_DEBTOR_RAW` (matched by `FILEDATE`+`COL3`) are left untouched, not updated. Functionally this is a dedup-insert/append pattern, not a true upsert. This is the same naming/behavior mismatch already documented for the CHI sibling (`CUBS_Raw_CHI_Debtor_Load_Upsert`), so it appears to be a systemic template characteristic rather than a one-off mistake in this job.
- **Schema drift between `tFileInputDelimited_1` and `tDataEncrypt_1`.** The file-read schema carries 462 business columns (`CUBS-DEBTOR-CO`), but `tDataEncrypt_1`'s schema stops at column 436 (`XD_ACCT_NUMBER`) — the trailing 26 source columns (`VAL_LTR_DT`, `TRIP_DT_2`, `TRIP_CERT`, `TRIP_ERROR`, `TRIP_RECON`, `TRIP_ERRCD`, `TRIP_ADD`, `TRIP_BAL`, `IOC_IW_NBR`, `IOC_STATUS`, `OFFSET_AMT`, `OFFSET_DT`, `TRIP_LTR`, `TRIP_DEL`, `IOC_AMT_HELD`, `IOC_AMT_PAID`, `IOC_DEL`, `AGENCY_CODE`, `IOC_MTBALL`, `IOC_FROMDT`, `IOC_MOD`, `TRIP_LTR_DT`, `LETTERABLE`, `EMAILABLE`, `TEXTABLE`, `CELL_PHONE_F83`) are not present in `tDataEncrypt_1`'s schema and therefore not available to the downstream `tMap_1`. This is the same schema-drift pattern seen in the CHI sibling job (there it was 668→328, a ~340-column gap; here it is a smaller but still real 462→436, a 26-column gap), which suggests both jobs' `tDataEncrypt` steps were not kept in sync when their respective source file formats were last extended.
- **No `SCHEMA_REJECT` parameter at all, and file-format settings are hardcoded rather than externalized.** Unlike the CHI sibling, this job's `tFileInputDelimited_1` has no `SCHEMA_REJECT` repository-schema reference in its captured parameters, and its `FIELDSEPARATOR`/`ROWSEPARATOR`/`HEADER`/`ENCODING` are literal hardcoded values (`"\t"`, `"\n"`, `1`, `"ISO-8859-15"`) instead of the `context.EXPORT_DEBTOR_*` variables the CHI job uses. This means the CO job avoids the CHI job's site-mismatched-reject-schema issue, but at the cost of losing the flexibility (and consistency with other sites) that externalizing these settings would provide — if the CO file format ever needs to change, it requires a code change here rather than a context-value change.
- **No `tFlowMeter` row-counting component.** The CHI sibling counts rows with a `tFlowMeter_3` component between `tMap_1` and its Snowflake output; this CO job wires `tMap_1` directly to `tDBOutput_2` with no equivalent row-count instrumentation. Not necessarily a defect, but a monitoring-coverage gap relative to the sibling job.
- **Not referenced by any orchestrator job under its own name.** `06_dependency_matrix.md` shows both `CUBS_Raw_Debtor_Load` and `CO_Master_Load` calling `CUBS_Raw_CO_Debtor_Load` (without the `_Upsert` suffix), not this job. Unable to determine from metadata whether `CUBS_Raw_CO_Debtor_Load_Upsert` is a newer replacement not yet wired into either orchestrator, a manually/ad-hoc-triggered job, or a separate job that happens to share almost the same name — verify with the team before assuming either job is dead code.
- **Several referenced context variables have no defined default anywhere in the extracted project context groups.** `context.sourceRoot`, `context.cryptoPath`, and `context.currentLogon` are all read by this job's components but do not appear in any of the context groups captured in `_shared_context.json` (the closest match, `sourceDir`/`sourceDCDir` in `StandardFolders_0.1`, is a different variable name). Either this job carries its own job-level context defaults that weren't captured by this extraction, or these are unresolved references — verify with the team.
- **4 hardcoded developer-workstation paths** (`C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...`) in `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, and `tFileDelete_1.DIRECTORY`/`PATH` — the same project-wide portability risk already documented in `05_operational_runbook.md`; none of these override the actual active `FILENAME`/`SOURCE` parameters (which correctly use `context.currentFile`/`context.filePath`), so they appear to be inert leftover defaults rather than active bugs, but should still be cleaned up.
- **The merge's natural key (`FILEDATE` + `COL3`) is opaque.** Because `tMap_1`/`tDBOutput_2` use the generic `COL1`-`COL500` naming scheme instead of business field names, `COL3`'s real meaning (the only one of the 500 marked non-nullable in `tDBOutput_2`'s schema, suggesting it's a business key such as an account or debtor ID) cannot be determined from this metadata.
