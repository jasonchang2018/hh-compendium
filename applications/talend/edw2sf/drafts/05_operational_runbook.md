# Operational Runbook — EDW2SF Project

## Overview

This covers what the 289 job *definitions* themselves reveal about monitoring and failure handling — not a scheduler's execution history, which isn't part of this metadata. One real complication: several jobs are **orchestrators** that call other jobs, so a single failure can originate several layers deep in a call chain (see `04_data_lineage_map.md`).

## 1. Monitoring job status

- **No schedule/execution metadata is present.** Job history lives in whatever scheduler triggers these jobs (Talend Administration Center or equivalent), not in this extraction.
- **12 jobs send email on failure or completion** (`Avita_Monthly_Report_Extract`, `Carle_Asset_Scrub`, `Columbia_Doctors_Legal_Rpt`, `DC_Call_Contact_Exceptions_2`, `LW_COC_Water_Scrub`, `LW_Carle_Asset_Scrub`, `LW_Insurance_Pmt_Tracking`, `LW_ProMedica_Scrub`, `Semaphore_Check`, `TEST_Avita_Monthly_Report_Extract`, `TEST_Email_Alerts`, `VA_Tax_Inventory_Report`) — mostly the external-partner report/scrub jobs, plus `Semaphore_Check`, which appears to be a gatekeeper job that waits for something and alerts if it doesn't show up in time.
- **16 jobs have explicit `tDie`/`tWarn` logic** reacting to a load or merge result (`ADP_Payroll_Load`, `ADP_Roster_Load`, `CO_Master_Load`, `CUBS_PostDates_Load`, `CUBS_Raw_Trans_Load_Special`, `DimCellphone_Load`, `DimDeskInfo_Load`, `DimEmployeeInfo_Load`, `Fact_Electronic_Media_Load`, `Livevox_Daily_Load`, `PaymentPlan_Load`, `ProInsight_CCU_Scorecard_V2_Load`, `ProInsight_HPS_Scorecard_Load`, `ProInsight_Scorecard_Load`, `Raw_PCI_Letter_Load`, `Semaphore_Check`) — for the rest of the 289 jobs, a failure only shows up as a generic Talend execution error in the log, not a job-specific message.
- **`CO_Master_Load` failing tells you the least on its own** — because it's an orchestrator, its own failure message won't say which of its 10 sub-jobs actually broke; check each sub-job's own log/`tDie` output (see its doc for the full call list).

## 2. Restarting a failed job

A truncate-staging-then-merge pattern appears across most `CUBS_Raw_*`/`Dim*_Load`/`Fact*_Load` jobs (see each job's own doc for its specific staging table and merge step) — the general guidance is: rerunning a job is usually safe because its staging table gets cleared and reloaded every run, but check whether the source file was already archived/deleted, and whether the failure was in the load step or in a downstream merge.

Two things specific to EDW2SF:

1. **If an orchestrator job failed (`CO_Master_Load`, `HealthPartners_Close_Rpt_Master`, `CUBS_Raw_Debtor_Load`, `CUBS_Raw_ETL_Load`, or any other job with `tRunJob` links — see `06_dependency_matrix.md`), find out which specific sub-job actually failed before restarting anything.** `CO_Master_Load` runs 10 sub-jobs in a defined order (some in parallel); restarting the whole orchestrator from the top may be wasteful or even harmful if some of its sub-jobs already succeeded and aren't safe to rerun (e.g. anything that doesn't follow the truncate-and-reload pattern) — confirm case by case.
2. **A handful of jobs (`ADP_Payroll_Load`, `ADP_Roster_Load`, and others tagged with explicit merge-result checking) fail loudly by design** — a `tDie` there is the job telling you specifically that its merge/load step reported a problem, which is more informative than a generic error and should point you straight at the underlying data or Snowflake procedure issue rather than a Talend problem.

## 3. Configuration risks worth fixing, not just monitoring

- **210 of 289 jobs contain the same hardcoded, developer-specific path** (`C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...`) — moving these jobs to a different install path or a non-Windows runner would very likely break them.
- **All 9 repository database connections have no host/port/database configured** — every real connection is wired through a hand-labeled component (see `01_system_architecture.md`) backed by a context group instead. Two of those labels (`SF_Equabli`, `SF_Equabli_2`, `PUB_JCHANG`) look like they may be tied to a specific external partner or individual rather than shared infrastructure — worth confirming who owns them and what happens if that person/relationship changes.
- **Only one site (`CO`) has its own `_Master_Load` orchestrator.** If the other sites (CHI, DC, HH, PRE, TOL) are supposed to run the same sequence of jobs, how that's triggered today is unable to determine from metadata — verify with team, since an undocumented trigger mechanism is itself an operational risk (nobody but its owner may know it exists).

## Glossary

| Term | Plain-English meaning |
|---|---|
| Orchestrator job | A job that mainly exists to run other jobs in sequence via `tRunJob`, rather than moving data itself. |
| Connection label | The human-readable name a developer gave a connection component on the canvas (e.g. `LEGACY_DW`) — the real way to tell which underlying system/credentials a job is using, since the repository connection list itself is blank. |
| `tDie` / `tWarn` | Ends a job with a specific failure message (`tDie`) or logs a warning without stopping it (`tWarn`). |
