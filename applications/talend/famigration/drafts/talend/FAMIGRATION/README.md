# FAMIGRATION Job Index

**Platform-wide picture:** [System Architecture](../../01_system_architecture.md) · [Data Lineage Map](../../04_data_lineage_map.md) · [Operational Runbook](../../05_operational_runbook.md) · [Dependency Matrix](../../06_dependency_matrix.md)

## Overview

The `FAMIGRATION` project contains 12 Talend jobs. Every one of them follows the same pattern — read one table from the SQL Server source, optionally map it, and write it into a matching table in Snowflake — so there's no complex pipeline to navigate here; use the groups below to jump straight to the jobs that behave differently from the rest, or use the full alphabetical table for the complete list.

## Grouped Quick-Links

### Jobs with an in-Talend transformation step

Only one job actually transforms data inside Talend (via a `tMap` component) rather than passing the source row straight through — though the mapping itself is a 1:1 column pass-through with no logic.

- [Calls_Load](job_Calls_Load.md) — reads `dbo.calls`, maps every column through `tMap_1` unchanged, writes to `CALLS`.

### Jobs that don't empty their target table before loading (duplicate-row risk)

These two are the only jobs that skip the truncate step the other ten use, which means re-running them (or an overlapping schedule) can duplicate rows — see `06_dependency_matrix.md` for the full explanation.

- [Calls_Load](job_Calls_Load.md) — `tableAction=NONE`; appends straight into `CALLS` with no truncate.
- [Client_Load](job_Client_Load.md) — `tableAction=CREATE_IF_NOT_EXISTS`; creates `CLIENT` only if missing, never empties it.

### Standard truncate-and-reload jobs

The remaining ten jobs empty their target table before every load, so each run fully replaces the previous data with no duplicate-row risk.

- [CommTexts_Load](job_CommTexts_Load.md) — `dbo.commtexts` → `COMMTEXTS`
- [Debtor_Load](job_Debtor_Load.md) — `dbo.debtor` → `DEBTOR`
- [Email_Address_Load](job_Email_Address_Load.md) — `dbo.email_address` → `EMAIL_ADDRESS`
- [Emails_Load](job_Emails_Load.md) — `dbo.emails` → `EMAILS`
- [Letters_Load](job_Letters_Load.md) — `dbo.letters` → `LETTERS`
- [Phone_Numbers_Load](job_Phone_Numbers_Load.md) — `dbo.phone_number` → `PHONE_NUMBER`
- [Texts_Load](job_Texts_Load.md) — `dbo.texts` → `TEXTS`
- [Transactions_Load](job_Transactions_Load.md) — `dbo.transactions` → `TRANSACTIONS`
- [Validation_Load](job_Validation_Load.md) — `dbo.validation` → `VALIDATION`
- [VoApps_Load](job_VoApps_Load.md) — `dbo.voapps` → `VOAPPS`

_No gatekeeper/alert-only jobs, reverse-direction (Snowflake → file) exports, or jobs with explicit success/failure branching on a merge or load step were found in this project's metadata — every job here is a simple one-table loader._

## Full Alphabetical Table

| Job | Target table |
|---|---|
| [Calls_Load](job_Calls_Load.md) | CALLS |
| [Client_Load](job_Client_Load.md) | CLIENT |
| [CommTexts_Load](job_CommTexts_Load.md) | COMMTEXTS |
| [Debtor_Load](job_Debtor_Load.md) | DEBTOR |
| [Email_Address_Load](job_Email_Address_Load.md) | EMAIL_ADDRESS |
| [Emails_Load](job_Emails_Load.md) | EMAILS |
| [Letters_Load](job_Letters_Load.md) | LETTERS |
| [Phone_Numbers_Load](job_Phone_Numbers_Load.md) | PHONE_NUMBER |
| [Texts_Load](job_Texts_Load.md) | TEXTS |
| [Transactions_Load](job_Transactions_Load.md) | TRANSACTIONS |
| [Validation_Load](job_Validation_Load.md) | VALIDATION |
| [VoApps_Load](job_VoApps_Load.md) | VOAPPS |
