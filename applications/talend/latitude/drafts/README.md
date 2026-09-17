# LATITUDE Platform Documentation

Reverse-engineered documentation for the LATITUDE Talend + Snowflake data platform, generated from extracted implementation metadata (`talend_metadata.json`) since no documentation existed from the original developer. No Qlik Cloud metadata was available at generation time, so Qlik apps/dashboards are not documented here.

## System-level documentation

| Doc | Covers |
|---|---|
| [`01_system_architecture.md`](01_system_architecture.md) | What the platform does end to end, project/connection counts, overall data flow diagram, glossary |
| [`04_data_lineage_map.md`](04_data_lineage_map.md) | Source file → Talend job → Snowflake staging table → merge → final table trace for every job, plus known gaps |
| [`05_operational_runbook.md`](05_operational_runbook.md) | How to monitor jobs, how to safely restart a failed job, known failure modes, configuration risks |
| [`06_dependency_matrix.md`](06_dependency_matrix.md) | Which jobs depend on which database connection / context group, and what's risky about that |

## Job-by-job documentation

| Doc              | Covers |
|------------------|--------|
| [`All_JOb_Index`](talend/LATITUDE/README.md)|All 56 Talend jobs in the `LATITUDE` project are documented individually |
