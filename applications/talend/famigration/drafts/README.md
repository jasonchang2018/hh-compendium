# FAMIGRATION Documentation — Index

This folder documents the `FAMIGRATION` Talend project: 12 jobs that each copy one table out of a SQL Server database and into Snowflake. Start with the four system-level documents below for the platform-wide picture, then use the job index for the details of any individual job. Everything here is written in plain English and grounded in the extracted Talend metadata — where something couldn't be confirmed from that metadata (notably, anything about Qlik Cloud), the docs say so explicitly rather than guessing.

## System-level documents (start here)

| Document | What it covers |
|---|---|
| [01. System Architecture](01_system_architecture.md) | What the platform does end to end, the project/job/connection counts, and a diagram of the overall data flow from SQL Server through Talend into Snowflake (and, unconfirmed, on to Qlik). |
| [04. Data Lineage Map](04_data_lineage_map.md) | A source → job → Snowflake-table trace for every one of the 12 jobs, plus an explicit list of the parts of the chain (mainly the Qlik side) that couldn't be confirmed from metadata. |
| [05. Operational Runbook](05_operational_runbook.md) | How to check whether a job ran, how to safely restart a failed one, and the specific failure modes this project is actually exposed to (e.g. duplicate rows, a hardcoded source server). |
| [06. Dependency Matrix](06_dependency_matrix.md) | Which jobs depend on which database connection and context (variable) group, and which patterns in that matrix look risky (e.g. hardcoded credentials repeated in every job). |

## Job-by-job documentation

| Document | What it covers |
|---|---|
| [talend/FAMIGRATION/README.md](talend/FAMIGRATION/README.md) | The job index — all 12 jobs grouped by the patterns that set them apart (has a transform step, doesn't truncate before loading, etc.), plus a full alphabetical table linking to each job's own page. |

Each individual job page (linked from that index) covers: what the job does, its version/author/dates, a step-by-step walkthrough with a diagram, its source/target settings translated into plain English, what it depends on, a glossary of the Talend component types it uses, and any issues observed in its configuration.

## Qlik app documentation

Not available yet. No `qlik_metadata.json` has been extracted for this workspace (the Qlik Cloud extractor is opt-in and hasn't been run), so there are no Qlik app names, spaces, or reload schedules to document. This gap is called out in `01_system_architecture.md` and `04_data_lineage_map.md` rather than guessed at. Run `src/qlik/qlik_cloud_extractor.py` and regenerate the docs to fill this in.

## Superseded / raw reference material

These were produced automatically by earlier, non-AI stages of the documentation pipeline, before the plain-English documents above existed. They're kept for reference but the documents above should be treated as the current source of truth — in particular, `02_job_documentation.md` mis-classifies all 12 jobs as "utility/demo" jobs because its rule-based classifier doesn't recognize the `tMSSqlInput` → `SnowflakeOutput` pattern as a real pipeline; the job pages linked above describe what each job actually does.

| Document | What it is |
|---|---|
| [00. System Overview](00_system_overview.md) | The raw, template-generated architecture summary (pre-enrichment version of `01_system_architecture.md`). |
| [02. Job Documentation](02_job_documentation.md) | The raw, rule-based job classification (pre-enrichment version of the job-by-job pages; see the mis-classification note above). |
| [AI Documentation Prompt](AI_DOCUMENTATION_PROMPT.md) | The prompt template used to generate the plain-English documents in this folder. |
