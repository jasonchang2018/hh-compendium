# Talend Job: CUBS_Raw_TOL_Client_Load

## Overview

Loads CUBS client master records (agency/creditor client accounts — name, address, phone, statement/invoice-frequency settings, commission/interest-rate fields, scoring thresholds, and a long tail of client-level flags) for the TOL site from a single delimited export file into the Snowflake `CUBS_CLIENT_RAW_CURRENT` staging table, then archives and deletes the source file. It is structurally and configurationally a near-exact copy of `CUBS_Raw_CO_Client_Load` (and, per that job's own doc, of `CUBS_Raw_CHI_Client_Load`) — same ~199-column-to-`COL1`-`COL200` flattening shape, same mismatched `CSVROWSEPARATOR`, same generically-labeled `"metadata"` main schema, same mislabeled `"CUBS_TRANSACTION"` reject schema. Unlike its CO sibling, however, **this job has no visible caller** in the project's `tRunJob` orchestration graph — see Issues observed.

## Detail table

| Field | Value |
|---|---|
| Job name | CUBS_Raw_TOL_Client_Load |
| Version | 0.1 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2024-04-18T09:18:40.510-0700 |
| Last Modified | 2025-11-04T11:08:07.574-0800 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` → `tJava_1` opens a per-run log file at `context.logDir + context.currentLogon + "_" + jobName + "_" + <timestamp> + ".log"` → on `SUBJOB_OK`, `tSetKeystore_1` configures SSL trust/keystore from `context.keystorePath` (passwords redacted) → on `SUBJOB_OK`, `tDBConnection_1` opens the Snowflake connection.

**Main subjob:**

1. `tFileInputDelimited_1` reads a single file at `context.sourceDir + context.EXPORT_CLIENT_File` (not a directory loop — one fixed export file per run). Separators/header/encoding are context-driven from the `EXPORT_CLIENT_*` group (`EXPORT_CLIENT_RowSeparator`, `EXPORT_CLIENT_FieldSeparator`, `EXPORT_CLIENT_Header`, `EXPORT_CLIENT_Encoding`), **except `CSVROWSEPARATOR`, which is set to `context.EXPORT_TRANS_RowSeparator`** instead of an `EXPORT_CLIENT_*` variable (only relevant if `CSV_OPTION` is ever turned on — currently `false`). `TRIMALL=true`. The main schema is labeled generically `"...- metadata"` in the repository (~199 unique client business columns: `LOGON`, `CLIENT`, `CLIENT_IDX`, `NAME`, address fields, rate/commission fields, statement/invoice settings, scoring thresholds, etc. — `LOGON`/`CLIENT`/`CLIENT_IDX` are marked non-nullable). The reject schema is labeled `"...- CUBS_TRANSACTION"`. `DIE_ON_ERROR=false`, no reject flow wired.
2. On `SUBJOB_OK` (as soon as the file read succeeds — not gated on the Snowflake insert), `tFileArchive_1` archives `context.sourceDir` to `context.archiveDir + "/" + <CCYYMMDD> + "/" + context.EXPORT_CLIENT_File + ".tar.gz"` (password redacted, `ENCRYPT_FILES=false`), then on `SUBJOB_OK`, `tFileDelete_1` deletes `context.sourceDir + context.EXPORT_CLIENT_File`.
3. On `FLOW`, `tMap_1` maps the ~199 named business columns to a generic output schema of `FILENAME`, `FILEDATE`, `COL1`–`COL200` (202 columns) — meaningful column names are not preserved past this point.
4. `tFlowMeter_2` counts rows passing through (link labeled `"cli"` — renamed from the Talend default, same as `CUBS_Raw_CO_Client_Load`).
5. `tDBOutput_1` inserts the rows into Snowflake table `CUBS_CLIENT_RAW_CURRENT` (`INSERT`, `tableAction=NONE` — no `TRUNCATE` step anywhere in this job and no merge call afterward, despite the `_RAW_CURRENT` table name).

**Teardown subjob:** `tPostjob_1` → `tDBClose_1` closes the Snowflake connection.

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> OpenLog["tJava_1<br/>Open per-run log file"] -->|OnSubjobOk| Keystore["tSetKeystore_1<br/>Configure SSL"] -->|OnSubjobOk| Connect["tDBConnection_1<br/>Open Snowflake connection"]

    Read["tFileInputDelimited_1<br/>Read sourceDir + EXPORT_CLIENT_File<br/>(CSVROWSEPARATOR mismatched)"] -->|FLOW| Map["tMap_1<br/>Map ~199 named cols to<br/>generic COL1-COL200"]
    Map -->|FLOW cli| FlowMeter["tFlowMeter_2<br/>Count rows"]
    FlowMeter -->|FLOW| Insert["tDBOutput_1<br/>INSERT into CUBS_CLIENT_RAW_CURRENT<br/>(no TRUNCATE, no merge)"]

    Read -->|OnSubjobOk| Archive["tFileArchive_1<br/>Archive source file to archiveDir"]
    Archive -->|OnSubjobOk| Delete["tFileDelete_1<br/>Delete source file"]

    Postjob["tPostjob_1"] --> Close["tDBClose_1<br/>Close Snowflake connection"]
```

## Settings tables

### Source: `tFileInputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.sourceDir + context.EXPORT_CLIENT_File` | A single, fixed export file per run — no directory iteration. |
| ROWSEPARATOR / FIELDSEPARATOR / HEADER / ENCODING | `context.EXPORT_CLIENT_RowSeparator` / `context.EXPORT_CLIENT_FieldSeparator` / `context.EXPORT_CLIENT_Header` / `context.EXPORT_CLIENT_Encoding` | Correctly scoped to the CLIENT export context group. |
| CSVROWSEPARATOR | `context.EXPORT_TRANS_RowSeparator` | **Mismatched** — references the Trans export's row separator instead of an `EXPORT_CLIENT_*` variable; only takes effect if `CSV_OPTION` is enabled (currently `false`). Identical mismatch to `CUBS_Raw_CO_Client_Load` and `CUBS_Raw_CHI_Client_Load`. |
| TRIMALL | `true` | All field values are trimmed of leading/trailing whitespace. |
| Main schema | Repository `"...- metadata"` (~199 unique client columns) | Generic repository label, not client- or site-specific — same as `CUBS_Raw_CO_Client_Load`, under a different repository GUID. |
| Reject schema | Repository `"...- CUBS_TRANSACTION"` | Mislabeled — same issue class as `CUBS_Raw_CO_Client_Load`, `CUBS_Raw_Payplan_Load`, and `ADP_Payroll_Load`. |
| TEMP_DIR | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace"` | Hardcoded developer-workstation path. |

### Transform: `tMap_1`

| Setting | Value | What it means |
|---|---|---|
| Output schema | `FILENAME`, `FILEDATE`, `COL1`–`COL200` (202 columns) | Identical width to `CUBS_Raw_CO_Client_Load`'s output shape. Named business columns are not preserved past this point. |

### Target: `tDBOutput_1` (`tSnowflakeOutput`)

| Setting | Value | What it means |
|---|---|---|
| Table | `CUBS_CLIENT_RAW_CURRENT` | Destination staging table — the same table name used by `CUBS_Raw_CO_Client_Load` and `CUBS_Raw_CHI_Client_Load`; no visible site-discriminator column in this metadata. |
| Output action / Table action | `INSERT` / `NONE` | Appends rows; no `TRUNCATE` precedes it and no merge stored procedure follows it. |
| Schema width | 211 columns (202 from `tMap_1` + 9 Snowflake reject-metadata columns). | |

### Archive / Delete: `tFileArchive_1` / `tFileDelete_1`

| Setting | Value | What it means |
|---|---|---|
| SOURCE / TARGET (`tFileArchive_1`) | `context.sourceDir` / `context.archiveDir + "/" + <CCYYMMDD> + "/" + context.EXPORT_CLIENT_File + ".tar.gz"` | Archives under a date-stamped subfolder; `PASSWORD` redacted, `ENCRYPT_FILES=false` (password not actually applied). |
| Trigger | Off `tFileInputDelimited_1`'s `SUBJOB_OK`, not off `tDBOutput_1` | Archive+delete happens as soon as the file is read, before the Snowflake insert is confirmed — a downstream failure in `tMap_1`/`tFlowMeter_2`/`tDBOutput_1` would still result in the source file being archived and deleted. Same ordering as `CUBS_Raw_CO_Client_Load`. |
| FILENAME (`tFileDelete_1`) | `context.sourceDir + context.EXPORT_CLIENT_File` | The actual value used; `DIRECTORY`/`PATH` hardcoded defaults (`.../workspace/delete_folder`) are present but not used. |

## Dependencies & configuration

- **Called by:** no job appears as a caller of `CUBS_Raw_TOL_Client_Load` in `06_dependency_matrix.md`'s `tRunJob` table — see Issues observed. This is unlike `CUBS_Raw_CO_Client_Load`, which is called once by `CO_Master_Load`.
- **Calls no other jobs** — `runjob_targets` is empty.
- **Context variables used:** `EXPORT_CLIENT_Encoding`, `EXPORT_CLIENT_FieldSeparator`, `EXPORT_CLIENT_File`, `EXPORT_CLIENT_Header`, `EXPORT_CLIENT_RowSeparator`, `EXPORT_TRANS_RowSeparator` (mismatched — see Issues observed), `archiveDir`, `currentLogon`, `keystorePath`, `logDir`, `sourceDir`.
- **5 hardcoded developer-workstation path findings** (`tFileInputDelimited_1.TEMP_DIR`, `tFileArchive_1.SOURCE_FILE`, `tFileDelete_1.DIRECTORY`/`PATH`, `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE`) — same project-wide pattern documented in `05_operational_runbook.md` (210 of 289 jobs).

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tFileInputDelimited` | Reads a delimited (CSV-style) text file according to a schema. |
| `tMap` | Maps/transforms columns from one schema to another. |
| `tFlowMeter` | Counts rows passing through a point in the flow, for logging/monitoring. |
| `tSnowflakeOutput` / `tSnowflakeConnection` / `tSnowflakeClose` | Write rows to a Snowflake table / open and close the shared Snowflake connection. |
| `tFileArchive` / `tFileDelete` | Zip a processed file to an archive location, then delete the original from the source directory. |
| `tSetKeystore` | Configures the SSL keystore/truststore used by subsequent secure connections. |
| `tPrejob` / `tPostjob` | Run once before/after the rest of the job. |
| `tJava` | Runs a block of custom Java code — here, opening a per-run log file. |

## Issues observed

- **No caller found for this job in `06_dependency_matrix.md`.** Of the six site-specific `_Client_Load` siblings implied by the project's site-code pattern (CHI/CO/DC/HH/PRE/TOL — see `01_system_architecture.md`), only `CUBS_Raw_CO_Client_Load` has a visible `tRunJob` caller (`CO_Master_Load`). Per that project-wide note in `05_operational_runbook.md` and `06_dependency_matrix.md`'s own Notes section, how (or whether) `CUBS_Raw_TOL_Client_Load` is triggered today is not visible in this metadata — verify with the team; an orphaned-looking job here could mean either an undocumented external trigger or a genuinely dead/retired job.
- **This job is a near-exact copy of `CUBS_Raw_CO_Client_Load`**, down to identical context-variable names (`context.EXPORT_CLIENT_*`), an identical `CSVROWSEPARATOR` mismatch, an identical generically-labeled `"metadata"` main schema, and an identical mislabeled `"CUBS_TRANSACTION"` reject schema. Nothing in this job's own component parameters is TOL-specific beyond the job name itself. Site differentiation must come entirely from per-job context-value overrides (e.g., a TOL-specific value bound to `context.sourceDir` or `context.EXPORT_CLIENT_File`) not captured in this extraction; verify directly in Talend Studio's context settings before assuming what actually differs between the CHI/CO/DC/HH/PRE/TOL siblings.
- **`CSVROWSEPARATOR` on `tFileInputDelimited_1` references `context.EXPORT_TRANS_RowSeparator`**, not an `EXPORT_CLIENT_*` variable, while every other separator/header/encoding setting on the same component is correctly scoped to `EXPORT_CLIENT_*`. Same copy-paste leftover as `CUBS_Raw_CO_Client_Load`; only matters if `CSV_OPTION` is ever switched on (currently `false`).
- **The reject schema is labeled `"CUBS_TRANSACTION"`, not a client-shaped schema**, and the main schema is labeled generically `"metadata"` rather than something client-specific — same mislabeling pattern as `CUBS_Raw_CO_Client_Load` and `ADP_Payroll_Load`.
- **`CUBS_Raw_TOL_Client_Load` and `CUBS_Raw_CO_Client_Load` (and presumably `CUBS_Raw_CHI_Client_Load`) all insert into the same table, `CUBS_CLIENT_RAW_CURRENT`**, with `INSERT`/`NONE` and no `TRUNCATE` in any of them. There is no visible site-discriminator column in the extracted schema — if multiple site jobs run against the same warehouse table without external partitioning or a later merge/dedup step, rows from different sites could co-mingle indistinguishably. Unable to confirm from metadata alone; verify with the team how (or whether) this table is expected to segregate site data.
- **No `TRUNCATE` step and no merge call anywhere in this job**, despite the target table being named `CUBS_CLIENT_RAW_CURRENT` — same missing-refresh-step concern as `CUBS_Raw_CO_Client_Load`.
- **Archive and delete are triggered by the file read succeeding, not by the Snowflake insert succeeding** — a downstream failure after `tFileInputDelimited_1` would still result in the source file being archived and removed from `sourceDir`.
- **Named business columns do not survive past `tMap_1`** — `CUBS_CLIENT_RAW_CURRENT` only stores generic `COL1`–`COL200` positional columns; interpreting any given column requires an external mapping back to this job's `tMap_1` configuration.
