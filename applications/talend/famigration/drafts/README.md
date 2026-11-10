# FAMIGRATION Documentation — Index

This folder documents the `FAMIGRATION` Talend project, which keeps the Snowflake `EDWPRODHH.BIDATA` schema in step with a SQL Server source database. It contains 33 jobs: 24 active loaders, 2 BIDATA utility jobs and 7 retired jobs. This version reflects branch `feature/bidata_incremental_changes` (commit `5c013af`, 2026-10-29), where the loaders were reworked from simple truncate-and-reload jobs into incremental loaders driven by a change log and a bookmark table, with run logging and a daily summary email. Start with the four system-level documents below for the platform-wide picture, then use the job index for the details of any individual job. Everything here is written in plain English and grounded in the extracted Talend metadata (cross-checked against `Snowflake_BIDATA_Schema_Change.sql`). Where something couldn't be confirmed from that metadata (notably anything about Qlik Cloud, scheduling, or how `dbo.SF_ChangeLog` is populated), the docs say so explicitly rather than guessing.

## System-level documents (start here)

| Document | What it covers |
|---|---|
| [01_System_Architecture](01_system_architecture.md) | What the platform does end to end, job/connection counts, a data-flow diagram, and how each loader decides between FULL, INCR and NONE. |
| [04_Data_Lineage_Map](04_data_lineage_map.md) | A source → job → Snowflake-table trace for all 24 active loaders (with merge keys), the shared bookmark/staging/run-log path, the retired jobs, and an explicit list of what couldn't be confirmed. |
| [05_Operational_Runbook](05_operational_runbook.md) | First-time deployment, monitoring via the run-log tables and progress view, safe restarts for FULL vs INCR failures, forcing a full reload, and the failure modes visible in the metadata. |
| [06_Dependency_Matrix](06_dependency_matrix.md) | Which tables, control tables and context variables each job depends on, and which patterns look risky (hardcoded keystore path, unmaintained change feed, retired jobs still pointing at live tables). |

## Job-by-job documentation

| Document | What it covers |
|---|---|
| [All_Job_Index](talend/FAMIGRATION/README.md) | All 33 jobs grouped by kind (utility, batched loaders, single-pass loaders, retired), plus a full alphabetical table linking to each job's own page. |
