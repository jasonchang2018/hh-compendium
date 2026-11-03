# Dependency Matrix

## Overview

This matrix shows what each of the 33 `FAMIGRATION` jobs depends on: its source and target tables, the BIDATA control tables it reads or writes, the context variables it relies on, and how it performs a FULL load. Read each row as "this job needs these things to run correctly." No job calls another (there is no `tRunJob` anywhere in the project), so there is still no job-to-job column. The new dependencies are **data** dependencies: every active loader now relies on `dbo.SF_ChangeLog` on SQL Server and on `ETL_BOOKMARK`, the run-log tables and its own pair of staging tables in Snowflake, all of which must exist (via `BIDATA_Schema_Deploy`) before the loader can run.

## Matrix Table

### Active loaders

All 24 active loaders read `dbo.SF_ChangeLog`; read and update `ETL_BOOKMARK`; write `ETL_JOB_RUN_LOG` and `ETL_JOB_RUN_STEP`; write `STG_CHANGED_<TARGET>` and `STG_CHANGED_<TARGET>_KEYS`; and use context variables `keystorePath`, `LAST_CHANGE_ID`, `LAST_RUN_DTTM`, `MAX_CHANGE_ID` and `LOAD_MODE`. The columns below show only what differs.

| Job | Source (SQL Server `dbo`) | Target (Snowflake `BIDATA`) | Merge key | FULL style | Extra context variables |
|---|---|---|---|---|---|
| Account_Load | account | ACCOUNT | ACCOUNTID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Account_Tag_Load | account_tag | ACCOUNT_TAG | ACCOUNT_TAG_ID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Calls_Load | calls | CALLS | ARLOGID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Client_Load | client | CLIENT | CLIENT_IDX | Single-pass | — |
| Consumer_Load | consumer | CONSUMER | CONSUMERID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Consumer_Tag_Load | consumer_tag | CONSUMER_TAG | CONSUMER_TAG_ID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Creditor_Transaction_Load | creditor_transaction | CREDITOR_TRANSACTION | CREDITOR_TRANSACTION_ID | Single-pass | — |
| Email_Address_Load | email_address | EMAIL_ADDRESS | CONSUMERID (delete + re-insert) | Single-pass | — |
| Notice_Account_Load | notice_account | NOTICE_ACCOUNT | NOTICE_ACCOUNT_ID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Notice_Email_Load | notice_email | NOTICE_EMAIL | NOTICEID | Single-pass | — |
| Notice_letter_Load | notice_letter | NOTICE_LETTER | NOTICEID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Notice_Text_Load | notice_text | NOTICE_TEXT | NOTICEID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Notice_Validation_Load | notice_validation | NOTICE_VALIDATION | NOTICEID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Payment_Schecule_Account_Load | payment_schedule_account | PAYMENT_SCHEDULE_ACCOUNT | PAYMENT_SCHEDULE_ACCOUNT_ID | Single-pass | — |
| Payment_Schedule_Instance_Load | payment_schedule_instance | PAYMENT_SCHEDULE_INSTANCE | PAYMENT_SCHEDULE_INSTANCE_ID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Payment_Schecule_Summary_Load | payment_schedule_summary | PAYMENT_SCHEDULE_SUMMARY | PAYMENT_SCHEDULE_ID | Single-pass | — |
| Phone_Numbers_Load | phone_number | PHONE_NUMBER | PHONE_ID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Tbl_Enotice_Email_Resp_Load | tbl_enotice_email_resp | TBL_ENOTICE_EMAIL_RESP | ID | Single-pass | — |
| Tbl_Enotice_To_Fand_Load | tbl_enotice_to_fand | TBL_ENOTICE_TO_FAND | RECON_STATUS_ID | Single-pass | — |
| Tbl_Fa_Consumer_Texting_Ack_3p_Hist_Load | tbl_fa_consumer_texting_ack_3p_hist | TBL_FA_CONSUMER_TEXTING_ACK_3P_HIST | TEXT_ID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Tbl_Fa_Consumer_Texting_Resp_3p_Hist_Load | tbl_fa_consumer_texting_resp_3p_hist | TBL_FA_CONSUMER_TEXTING_RESP_3P_HIST | RESPONSE_ID | Single-pass | — |
| Transactions_Load | transactions | TRANSACTIONS | TRANS_ID | Batched | `BATCH_SIZE`, `PARALLEL_BATCHES` |
| Vmdrops_Load | vmdrops | VMDROPS | ARLOGID | Single-pass | — |
| VoApps_Load | voapps | VOAPPS | VOAPPS_ID | Single-pass | — |

### BIDATA utility jobs

| Job | Reads | Writes | Context variables |
|---|---|---|---|
| [BIDATA_Schema_Deploy](talend/FAMIGRATION/job_BIDATA_Schema_Deploy.md) | `INFORMATION_SCHEMA` (verification) | Alters the 24 target tables; creates/seeds `ETL_BOOKMARK`, 48 `STG_CHANGED_*` tables, `ETL_JOB_RUN_LOG`, `ETL_JOB_RUN_STEP` | `keystorePath` |
| [BIDATA_Load_Summary_Alert](talend/FAMIGRATION/job_BIDATA_Load_Summary_Alert.md) | `ETL_BOOKMARK`, `ETL_JOB_RUN_LOG` | Email only (SMTP) | `keystorePath`, `emailRecipients`, `emailCC`, `LOOKBACK_HOURS`, `SEND_ONLY_ON_ISSUES` |

### Retired jobs (`Older_Inactive_Jobs`)

| Job | Source | Target | Table emptied before load? | Uses bookmark/run log? |
|---|---|---|---|---|
| Account_Load_Copy | dbo.account | ACCOUNT | Yes | No |
| CommTexts_Load | dbo.commtexts | COMMTEXTS | Yes | No |
| Debtor_Load | dbo.debtor | DEBTOR | Yes | No |
| Emails_Load | dbo.emails | EMAILS | Yes | No |
| Letters_Load | dbo.letters | LETTERS | Yes | No |
| Texts_Load | dbo.texts | TEXTS | Yes | No |
| Validation_Load | dbo.validation | VALIDATION | Yes | No |

All jobs connect to the same SQL Server (`10.1.40.7:1433`) and Snowflake account (`xca26579.us-east-1`, `EDWPRODHH.BIDATA`, warehouse `COMPUTE_WH`); that is omitted from the columns because it is identical on every row.

## Notes

- **Everything now depends on `BIDATA_Schema_Deploy` having run first.** The loaders assume `ROW_HASH`, the bookmark row, both staging tables and the run-log tables exist. This ordering is not enforced anywhere in Talend; it has to be handled at deployment time.
- **Everything also depends on `dbo.SF_ChangeLog`, which no Talend job maintains.** If that feed stops being written, every loader silently settles into NONE (no changes) and the tables go stale without any error. Because a NONE run is a normal outcome (logged with `LOAD_MODE = 'NONE'`), nothing in the metadata flags "no changes for days" as a problem; consider adding a staleness check to the alert.
- **The bookmark row is a hidden prerequisite.** Jobs only `UPDATE` `ETL_BOOKMARK`; the deploy script seeds the 24 rows. A table added later without a seeded row will reload FULL on every run and never appear in the alert email.
- **Connection details are still hardcoded in every job, not centralized.** All jobs type in the SQL Server host and login directly (with `trustServerCertificate=true`) rather than using the project's `Frostlake_0.1` connection (still empty and unused) or a context variable.
- **The one shared context variable, `keystorePath`, is effectively bypassed.** Every job's `tSetKeystore_1` has the keystore path typed in as `.../ssl/keystore.p12`, while `keystorePath` defaults to `.../.ssl/keystore.p12`. Changing the context variable will not change which file the jobs actually use.
- **Leftover/inert settings.** Several loaders carry an `upsertKeyColumn` that is not their real merge key (e.g. `Calls_Load` = `CALLIDKEY`, `Phone_Numbers_Load` / `Vmdrops_Load` / `Account_Load` = `DEBTOR_IDX`, `Consumer_Load` = `PACKET_IDX`, `Creditor_Transaction_Load` = `CONSUMERID`). These have no effect while the write mode is `INSERT`, but they will mislead anyone reading the job. Several jobs also carry unused schemas labelled `account`, left over from copying the Account loader.
- **Retired jobs still point at live tables.** `Account_Load_Copy` writes to `ACCOUNT`, which is now owned by the incremental `Account_Load`. Running it would desynchronise the bookmark. The other six retired jobs own tables (`COMMTEXTS`, `DEBTOR`, `EMAILS`, `LETTERS`, `TEXTS`, `VALIDATION`) that no active job loads any more.
- **Naming typo.** `Payment_Schecule_Account_Load` and `Payment_Schecule_Summary_Load` ("Schecule") load tables spelled correctly (`PAYMENT_SCHEDULE_*`); worth fixing before these job names get baked into schedules and run-log history.
