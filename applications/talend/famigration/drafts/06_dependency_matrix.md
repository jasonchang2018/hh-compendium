# Dependency Matrix

## Overview

This matrix shows what each of the 12 `FAMIGRATION` jobs depends on: the source/target tables it moves data between, the one Talend-defined database connection and the one context (variable) group in the project, and whether it truncates its target table before loading. Read each row as "this job needs these things to run correctly." Because no job in this project calls another (no `tRunJob` components were found anywhere in the extracted metadata), there is no job-to-job dependency column — every job is independent of every other job.

## Matrix Table

| Job | Source table (SQL Server) | Target table (Snowflake) | Has transform step? | Table emptied before load? | Uses `Common_0.1` context group (`keystorePath`)? | Uses `Frostlake_0.1` connection (Talend repository object)? |
|---|---|---|---|---|---|---|
| Calls_Load | dbo.calls | CALLS | Yes (`tMap_1`) | No (`tableAction=NONE`) | Yes | No — connects with its own hardcoded host/port/login instead |
| Client_Load | dbo.client | CLIENT | No | No (`tableAction=CREATE_IF_NOT_EXISTS`) | Yes | No |
| CommTexts_Load | dbo.commtexts | COMMTEXTS | No | Yes | Yes | No |
| Debtor_Load | dbo.debtor | DEBTOR | No | Yes | Yes | No |
| Email_Address_Load | dbo.email_address | EMAIL_ADDRESS | No | Yes | Yes | No |
| Emails_Load | dbo.emails | EMAILS | No | Yes | Yes | No |
| Letters_Load | dbo.letters | LETTERS | No | Yes | Yes | No |
| Phone_Numbers_Load | dbo.phone_number | PHONE_NUMBER | No | Yes | Yes | No |
| Texts_Load | dbo.texts | TEXTS | No | Yes | Yes | No |
| Transactions_Load | dbo.transactions | TRANSACTIONS | No | Yes | Yes | No |
| Validation_Load | dbo.validation | VALIDATION | No | Yes | Yes | No |
| VoApps_Load | dbo.voapps | VOAPPS | No | Yes | Yes | No |

All 12 jobs also connect to the same Snowflake account (`xca26579.us-east-1`), warehouse (`COMPUTE_WH`), database/schema (`EDWPRODHH.BIDATA`), and role (`DATALOADER`) — that pattern is omitted from the columns above only because it's identical across every row.

## Notes

- **Every job shares one SQL Server login and host — hardcoded, not centralized.** All 12 jobs connect to `10.1.40.7:1433` as `svc_talend`, but none of them do it through the project's one defined database connection (`Frostlake_0.1`) or through a context variable — the host, port, and login are typed directly into each job's `tDBInput_1` component. This is the riskiest pattern in the matrix: a single source-side change (server move, port change, password rotation) requires editing all 12 jobs individually, and there's no shared place to see or update it.
- **The one defined connection object (`Frostlake_0.1`) looks unused.** It's declared at the project level with every detail field (host, port, database, schema) blank in the extracted metadata, and no job's components reference it by name. Worth confirming with the team whether it's a leftover from an earlier design or is used by tooling not captured in this extraction.
- **The one context group (`Common_0.1` → `keystorePath`) is used by all 12 jobs identically** — every job loads the same SSL keystore file path before opening its Snowflake connection. This is the one thing that is properly centralized in this project; if it needs to change, changing the single context variable value updates all 12 jobs at once (assuming they share the same context environment).
- **Two jobs (`Calls_Load`, `Client_Load`) don't empty their target table before loading, while the other ten do.** Since none of the 12 jobs use an upsert (all use plain `INSERT`, even though each has an `upsertKeyColumn` configured — see each job's page), these two are the only ones at risk of duplicate rows from a re-run or an overlapping schedule. This inconsistency (10 jobs truncate, 2 don't) looks unintentional rather than deliberate, since nothing else distinguishes those two jobs' purpose from the rest.
- **No job has a visible dependency on another job, which is expected here** — this project is a flat set of independent one-table loaders, not an orchestrated pipeline. If any of these 12 tables are actually meant to load in a particular order relative to each other (e.g. `Client_Load` before `Debtor_Load` because debtor rows reference a client), that ordering is not enforced anywhere in Talend and would need to be verified with the team and enforced by whatever external scheduler runs these jobs.
