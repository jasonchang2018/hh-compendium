# Talend Job: CUBS_Raw_PRE_Debtor_Load_Upsert

## Overview

Loads CUBS collections debtor master-file extracts for the PRE site (per-debtor demographic and account fields — name, address, phone, client, agency-code, trip/IOC/letter-cycle flags, letterable/emailable/textable flags, etc., per the `CUBS_DEBTOR_PRE` repository schema) from a local drop directory into Snowflake. Each file's rows are AES-encrypted (PII fields) in flight, flattened into a generic `COL1`-`COL500` staging schema, and loaded into `CUBS_DEBTOR_RAW_PRE_CURRENT` (`UPSERT` output action). Once every file in the batch has loaded, a single `MERGE` statement copies any not-already-present rows from that staging table into the cross-site raw table `EDWPRODHH.STAGING.CUBS_DEBTOR_RAW`, after which processed source files are archived (as `.tar.gz`) and then deleted from the source directory. This job is one of the `CUBS_Raw_<Site>_Debtor_Load_Upsert` family that repeats the same template per site code (CHI, CO, DC, HH, PRE, TOL — see `01_system_architecture.md`); see Issues observed for the specific ways this PRE copy differs from its CHI/CO siblings.

## Detail table

| Field | Value |
|---|---|
| Job name | CUBS_Raw_PRE_Debtor_Load_Upsert |
| Version | 0.4 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2024-07-11T12:00:15.946-0700 |
| Last Modified | 2026-07-07T12:12:16.609-0700 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` →(`OnComponentOk`)→ `tJava_4` opens a per-run log file at `context.logDir + context.currentLogon + "_" + jobName + "_" + <timestamp> + ".log"` and redirects `System.out` to it (code truncated at 253 characters in the extracted metadata; remainder not recoverable from this JSON) →(`OnComponentOk`)→ `tDBConnection_1` opens the job's Snowflake connection.

**Main subjob — file-load loop (runs once per file in `context.sourceRoot`):**

1. `tFileList_1` lists files in `context.sourceRoot` (files only, no subdirectories; `ORDER_BY_NOTHING=true`, so no explicit sort order is applied; `EXCLUDEFILEMASK="*.txt"` is configured but `IFEXCLUDE=false`, so that exclusion is not actually applied — every file in the directory is picked up).
2. `tFileList_1` →(`ITERATE`)→ `tJava_3` copies the current iteration's file path/name/directory from `globalMap` into `context.currentFile` / `context.fileName` / `context.filePath` (code truncated in metadata after the `System.out.println("Proc...` line).
3. →(`ITERATE`)→ `tFileInputDelimited_1` reads the file as delimited text using repository schema `CUBS_DEBTOR_PRE` (333 distinct business columns — see Issues observed on how this is captured in the metadata), with `FIELDSEPARATOR=context.EXPORT_DEBTOR_FieldSeparator`, `ROWSEPARATOR=context.EXPORT_DEBTOR_RowSeparator`, `HEADER=context.EXPORT_DEBTOR_Header`, `ENCODING=context.EXPORT_DEBTOR_Encoding` (all externalized to context, not hardcoded); `DIE_ON_ERROR=false`. Its `SCHEMA_REJECT` is set to repository schema `CUBS_DEBTOR_HH` — mismatched to the HH site, not PRE — see Issues observed.
4. →(`FLOW`, link `row1`)→ `tDataEncrypt_1` AES-encrypts the row (`SECRET_TYPE`, `SECRET_KEY`, `PASSWORD_M1` all `***REDACTED***` in source metadata). Its own schema carries only 329 of the upstream 333 business columns — see Issues observed.
5. →(`FLOW`, link `row2`)→ `tMap_1` maps the row down to a generic 502-column output shape: `FILENAME`, `FILEDATE`, `COL1`...`COL500` (`DIE_ON_ERROR=true`, so a mapping failure fails the job).
6. →(`FLOW`, link `PRE_DBTR`)→ `tFlowMeter_3` counts rows passing through (link explicitly named `PRE_DBTR` for this job, unlike the generic labels seen in some sibling jobs).
7. →(`FLOW`, link `row3`)→ `tDBOutput_1` (`tSnowflakeOutput`) writes to table `CUBS_DEBTOR_RAW_PRE_CURRENT` with `outputAction=UPSERT`, `tableAction=NONE`.
8. →(`OnComponentOk`)→ `tFileArchive_1` archives the just-processed file to `context.archiveDir + "/" + <today's date CCYYMMDD> + "/" + context.fileName + ".tar.gz"`.

**After the entire file-load loop subjob completes successfully** (not per file): `tFileList_1` →(`OnSubjobOk`)→ `tDBRow_2` (`tSnowflakeRow`) runs a single `MERGE` from `STAGING.CUBS_DEBTOR_RAW_PRE_CURRENT` into `EDWPRODHH.STAGING.CUBS_DEBTOR_RAW`, matching on `FILEDATE` + `COL3`, inserting only rows `WHEN NOT MATCHED` (no `WHEN MATCHED` clause — see Issues observed).

**Cleanup loop (runs after the merge, once per file in `context.sourceRoot` again):**

9. `tDBRow_2` →(`OnSubjobOk`)→ `tFileList_2` re-lists files in `context.sourceRoot` (same directory, same filter settings as `tFileList_1`) →(`ITERATE`)→ `tJava_2` re-sets `context.currentFile`/`fileName`/`filePath` from this second listing →(`ITERATE`)→ `tFileDelete_1` deletes `context.currentFile` →(`OnComponentOk`)→ `tJava_1` logs the delete status/path/error from `globalMap` (code also truncated in metadata).

**Teardown subjob:** `tPostjob_1` →(`OnComponentOk`)→ `tDBClose_1` closes the Snowflake connection.

```mermaid
flowchart TD
    Prejob["tPrejob_1"] -->|OnComponentOk| OpenLog["tJava_4<br/>Open per-run log file"]
    OpenLog -->|OnComponentOk| Connect["tDBConnection_1<br/>Open Snowflake connection"]

    FileList1["tFileList_1<br/>List files in sourceRoot"] -->|Iterate| SetVars1["tJava_3<br/>Set currentFile/fileName/filePath"]
    SetVars1 -->|Iterate| ReadCSV["tFileInputDelimited_1<br/>Read CSV (schema: CUBS_DEBTOR_PRE;<br/>reject schema mislabeled HH)"]
    ReadCSV -->|row1| Encrypt["tDataEncrypt_1<br/>AES encrypt (329 of 333 cols)"]
    Encrypt -->|row2| Map["tMap_1<br/>Flatten to FILENAME/FILEDATE/COL1-COL500"]
    Map -->|PRE_DBTR| FlowMeter["tFlowMeter_3<br/>Count rows"]
    FlowMeter -->|row3| Output["tDBOutput_1<br/>UPSERT into CUBS_DEBTOR_RAW_PRE_CURRENT"]
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
| ORDER_BY_NOTHING | `true` | No explicit sort order is applied to the file list. |
| EXCLUDEFILEMASK / IFEXCLUDE | `"*.txt"` / `false` | An exclusion mask is configured but explicitly disabled (`IFEXCLUDE=false`) — every file in `sourceRoot`, including `.txt` files, is picked up. |

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.currentFile` | The current file from `tFileList_1`'s iteration. |
| FIELDSEPARATOR | `context.EXPORT_DEBTOR_FieldSeparator` | Externalized to context (default `"\t"` per `EXPORT_DEBTOR_0.1` in `_shared_context.json`), not hardcoded. |
| ROWSEPARATOR | `context.EXPORT_DEBTOR_RowSeparator` | Externalized (default `"\n"`). |
| HEADER | `context.EXPORT_DEBTOR_Header` | Externalized (default `1` header row). |
| ENCODING | `context.EXPORT_DEBTOR_Encoding` | Externalized (default `US-ASCII`). |
| SCHEMA (main) | Repository schema `CUBS_DEBTOR_PRE` (id `_e3LJsM1UEey68bfiIIIBcg`) | 333 distinct business columns (`LOGON` through `PV_FLAG`: demographic, client, agency, trip/IOC/letter-cycle, letterable/emailable/textable flags) — correctly labeled for the PRE site. Note the raw extracted `schema_columns` list for this component contains 668 entries because the same 333-column list appears to have been captured twice back-to-back (666 rows) plus the 2 reject columns (`errorCode`, `errorMessage`); this doc counts only the distinct 333. |
| SCHEMA_REJECT | Repository schema `CUBS_DEBTOR_HH` (id `_P5bI4GQVEeyyeeshWCVUmg`) | **Site mismatch** — this is the PRE job but its reject schema is labeled for HH. See Issues observed. |
| DIE_ON_ERROR | `false` | Malformed rows don't fail the job... |
| Reject flow | Not wired | ...but no connection in this job routes rejected rows anywhere — they are silently dropped. |
| TEMP_DIR | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace"` | Hardcoded developer-workstation path (see `hardcoded_path_findings`). |

### Transform: `tDataEncrypt_1`

| Setting | Value | What it means |
|---|---|---|
| CRYPTO_METHOD | `AES` | Symmetric encryption of column values. |
| SECRET_TYPE / SECRET_KEY / PASSWORD_M1 | `***REDACTED***` | Encryption key material — preserved as redacted, not guessable from this metadata. |
| CRYPTO_FILE_PATH | `context.cryptoPath` | Externalized crypto-config file path (variable not found in any extracted context group — see Issues observed). |
| Schema | 329 columns (`LOGON` ... `SIG_PROC_DT`) | Only the first 329 of the upstream 333 business columns are present in this component's schema; the trailing 4 (`LETTERABLE`, `EMAILABLE`, `TEXTABLE`, `PV_FLAG`) are absent — see Issues observed. |

### Transform: `tMap_1`

| Setting | Value | What it means |
|---|---|---|
| DIE_ON_ERROR | `true` | Any mapping/lookup error here fails the job outright (unlike the upstream file-read step). |
| Output schema | `FILENAME`, `FILEDATE`, `COL1`...`COL500` (502 columns) | Business field names are discarded in favor of a fixed, generically-numbered column layout — matches `tDBOutput_1`'s target schema exactly, and the same layout used by the CHI/CO siblings. |

### Target: `tDBOutput_1` (`tSnowflakeOutput`)

| Setting | Value | What it means |
|---|---|---|
| Table | `CUBS_DEBTOR_RAW_PRE_CURRENT` | Per-run staging table for this file batch (PRE site). |
| Output action | `UPSERT` | Row-level upsert into the staging table (merge key not shown in this component's own metadata). |
| Table action | `NONE` | Table is not recreated/altered by this job. |
| Schema | `FILENAME`, `FILEDATE`, `COL1`...`COL500`, plus reject-flow columns (`columnName`, `rowNumber`, `category`, `character`, `errorMessage`, `byteOffset`, `line`, `sqlState`, `code`) — 511 columns total; `COL3` is the only column marked non-nullable | A reject schema exists on this component, but (per `connections`) no reject flow is wired out of it — see Issues observed. `COL3` being the sole non-nullable business column corroborates that it's the merge/business key used downstream. |

### Archive/cleanup: `tFileArchive_1` / `tFileDelete_1`

| Setting | Value | What it means |
|---|---|---|
| TARGET (`tFileArchive_1`) | `context.archiveDir + "/" + TalendDate.getDate("CCYYMMDD") + "/" + context.fileName + ".tar.gz"` | Archives each processed file into a date-stamped subfolder. |
| SOURCE (`tFileArchive_1`) | `context.filePath` | The actual source used at runtime. |
| SOURCE_FILE (`tFileArchive_1`) | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/source.csv"` | Hardcoded developer-workstation path (see `hardcoded_path_findings`); not the active `SOURCE` param, so appears to be an unused default placeholder. |
| ENCRYPT_FILES / PASSWORD (`tFileArchive_1`) | `false` / `***REDACTED***` | Archive encryption is disabled, so the redacted password is configured but not currently used. |
| FILENAME (`tFileDelete_1`) | `context.currentFile` | The actual file deleted at runtime. |
| DIRECTORY / PATH (`tFileDelete_1`) | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/delete_folder"` / `"...delete_folder or delete_file"` | Hardcoded developer-workstation paths (see `hardcoded_path_findings`); not the active `FILENAME` param. |

### Merge step: `tDBRow_2` (`tSnowflakeRow`)

| Setting | Value | What it means |
|---|---|---|
| Query | `MERGE INTO EDWPRODHH.STAGING.CUBS_DEBTOR_RAW AS tgt USING STAGING.CUBS_DEBTOR_RAW_PRE_CURRENT AS src ON tgt.FILEDATE = src.FILEDATE AND tgt.COL3 = src.COL3 WHEN NOT MATCHED THEN INSERT (FILENAME, FILEDATE, COL1...COL500) VALUES (src.FILENAME, src.FILEDATE, src.COL1...src.COL500);` | Copies rows not already present (by `FILEDATE`+`COL3`) from the per-run PRE staging table into the shared cross-site raw table. There is **no `WHEN MATCHED THEN UPDATE`** clause — see Issues observed. |
| Runs when | `OnSubjobOk` from `tFileList_1` | Fires once after the entire file-load loop finishes successfully, not once per file. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none — `runjob_targets` is empty; this job contains no `tRunJob` components.
- **Called by:** not found as a `tRunJob` target anywhere in `06_dependency_matrix.md`. The matrix shows `CUBS_Raw_Debtor_Load` calling `CUBS_Raw_PRE_Debtor_Load` (without the `_Upsert` suffix) for the PRE site instead. See Issues observed.
- **Context variables used:** `EXPORT_DEBTOR_Encoding`, `EXPORT_DEBTOR_FieldSeparator`, `EXPORT_DEBTOR_Header`, `EXPORT_DEBTOR_RowSeparator` (all defined with defaults in the `EXPORT_DEBTOR_0.1` context group — see Issues observed on that group's own HH-flavored default file path), `sourceRoot`, `cryptoPath`, `currentLogon` (none of these three appear in any context group in `_shared_context.json` — the closest named variables, `sourceDir`/`sourceDCDir` in `StandardFolders_0.1`, are different names), plus `archiveDir` and `logDir` (defined in `StandardFolders_0.1`, with two candidate values each — `/archive/`/`/logs/` vs. `C:/Data/`/`C:/Data/` — the metadata doesn't indicate which corresponds to which environment), and `currentFile`, `fileName`, `filePath` (set internally by `tJava_2`/`tJava_3` from `tFileList_*` iteration state).
- **4 hardcoded developer-workstation paths** (`C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...`) in `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, and `tFileDelete_1.DIRECTORY`/`PATH` — the same project-wide portability risk pattern documented in `05_operational_runbook.md`; none of these override the actual active `FILENAME`/`SOURCE` parameters (which correctly use `context.currentFile`/`context.filePath`), so they appear to be inert leftover defaults rather than active bugs, but should still be cleaned up.

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
| `tFlowMeter` | Counts rows passing a point in the flow, for logging/monitoring. |
| `tSnowflakeOutput` | Writes rows to a Snowflake table (insert/update/upsert/etc., per `outputAction`). |
| `tSnowflakeRow` | Runs an arbitrary SQL statement (here, a `MERGE`) against Snowflake. |
| `tFileArchive` / `tFileDelete` | Archives a processed file to a compressed location, then deletes the original from the source directory. |

## Issues observed

- **Job name says "Upsert," but the merge is insert-only.** `tDBRow_2`'s `MERGE` statement has a `WHEN NOT MATCHED THEN INSERT` clause and no `WHEN MATCHED THEN UPDATE` clause — rows already present in `EDWPRODHH.STAGING.CUBS_DEBTOR_RAW` (matched by `FILEDATE`+`COL3`) are left untouched, not updated. Functionally this is a dedup-insert/append pattern, not a true upsert. This is the same naming/behavior mismatch already documented for the CHI and CO siblings (`CUBS_Raw_CHI_Debtor_Load_Upsert`, `CUBS_Raw_CO_Debtor_Load_Upsert`), so it appears to be a systemic template characteristic across the whole `_Upsert` family rather than a one-off mistake in this job.
- **Reject schema is labeled for the wrong site.** `tFileInputDelimited_1`'s `SCHEMA_REJECT` is the `CUBS_DEBTOR_HH` repository schema, not a PRE-specific one, even though this is `CUBS_Raw_PRE_Debtor_Load_Upsert`. The CHI sibling job has the identical defect (its reject schema is also `CUBS_DEBTOR_HH`), and the `EXPORT_DEBTOR_0.1` context group's own `EXPORT_DEBTOR_File` default value (`Z:/EDW/2021-11-27/HH/HH-EDW-EXPORT-DEBTOR1.txt`) is also an HH path — together these strongly suggest the whole `CUBS_Raw_*_Debtor_Load_Upsert` template family, including its shared reject-schema and context defaults, was originally built for the HH site and cloned per-site without repointing the reject schema. Combined with the fact that no reject flow is actually wired out of `tFileInputDelimited_1` (`DIE_ON_ERROR=false`, malformed rows are simply dropped with no record), a malformed PRE row's shape mismatch against the HH reject schema is unverifiable from this metadata — verify directly in the Talend repository.
- **Schema drift between `tFileInputDelimited_1` and `tDataEncrypt_1`, though smaller than in sibling jobs.** The file-read schema carries 333 distinct business columns (`CUBS_DEBTOR_PRE`), but `tDataEncrypt_1`'s schema stops at column 329 (`SIG_PROC_DT`) — the trailing 4 columns (`LETTERABLE`, `EMAILABLE`, `TEXTABLE`, `PV_FLAG`) are not present in `tDataEncrypt_1`'s schema and therefore not available to the downstream `tMap_1`. This is the same kind of schema-drift pattern seen in the CHI and CO sibling jobs (there the gaps were larger), suggesting the `tDataEncrypt` step across this whole job family is not reliably kept in sync when the source file format is extended — here the practical impact looks small (only 4 trailing flag columns), but it should still be confirmed whether those flags are needed downstream.
- **Raw extracted schema for `tFileInputDelimited_1` appears to duplicate its 333-column list back-to-back** (666 of the 668 captured `schema_columns` entries are an exact repeat, plus 2 reject columns). This looks like an artifact of how the main and reject-schema branches were captured together in this metadata export, not a real 666-column schema in the Talend job itself — worth being aware of when comparing raw metadata sizes across jobs in this family, since a naive column count would overstate the actual schema width by roughly 2x.
- **Not referenced by any orchestrator job under its own name.** `06_dependency_matrix.md` shows `CUBS_Raw_Debtor_Load` calling `CUBS_Raw_PRE_Debtor_Load` (without the `_Upsert` suffix) for the PRE site, not this job. Unable to determine from metadata whether `CUBS_Raw_PRE_Debtor_Load_Upsert` is a newer replacement not yet wired into that orchestrator, a manually/ad-hoc-triggered job, or a separate job that happens to share almost the same name — verify with the team before assuming either job is dead code.
- **Several referenced context variables have no defined default anywhere in the extracted project context groups.** `context.sourceRoot`, `context.cryptoPath`, and `context.currentLogon` are all read by this job's components but do not appear in any of the context groups captured in `_shared_context.json` (the closest match, `sourceDir`/`sourceDCDir` in `StandardFolders_0.1`, is a different variable name). Either this job carries its own job-level context defaults that weren't captured by this extraction, or these are unresolved references — verify with the team.
- **4 hardcoded developer-workstation paths** (`C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...`) in `tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, and `tFileDelete_1.DIRECTORY`/`PATH` — the same project-wide portability risk already documented in `05_operational_runbook.md`; each is inert (the active `SOURCE`/`FILENAME` params correctly use `context.filePath`/`context.currentFile`), but should still be cleaned up.
- **The merge's natural key (`FILEDATE` + `COL3`) is opaque.** Because `tMap_1`/`tDBOutput_1` use the generic `COL1`-`COL500` naming scheme instead of business field names, `COL3`'s real meaning (the only one of the 500 marked non-nullable in `tDBOutput_1`'s schema, suggesting it's a business key such as an account or debtor ID) cannot be determined from this metadata.
- **The two Java logging/cleanup snippets (`tJava_1`, `tJava_3`, `tJava_4`) are truncated at 253 characters in this job's extracted metadata**, each ending mid-statement with a literal `...`. The visible portions show what each is doing (setting context vars from `tFileList` iteration state, opening/redirecting a log file, printing delete status), but the full code — including any additional logic past the truncation point — is not recoverable from this JSON; verify directly in Talend Studio if the complete logic matters.