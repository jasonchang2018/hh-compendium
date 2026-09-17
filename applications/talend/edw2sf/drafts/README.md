# EDW2SF Platform Documentation

Reverse-engineered documentation for the EDW2SF Talend + Snowflake data platform, generated from extracted implementation metadata (`talend_metadata.json`) since no documentation existed from the original developer. No Qlik Cloud metadata was available at generation time, so Qlik apps/dashboards are not documented here.

EDW2SF is a large, heterogeneous project: 289 jobs spanning per-site (CHI/CO/DC/HH/PRE/TOL) `CUBS_Raw_*` raw-data loads, `i3_*` telephony/dialer loads, `tRunJob`-based orchestrators (most notably `CO_Master_Load`), payroll/HR, HOPE/HUB (MySQL) collections-workflow data, client reporting/scorecard jobs, and a long tail of one-off extracts, backfills, and utility jobs. Naming and structural conventions (staging-table prefixes, merge-procedure names, reject-flow wiring) are noticeably inconsistent across the project — see `05_operational_runbook.md` and individual job docs for specifics.

## System-level documentation

| Doc | Covers |
|---|---|
| [`01_system_architecture.md`](01_system_architecture.md) | What the platform does end to end, project/connection counts, overall data flow diagram, glossary |
| [`04_data_lineage_map.md`](04_data_lineage_map.md) | Source file/table → Talend job → Snowflake staging table → merge → final table trace for every job, plus known gaps |
| [`05_operational_runbook.md`](05_operational_runbook.md) | How to monitor jobs, how to safely restart a failed job, known failure modes, configuration risks |
| [`06_dependency_matrix.md`](06_dependency_matrix.md) | Which jobs depend on which database connection / context group, the full `tRunJob` orchestration graph (65 edges), and what's risky about that |

## Job-by-job documentation

All 289 Talend jobs in the `EDW2SF` project are documented individually under [`talend/EDW2SF/`](talend/EDW2SF/README.md) — start at that folder's [index](talend/EDW2SF/README.md) to jump straight to any job, grouped by family (orchestrators, per-site `CUBS_Raw_*` loads, `i3_*` telephony, ADP, HOPE/HUB, reporting/scorecards, extracts, dimensional-model loads, and more).
