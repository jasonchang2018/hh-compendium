# Operational Runbook

## Overview

This runbook covers day-to-day operation of the 12 `FAMIGRATION` Talend jobs that load SQL Server tables into Snowflake: how to check whether a job/reload ran successfully, how to restart a job that failed, and how to troubleshoot the failure modes that are actually visible in the extracted job metadata (as opposed to speculative ones). It does not cover Qlik reload monitoring, because no Qlik metadata was available to confirm what, if anything, reloads downstream of these Snowflake tables — see the gap noted in `04_data_lineage_map.md`.

## How-To Sections

### 1. Monitoring job / reload status

1. This documentation set was built from a one-time export of the Talend Studio workspace (a `.item` file per job), which has no execution history in it — it describes what each job *is configured to do*, not whether last night's run succeeded. To check actual run status, look at whichever scheduler triggers these jobs in production (Talend Cloud Management Console if the jobs are deployed as Tasks there, or an external scheduler such as Windows Task Scheduler/cron if not) — **which scheduler that is could not be determined from the metadata available here; verify with the team.**
2. Once you've found the run history, check each job's last run for a non-zero exit code or an uncaught exception — these jobs have no custom error-handling components (see #2 below), so a failure will surface as the job simply stopping partway through, not a friendly message.
3. In Snowflake, you can sanity-check that a load actually happened by checking `EDWPRODHH.BIDATA.<TABLE>` row counts/last-modified timestamps against when the job was supposed to run. Because 10 of the 12 tables are truncated before every load (see `06_dependency_matrix.md`), a table with an old or unexpectedly low row count is a strong sign that job didn't run or died partway through.

### 2. Restarting a failed job

1. None of the 12 jobs have `tRunJob` links to each other (confirmed from the extracted metadata — no job triggers another), so each of the 12 can be safely restarted independently without needing to also restart anything upstream or downstream in Talend.
2. Before restarting a job whose target table uses `TRUNCATE` (10 of the 12 — see `06_dependency_matrix.md`), you can simply re-run it: the truncate step will clear out any partial data from the failed attempt automatically.
3. Before restarting **`Calls_Load`** or **`Client_Load`** specifically, check whether the target table (`CALLS` or `CLIENT`) already picked up rows from the failed attempt. Because neither job truncates the table first and both use a plain `INSERT` (not an upsert), simply re-running either job after a partial failure **will duplicate any rows that made it through before the failure**. If in doubt, manually verify/clean up the partial rows in Snowflake before re-running.
4. All 12 jobs authenticate to SQL Server and Snowflake using credentials and a keystore path (`context.keystorePath`) that are set once per job rather than centrally — if a restart fails immediately with an authentication or SSL/TLS error, check that the SSL keystore file at the path in the `Common_0.1` context group (see `06_dependency_matrix.md`) still exists and is valid on whatever machine/agent runs the job, and that the `svc_talend` SQL Server login and the Snowflake `DATALOADER` role credentials haven't expired or been rotated.

### 3. Troubleshooting the most likely failure modes evident from the metadata

- **Duplicate rows in `CALLS` or `CLIENT` after a re-run or an overlapping schedule.** As above — these are the only two jobs that don't truncate their target table before loading. If you see row counts higher than expected in either table, this is the most likely cause. Confirm by counting duplicate primary-key values (`CALLIDKEY` for `CALLS`, `CLIENT_IDX` for `CLIENT` — both are the same columns configured as the unused `upsertKeyColumn` on each job, see `06_dependency_matrix.md`).
- **A single bad row aborting `Calls_Load`.** `Calls_Load` is the only job with a `tMap` transformation step, and that step has "die on error" turned on. If `Calls_Load` fails while the other 11 jobs are running fine, check for a row in `dbo.calls` with a value that can't be converted to the expected type (e.g. a non-numeric value in a numeric column) — that would stop the whole job rather than being skipped.
- **A source-side change breaking every job at once.** All 12 jobs point at the same hardcoded SQL Server host/port/login (`10.1.40.7:1433`, `svc_talend`) rather than a shared, centrally-updated connection or context variable. If SQL Server is moved, its port changes, or the `svc_talend` login's password rotates, **all 12 jobs will fail simultaneously** and each one has to be updated individually in Talend Studio (there is no single place to fix this once).
- **Confusing troubleshooting due to the source connection's name.** If you're debugging with someone unfamiliar with this project, note that the SQL Server source connection's `DBNAME` setting is literally the text `"snowflake"` in every job — this is a labeling artifact in the job design, not an indication that the source is actually a Snowflake database. Don't let it send troubleshooting down the wrong path.
- **Missing schema/description metadata.** None of the 12 jobs have a `purpose` or `description` field filled in in Talend Studio — there is no built-in documentation to fall back on inside the tool itself, which is part of why this documentation set exists.

## Glossary

| Term | Plain-English meaning |
|---|---|
| Die on error | A per-component setting that stops the whole job immediately if that step hits a data error, instead of skipping the bad row and continuing. |
| Upsert | "Update if it exists, insert if it doesn't" — a load mode that avoids duplicate rows by matching on a key column. None of these 12 jobs actually use it, despite each having a key column configured for it (see `06_dependency_matrix.md`). |
| Truncate | Emptying a table completely before loading new rows into it — used by 10 of the 12 jobs here as their way of avoiding duplicate data on every run. |
| Service account | A non-human login (here, `svc_talend` for SQL Server and the Snowflake `DATALOADER` role) used by an automated job rather than a person. |
