# Operational Runbook

## Overview

This runbook covers the LATITUDE Talend project only — it is built from job *definitions* in the extracted metadata, not from an execution scheduler, so it cannot tell you when a job is supposed to run or its recent run history. It explains what monitoring options the jobs themselves offer, how to approach restarting a failed job safely, and the failure patterns that are visible directly in the job definitions (as opposed to ones that would only show up in live logs).

## 1. Monitoring job status

- **No schedule/execution metadata is present in this extraction.** `talend_metadata.json` describes what each job *is* (its components, its SQL, its file paths) — not when it runs or whether last night's run succeeded. Job execution history lives in Talend Administration Center / Talend Management Console (or whatever scheduler triggers these jobs), which is outside what was extracted here.
- **Email is the only built-in "it broke" signal captured in the metadata**, and only two jobs send one: `Export_File_Check` emails `jmach@harriscollect.com` if the expected upstream export file never arrives within 4 hours (240 checks × 60 seconds), and `Plan_Success_Alert` is a single-component job whose only job is to send a mail (its trigger/schedule is unable to determine from metadata). Everything else that can fail (see §3) only writes a message to the job's own execution log — there is no email/alert wired to those failures in what was extracted.
- **Practical monitoring today means checking the Talend execution log for each run**, specifically looking for the `tDie`/`tWarn` messages listed in §3, since those are the only jobs that classify their own failures with a specific message and severity code.

## 2. Restarting a failed job

Before restarting any of the 46+ "text load" jobs (`Address_Text_Load`, `Bankruptcy_Text_Load`, etc.), it helps to know the pattern they all follow: each one truncates a Snowflake staging table (schema `LIQUID_STAGING` in most cases), reloads it from the current source file, then calls a merge procedure or `MERGE` statement to fold that into the final table, then archives and deletes the source file. Because the staging table is truncated at the start of every run, **simply re-running the same job against the same source file is normally safe** — the staging step will overwrite whatever was there before it merges again. Two things to check before you do that:

1. **Was the source file already archived/deleted?** Steps near the end of each job (`tFileArchive`, `tFileDelete`) move or remove the source file from the watched folder once it's been read. If the job failed *after* that step, the file may no longer be sitting where the job expects it, and a straight rerun will find nothing to load. Check the archive directory (`context.archiveDir`) for the file before re-triggering.
2. **Was the failure inside the merge step, not the load step?** For the 8 jobs listed in §3 that explicitly evaluate success/failure (`tDie`/`tWarn`), a failure there means the staging table was loaded but the merge into the final table did not complete or reported an error. Re-running the whole job again is usually still correct (staging gets truncated and reloaded either way), but if the same merge keeps failing on retry, the problem is very likely in the underlying Snowflake stored procedure or the data itself, not in Talend — escalate to whoever owns the `MERGE_TXT_INTO_*` procedures in Snowflake (see `04_data_lineage_map.md`'s Gaps section — those procedure bodies aren't visible from Talend at all).

`master_prediction_proposal_Load` and `Last4SSN_Extract` are exceptions to the truncate-then-merge pattern (see `04_data_lineage_map.md`) — treat a rerun of either more cautiously since it's unable to determine from metadata whether they're idempotent the same way.

## 3. Troubleshooting the most likely failure modes evident from the metadata

| Job | What can trip it | What the job tells you |
|---|---|---|
| `cmi_Hermes_Recommendations_Load` | The `MERGE_TXT_INTO_CMI_HERMES_RECOMMENDATIONS()` Snowflake procedure call fails or reports an error code | `tDie` message: `"MERGE failed - error code <code>"` |
| `cmi_VoApp_Results_Load` | Same pattern — its merge procedure call fails | `tDie`/`tWarn` on the merge result |
| `Dialer_CallTracking_Load` | Same pattern | `tDie`/`tWarn` on the merge result |
| `master_prediction_proposal_Load` | Same pattern (its procedure is `INSERT_TXT_INTO_MASTER_PREDICTION_PROPOSAL()`, not a merge — see the Gaps note in `04_data_lineage_map.md`) | `tDie`/`tWarn` on the procedure result |
| `PatientInfo_Text_Load` | Same pattern | `tDie`/`tWarn` on the merge result |
| `HH_Violation_Text_Load` | Same pattern | `tDie` only (no corresponding success `tWarn` component was found) |
| `Livevox_Daily_Load` | Same pattern | `tWarn` only (no `tDie` found — a failed merge here may only produce a warning, not a hard failure) |
| `Export_File_Check` | The upstream export never drops a `*_zz-done.csv` file in `context.sourceDir` within 4 hours | Emails `jmach@harriscollect.com` with `"The Latitude export to Snowflake failed to start: " + context.errorMsg`, then fails with exit code 4 and message `"No Latitude export files to load into Snowflake!"` |
| Any of the 51 jobs with a hardcoded `C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...` path (see §"Configuration risks") | The job runs on a machine where that exact folder doesn't exist (e.g., a new build agent or a Linux-hosted scheduler) | A component-level file-not-found error at whichever step references that path (typically the archive/delete steps) |
| Any job depending on `TalendLog_0.1` | This repository connection has no host, port, database, or schema configured at all | Would fail immediately with a connection error if any job actually uses it (no job in this project was found to reference it — see `06_dependency_matrix.md`) |

## Configuration risks worth fixing, not just monitoring

- **51 of 56 jobs contain a hardcoded, developer-specific path** (`C:/Talend-Studio-20211109_1610-V8.0.1/workspace/...`), typically inside a `tFileArchive`/`tFileCopy`/`tFileDelete` component, alongside the otherwise-parameterized `context.sourceDir`/`context.archiveDir` variables. This should be parameterized the same way the rest of the file paths already are — as written, moving these jobs to a different Talend Studio install path or a non-Windows runner would very likely break them.
- **51 of 56 jobs configure a client trust-store/keystore (`tSetKeystore`) pointing at `context.keystorePath`**, which does vary correctly between the two recorded context value sets (`C:/Users/jmach/.ssl/keystore.p12` vs. `/etc/keys/keystore.p12`) — this one is already parameterized correctly and is called out here only so it isn't mistaken for a gap.
- **`TalendLog_0.1`, one of only two defined repository database connections, has no host, port, database, or schema value at all.** If anything is meant to use it (its name suggests centralized job logging), it isn't configured, and it isn't referenced by any of the 56 jobs in this project based on the extracted metadata.

## Glossary

| Term | Plain-English meaning |
|---|---|
| Staging table | A table that gets emptied (`TRUNCATE`) and reloaded on every job run — it reflects only the most recent file, not a running history. |
| Merge (procedure or inline) | The step that reconciles the freshly loaded staging rows into the permanent table — inserting new records and updating changed ones, rather than blindly appending. |
| `tDie` / `tWarn` | Talend components that end a job with a specific failure message and severity code (`tDie`) or log a warning without stopping the job (`tWarn`) — used here to react to whether a Snowflake merge succeeded. |
| Watched folder / marker file | The pattern `Export_File_Check` uses: instead of loading data itself, it waits for a specific file name pattern to appear as a signal that an upstream process has finished. |
