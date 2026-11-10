# FAMIGRATION Job Index

**Platform-wide picture:** [System Architecture](../../01_system_architecture.md) · [Data Lineage Map](../../04_data_lineage_map.md) · [Operational Runbook](../../05_operational_runbook.md) · [Dependency Matrix](../../06_dependency_matrix.md)

## Overview

The `FAMIGRATION` project contains 33 Talend jobs (extracted from branch `feature/bidata_incremental_changes`). There are 24 active loaders that each keep one Snowflake `BIDATA` table in step with one SQL Server table, 2 BIDATA utility jobs, and 7 retired jobs kept in the `Older_Inactive_Jobs` folder. All 24 active loaders use the same bookmark + change-log design (FULL / INCR / NONE), so the groups below focus on what sets jobs apart. Use the full alphabetical table at the bottom for the complete list.

## Grouped Quick-Links

### BIDATA utility jobs (`process/misc`)

- [BIDATA_Schema_Deploy](job_BIDATA_Schema_Deploy.md): one-off deployment that adds `ROW_HASH` to the 24 target tables and creates the bookmark, staging and run-log tables. Must run before any loader.
- [BIDATA_Load_Summary_Alert](job_BIDATA_Load_Summary_Alert.md): gatekeeper/alert job. Reads the bookmark and run log and emails a colour-coded load summary for the last 24 hours, flagged `[ACTION NEEDED]` when a table failed or didn't run.

### Batched loaders (large tables: parallel key-range FULL loads with post-load validation)

On a FULL load these split the source into 5,000,000-row key ranges, load up to 4 at once, and then check in Snowflake that all batches finished, at least 99.5% of rows arrived and keys are unique.

- [Account_Load](job_Account_Load.md): `dbo.account` → `ACCOUNT`
- [Account_Tag_Load](job_Account_Tag_Load.md): `dbo.account_tag` → `ACCOUNT_TAG`
- [Calls_Load](job_Calls_Load.md): `dbo.calls` → `CALLS`
- [Consumer_Load](job_Consumer_Load.md): `dbo.consumer` → `CONSUMER`
- [Consumer_Tag_Load](job_Consumer_Tag_Load.md): `dbo.consumer_tag` → `CONSUMER_TAG`
- [Notice_Account_Load](job_Notice_Account_Load.md): `dbo.notice_account` → `NOTICE_ACCOUNT`
- [Notice_letter_Load](job_Notice_letter_Load.md): `dbo.notice_letter` → `NOTICE_LETTER`
- [Notice_Text_Load](job_Notice_Text_Load.md): `dbo.notice_text` → `NOTICE_TEXT`
- [Notice_Validation_Load](job_Notice_Validation_Load.md): `dbo.notice_validation` → `NOTICE_VALIDATION`
- [Payment_Schedule_Instance_Load](job_Payment_Schedule_Instance_Load.md): `dbo.payment_schedule_instance` → `PAYMENT_SCHEDULE_INSTANCE`
- [Phone_Numbers_Load](job_Phone_Numbers_Load.md): `dbo.phone_number` → `PHONE_NUMBER`
- [Tbl_Fa_Consumer_Texting_Ack_3p_Hist_Load](job_Tbl_Fa_Consumer_Texting_Ack_3p_Hist_Load.md): `dbo.tbl_fa_consumer_texting_ack_3p_hist` → `TBL_FA_CONSUMER_TEXTING_ACK_3P_HIST`
- [Transactions_Load](job_Transactions_Load.md): `dbo.transactions` → `TRANSACTIONS`

### Single-pass loaders (FULL load is one truncate-and-insert)

Same INCR path as the batched loaders; FULL reads and writes the whole table in one pass with no batching or post-load validation.

- [Client_Load](job_Client_Load.md): `dbo.client` → `CLIENT`
- [Creditor_Transaction_Load](job_Creditor_Transaction_Load.md): `dbo.creditor_transaction` → `CREDITOR_TRANSACTION`
- [Email_Address_Load](job_Email_Address_Load.md): `dbo.email_address` → `EMAIL_ADDRESS`. **Different INCR logic:** deletes and re-inserts all rows per changed `CONSUMERID` instead of a `ROW_HASH` MERGE.
- [Notice_Email_Load](job_Notice_Email_Load.md): `dbo.notice_email` → `NOTICE_EMAIL`
- [Payment_Schecule_Account_Load](job_Payment_Schecule_Account_Load.md): `dbo.payment_schedule_account` → `PAYMENT_SCHEDULE_ACCOUNT`
- [Payment_Schecule_Summary_Load](job_Payment_Schecule_Summary_Load.md): `dbo.payment_schedule_summary` → `PAYMENT_SCHEDULE_SUMMARY`
- [Tbl_Enotice_Email_Resp_Load](job_Tbl_Enotice_Email_Resp_Load.md): `dbo.tbl_enotice_email_resp` → `TBL_ENOTICE_EMAIL_RESP`
- [Tbl_Enotice_To_Fand_Load](job_Tbl_Enotice_To_Fand_Load.md): `dbo.tbl_enotice_to_fand` → `TBL_ENOTICE_TO_FAND`
- [Tbl_Fa_Consumer_Texting_Resp_3p_Hist_Load](job_Tbl_Fa_Consumer_Texting_Resp_3p_Hist_Load.md): `dbo.tbl_fa_consumer_texting_resp_3p_hist` → `TBL_FA_CONSUMER_TEXTING_RESP_3P_HIST`
- [Vmdrops_Load](job_Vmdrops_Load.md): `dbo.vmdrops` → `VMDROPS`
- [VoApps_Load](job_VoApps_Load.md): `dbo.voapps` → `VOAPPS` (the only loader that trims whitespace on every text column)

### Retired jobs (`Older_Inactive_Jobs`; do not schedule)

Old-style truncate-and-reload jobs with no bookmark or run logging.

- [Account_Load_Copy](job_Account_Load_Copy.md): writes `ACCOUNT`, which is now owned by `Account_Load`. Running it would put the bookmark out of step.
- [CommTexts_Load](job_CommTexts_Load.md): `dbo.commtexts` → `COMMTEXTS`
- [Debtor_Load](job_Debtor_Load.md): `dbo.debtor` → `DEBTOR`
- [Emails_Load](job_Emails_Load.md): `dbo.emails` → `EMAILS`
- [Letters_Load](job_Letters_Load.md): `dbo.letters` → `LETTERS`
- [Texts_Load](job_Texts_Load.md): `dbo.texts` → `TEXTS`
- [Validation_Load](job_Validation_Load.md): `dbo.validation` → `VALIDATION`

_No reverse-direction (Snowflake → file) exports were found in this project's metadata._

## Full Alphabetical Table

| Job | Status | Target table |
|---|---|---|
| [Account_Load](job_Account_Load.md) | Active (batched) | ACCOUNT |
| [Account_Load_Copy](job_Account_Load_Copy.md) | Retired | ACCOUNT |
| [Account_Tag_Load](job_Account_Tag_Load.md) | Active (batched) | ACCOUNT_TAG |
| [BIDATA_Load_Summary_Alert](job_BIDATA_Load_Summary_Alert.md) | Utility | — (reads run log, sends email) |
| [BIDATA_Schema_Deploy](job_BIDATA_Schema_Deploy.md) | Utility (one-off) | — (DDL for all BIDATA tables) |
| [Calls_Load](job_Calls_Load.md) | Active (batched) | CALLS |
| [Client_Load](job_Client_Load.md) | Active (single-pass) | CLIENT |
| [CommTexts_Load](job_CommTexts_Load.md) | Retired | COMMTEXTS |
| [Consumer_Load](job_Consumer_Load.md) | Active (batched) | CONSUMER |
| [Consumer_Tag_Load](job_Consumer_Tag_Load.md) | Active (batched) | CONSUMER_TAG |
| [Creditor_Transaction_Load](job_Creditor_Transaction_Load.md) | Active (single-pass) | CREDITOR_TRANSACTION |
| [Debtor_Load](job_Debtor_Load.md) | Retired | DEBTOR |
| [Email_Address_Load](job_Email_Address_Load.md) | Active (single-pass) | EMAIL_ADDRESS |
| [Emails_Load](job_Emails_Load.md) | Retired | EMAILS |
| [Letters_Load](job_Letters_Load.md) | Retired | LETTERS |
| [Notice_Account_Load](job_Notice_Account_Load.md) | Active (batched) | NOTICE_ACCOUNT |
| [Notice_Email_Load](job_Notice_Email_Load.md) | Active (single-pass) | NOTICE_EMAIL |
| [Notice_letter_Load](job_Notice_letter_Load.md) | Active (batched) | NOTICE_LETTER |
| [Notice_Text_Load](job_Notice_Text_Load.md) | Active (batched) | NOTICE_TEXT |
| [Notice_Validation_Load](job_Notice_Validation_Load.md) | Active (batched) | NOTICE_VALIDATION |
| [Payment_Schecule_Account_Load](job_Payment_Schecule_Account_Load.md) | Active (single-pass) | PAYMENT_SCHEDULE_ACCOUNT |
| [Payment_Schecule_Summary_Load](job_Payment_Schecule_Summary_Load.md) | Active (single-pass) | PAYMENT_SCHEDULE_SUMMARY |
| [Payment_Schedule_Instance_Load](job_Payment_Schedule_Instance_Load.md) | Active (batched) | PAYMENT_SCHEDULE_INSTANCE |
| [Phone_Numbers_Load](job_Phone_Numbers_Load.md) | Active (batched) | PHONE_NUMBER |
| [Tbl_Enotice_Email_Resp_Load](job_Tbl_Enotice_Email_Resp_Load.md) | Active (single-pass) | TBL_ENOTICE_EMAIL_RESP |
| [Tbl_Enotice_To_Fand_Load](job_Tbl_Enotice_To_Fand_Load.md) | Active (single-pass) | TBL_ENOTICE_TO_FAND |
| [Tbl_Fa_Consumer_Texting_Ack_3p_Hist_Load](job_Tbl_Fa_Consumer_Texting_Ack_3p_Hist_Load.md) | Active (batched) | TBL_FA_CONSUMER_TEXTING_ACK_3P_HIST |
| [Tbl_Fa_Consumer_Texting_Resp_3p_Hist_Load](job_Tbl_Fa_Consumer_Texting_Resp_3p_Hist_Load.md) | Active (single-pass) | TBL_FA_CONSUMER_TEXTING_RESP_3P_HIST |
| [Texts_Load](job_Texts_Load.md) | Retired | TEXTS |
| [Transactions_Load](job_Transactions_Load.md) | Active (batched) | TRANSACTIONS |
| [Validation_Load](job_Validation_Load.md) | Retired | VALIDATION |
| [Vmdrops_Load](job_Vmdrops_Load.md) | Active (single-pass) | VMDROPS |
| [VoApps_Load](job_VoApps_Load.md) | Active (single-pass) | VOAPPS |
