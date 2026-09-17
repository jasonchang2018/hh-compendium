# FAMIGRATION Documentation — Index

This folder documents the `FAMIGRATION` Talend project: 12 jobs that each copy one table out of a SQL Server database and into Snowflake. Start with the four system-level documents below for the platform-wide picture, then use the job index for the details of any individual job. Everything here is written in plain English and grounded in the extracted Talend metadata — where something couldn't be confirmed from that metadata (notably, anything about Qlik Cloud), the docs say so explicitly rather than guessing.

## System-level documents (start here)

| Document | What it covers |
|---|---|
| [01_System_Architecture](01_system_architecture.md) | What the platform does end to end, the project/job/connection counts, and a diagram of the overall data flow from SQL Server through Talend into Snowflake (and, unconfirmed, on to Qlik). |
| [04_Data_Lineage_Map](04_data_lineage_map.md) | A source → job → Snowflake-table trace for every one of the 12 jobs, plus an explicit list of the parts of the chain (mainly the Qlik side) that couldn't be confirmed from metadata. |
| [05_Operational_Runbook](05_operational_runbook.md) | How to check whether a job ran, how to safely restart a failed one, and the specific failure modes this project is actually exposed to (e.g. duplicate rows, a hardcoded source server). |
| [06_Dependency_Matrix](06_dependency_matrix.md) | Which jobs depend on which database connection and context (variable) group, and which patterns in that matrix look risky (e.g. hardcoded credentials repeated in every job). |

## Job-by-job documentation

| Document | What it covers |
|---|---|
| [All_Job_Index](talend/FAMIGRATION/README.md) | The job index — all 12 jobs grouped by the patterns that set them apart (has a transform step, doesn't truncate before loading, etc.), plus a full alphabetical table linking to each job's own page. |


