# Operational Runbook

## Overview

This runbook covers day-to-day operation of the 24 active `FAMIGRATION` loaders that keep `EDWPRODHH.BIDATA` in step with SQL Server, plus the two BIDATA utility jobs (`BIDATA_Schema_Deploy`, `BIDATA_Load_Summary_Alert`). Unlike the previous truncate-and-reload design, these loaders are now **stateful**: each one remembers how far it got in `ETL_BOOKMARK` and records every run in `ETL_JOB_RUN_LOG` / `ETL_JOB_RUN_STEP`. That makes monitoring much easier, because status is now in Snowflake rather than only in the scheduler. It also means a careless restart or manual edit can skip or replay changes. Everything below is derived from the job metadata and `Snowflake_BIDATA_Schema_Change.sql` on branch `feature/bidata_incremental_changes`. Qlik reload monitoring is out of scope because no Qlik metadata was extracted.

## How-To Sections

### 0. First-time deployment (once per environment)

1. Run `BIDATA_Schema_Deploy` (or `Snowflake_BIDATA_Schema_Change.sql` by hand) **before** any loader on this branch. It adds `ROW_HASH` to the 24 target tables, makes a few column changes (`NOTICE_ACCOUNT.NOTICE_ACCOUNT_ID`, `VOAPPS.SOURCE_FILE_DATE`, `TBL_FA_CONSUMER_TEXTING_RESP_3P_HIST.RESPONSE_ID` widened, `TRANSACTIONS.TRANS_DATE` → `TIMESTAMP_NTZ(3)`), and creates/seeds `ETL_BOOKMARK`, the 48 `STG_CHANGED_*` tables, `ETL_JOB_RUN_LOG`, `ETL_JOB_RUN_STEP` and the `ETL_JOB_PROGRESS_V` progress view.
2. **Expect target tables to be empty until each loader has run once.** The deploy script truncates any target table that does not yet have `ROW_HASH` before adding the column, and every bookmark starts at 0, so the first run of every loader is a FULL reload.
3. **Known defect — check the deploy's verification step.** The verification query inside the job (`tDBInput_1`) ends with an unterminated comment (`/* ---------- Live progress (run any time`), so Snowflake will most likely reject it with a syntax error *after* the DDL has already been applied. Treat a failure on that step as "verify manually" rather than "deploy failed", and fix the query in Talend Studio. Failed checks in that step are only printed; they do not fail the job.
4. To start a very large table from its current data instead of a FULL reload, the script's comments describe setting that table's `ETL_BOOKMARK.LAST_CHANGE_ID` to the change ID captured at its last full load. Only do this if you are certain the target already matches the source up to that change.

### 1. Monitoring job status

1. **Live progress:** query `EDWPRODHH.BIDATA.ETL_JOB_PROGRESS_V`. It shows status, current step, batches done, rows done/pending, percent complete, elapsed time and an estimated finish time for FULL loads.
2. **Latest run per table:** in `ETL_JOB_RUN_LOG`, take the newest `RUN_ID` per `TABLE_NAME` (the schema script includes a ready-made `QUALIFY ROW_NUMBER()` query). `STATUS` is `RUNNING`, `SUCCESS` or `FAILED`; `LOAD_MODE` shows FULL/INCR/NONE; `ERROR_MESSAGE` holds the first error captured.
3. **Per-step detail:** join `ETL_JOB_RUN_STEP` to the run on `TALEND_PID` + `JOB_NAME` and order by `STEP_NO` to see which step failed and how long each took.
4. **Daily email:** `BIDATA_Load_Summary_Alert` emails a colour-coded table covering the last `LOOKBACK_HOURS` (default 24). With the default `SEND_ONLY_ON_ISSUES=false` it sends every run; the subject is prefixed `[ACTION NEEDED]` when any table failed, did not run, or is still running. Tables missing from `ETL_BOOKMARK` are never reported.
5. **Where the schedule lives:** no job triggers another, so run frequency and order come from an external scheduler (likely Talend Cloud Management Console). **Unable to determine from metadata — verify with team.**

### 2. Restarting a failed loader

1. **Find out which mode failed** from `ETL_JOB_RUN_LOG.LOAD_MODE` and the failed step in `ETL_JOB_RUN_STEP`.
2. **INCR failure:** safe to simply re-run. The delete + MERGE + bookmark update happen in one Snowflake transaction, so a failure rolls back and the bookmark stays where it was; the next run re-applies the same change range.
3. **FULL failure:** re-run, but be aware the target is **empty or partially loaded until the re-run completes**. The truncate is committed separately from the reload, so readers (dashboards) will see missing data in the meantime. The bookmark is only advanced after a successful load, so the re-run will again be FULL.
4. **NONE:** nothing was loaded and the bookmark was not touched; there is nothing to restart.
5. **Stuck `RUNNING` rows:** if a job was killed, its log row stays `RUNNING` until a newer run for that table replaces it. The `Log run end` step also has `dieOnError=false`, so a failure while writing the final status can leave a row `RUNNING`. Check the scheduler before assuming it is still running.
6. **Never run the retired jobs in `Older_Inactive_Jobs`** to "fix" a table. In particular `Account_Load_Copy` truncates and reloads `ACCOUNT` outside the bookmark framework, which would leave the bookmark and the table out of step.
7. **Do not run two copies of the same loader at once.** Staging table names are fixed per table (`STG_CHANGED_<TABLE>`), so overlapping runs would overwrite each other's staged rows.

### 3. Forcing a full reload

Either insert a full-reload marker (`change_operation = 'F'`) into `dbo.SF_ChangeLog` for that table (if that is how the change log is maintained; verify with the team), or set the table's `ETL_BOOKMARK.LAST_CHANGE_ID` to 0. Both make the next run FULL. Do not delete the bookmark row: the jobs only ever `UPDATE` it, so a missing row means every run is FULL and the bookmark never advances.

### 4. Troubleshooting the most likely failure modes evident from the metadata

- **Every run is FULL for one table.** The bookmark row is missing (jobs never insert it) or stuck at 0, or `SF_ChangeLog` keeps receiving `F` markers. Check `ETL_BOOKMARK` for that `TABLE_NAME`.
- **FULL fails validation.** Batched loaders fail with a custom Snowflake error if a batch did not finish, fewer than 99.5% of source rows arrived, or the key column is not unique (error -20003). The three `Notice_letter/Text/Validation` loaders key on `NOTICEID`, whose uniqueness the metadata cannot confirm; this is the first suspect if one of them fails here. Note the 0.5% tolerance means a FULL load can succeed with some rows missing.
- **SSL/keystore errors on every job.** Each job's `tSetKeystore_1` has a **hardcoded** path `C:/Users/svc_talend_prd/ssl/keystore.p12`, while the `keystorePath` context variable defaults to `C:/Users/svc_talend_prd/.ssl/keystore.p12` (note the dot). Check which file actually exists on the Talend agent; changing the context variable alone will not fix a missing hardcoded path.
- **Source-side change breaks every job at once.** Host `10.1.40.7:1433` and the SQL Server login are typed into every job (with `trustServerCertificate=true`) rather than using the empty `Frostlake_0.1` connection or a context variable. A server move or password rotation means editing all 26 active jobs individually.
- **Failures with no run-log row.** If a job fails before it writes its `RUNNING` row (keystore, connection, bookmark or change-log read), nothing appears in `ETL_JOB_RUN_LOG`; check the scheduler/Talend logs instead. In the alert email this shows up as "not run".
- **Column-type errors after deploying to a new environment.** `Tbl_Fa_Consumer_Texting_Resp_3p_Hist_Load` needs the `RESPONSE_ID` widening, `VoApps_Load` needs `SOURCE_FILE_DATE`, `Notice_Account_Load` needs `NOTICE_ACCOUNT_ID`, and `Transactions_Load` needs the new `TRANS_DATE` type, all from the schema deploy (step 0).
- **Alert email not arriving.** `BIDATA_Load_Summary_Alert` sends through `harriscollect-com.mail.protection.outlook.com:25` with SSL and STARTTLS both off, and its default recipient (`emailRecipients`) is a single person rather than a distribution list. Check the context values set for the production run.

## Glossary

| Term | Plain-English meaning |
|---|---|
| Bookmark | The `ETL_BOOKMARK` row for a table: the last change-log ID that has been applied to it. |
| FULL / INCR / NONE | Reload everything / apply only changed rows / nothing to do. |
| Full-reload marker | A change-log entry with `change_operation = 'F'`, which forces the next run to be FULL. |
| Batch | One key range of a FULL load on a batched loader (default 5,000,000 rows; up to 4 run in parallel). |
| Die on error | A per-step setting that stops the whole job if that step fails, instead of logging and continuing. |
| MERGE | One SQL statement that updates existing rows and inserts new ones. |
| `ROW_HASH` | A fingerprint of a row's contents, used to skip updates when nothing actually changed. |
| Run log | `ETL_JOB_RUN_LOG` (one row per run) and `ETL_JOB_RUN_STEP` (one row per step). |
| `ETL_JOB_PROGRESS_V` | A Snowflake view over the run log that shows live progress and an estimated finish time. |
| Service account | A non-human login used by an automated job (here, the SQL Server login and the Snowflake `DATALOADER` role). |
