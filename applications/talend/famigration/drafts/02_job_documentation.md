# Job-by-Job Documentation

> **Data-source caveat:** This documentation is generated from metadata extracted from `C:\H_H\Repo\FAMigration-1594247393`. Signals found in the data suggest it may not represent a real production platform: All 1 defined DB connection(s) have empty host/port/database/schema fields — not configured for real use. The documents below describe exactly what is present in the extracted metadata; treat any "production" framing with that in mind and verify with the team before relying on it operationally.

33 job(s) across 1 project(s). Grouped by inferred kind rather than one write-up per job, so large sets of near-identical tutorial/demo jobs don't drown out the jobs that actually move data.

## Kind breakdown

| Kind | Count | What it means |
|---|---|---|
| utility | 33 | Neither a clear pipeline nor a named component match |

## Utility jobs

| Job | Description |
|---|---|
| `Account_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Account_Load_Copy` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeOutput', 'tMSSqlInput', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Account_Tag_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `BIDATA_Load_Summary_Alert` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'tJava', 'tJavaRow', 'tPrejob', 'tSendMail', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `BIDATA_Schema_Deploy` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeRow', 'tJavaRow', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Calls_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Client_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `CommTexts_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeOutput', 'tMSSqlInput', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Consumer_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Consumer_Tag_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Creditor_Transaction_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Debtor_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeOutput', 'tMSSqlInput', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Email_Address_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Emails_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeOutput', 'tMSSqlInput', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Letters_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeOutput', 'tMSSqlInput', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Notice_Account_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Notice_Email_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Notice_Text_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Notice_Validation_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Notice_letter_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Payment_Schecule_Account_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Payment_Schecule_Summary_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Payment_Schedule_Instance_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Phone_Numbers_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Tbl_Enotice_Email_Resp_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Tbl_Enotice_To_Fand_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Tbl_Fa_Consumer_Texting_Ack_3p_Hist_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Tbl_Fa_Consumer_Texting_Resp_3p_Hist_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Texts_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeOutput', 'tMSSqlInput', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Transactions_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tFlowToIterate', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Validation_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeOutput', 'tMSSqlInput', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `Vmdrops_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
| `VoApps_Load` | Utility/demo job using: ['SnowflakeConnection', 'SnowflakeInput', 'SnowflakeOutput', 'SnowflakeRow', 'tJava', 'tJavaRow', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSetKeystore']. Not a source-to-target data pipeline. |
