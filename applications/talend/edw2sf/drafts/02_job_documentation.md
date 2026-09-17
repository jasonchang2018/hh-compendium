# Job-by-Job Documentation

> **Data-source caveat:** This documentation is generated from metadata extracted from `C:\H&H\Repo\compendium\automation\talend-documentation\full-documentation\working\edw2sf`. Signals found in the data suggest it may not represent a real production platform: All 9 defined DB connection(s) have empty host/port/database/schema fields — not configured for real use. The documents below describe exactly what is present in the extracted metadata; treat any "production" framing with that in mind and verify with the team before relying on it operationally.

289 job(s) across 1 project(s). Grouped by inferred kind rather than one write-up per job, so large sets of near-identical tutorial/demo jobs don't drown out the jobs that actually move data.

## Kind breakdown

| Kind | Count | What it means |
|---|---|---|
| utility | 147 | Neither a clear pipeline nor a named component match |
| read-only / preview | 109 | Reads data but only logs/previews it — no persisted output |
| etl-pipeline | 18 | Has both a source and a target component — the jobs that resemble a real data pipeline |
| orchestration | 14 | Calls other jobs via tRunJob |
| code-only | 1 | Custom Java/Groovy code only, no source/target components |

## ETL-pipeline jobs (source→transform→target)

| Job | Project | Description | Risk flags |
|---|---|---|---|
| `CUBS_EMail_Address_Load` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `CUBS_Raw_EMail_Address_Load` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `Copy_of_i3_DialerCallListTOL_Load_Backup` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `DoNotCall_Load` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tFilterRow', 'tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava', 'tJavaRow']) — logic not visible from metadata alone |
| `DoNotCall_Load_Full` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava', 'tJavaRow']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `EncryptValue_ContextVariable` | EDW2SF | Reads via ['tFileInputProperties', 'tFixedFlowInput'], writes via ['tFileOutputProperties']. | Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `Initial_Ins_Discovery_V2_Decrypted` | EDW2SF | Reads via ['tFileInputDelimited'], writes via ['tFileOutputDelimited']. | Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `Initial_Insurance_Discovery_File` | EDW2SF | Reads via ['tFileInputDelimited'], writes via ['tFileOutputDelimited']. | Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `Insurance_Discovery_Test` | EDW2SF | Reads via ['tFileInputExcel'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `Livevox_Sample_Load` | EDW2SF | Reads via ['tFileInputDelimited'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone |
| `LoadLegalRpt20231130` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tAggregateRow', 'tFilterRow', 'tMap', 'tSortRow'], writes via ['tFileOutputDelimited']. | Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `Test_Decryption` | EDW2SF | Reads via ['tFileInputDelimited'], writes via ['tFileOutputDelimited']. | Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `i3_DialerCallListCO_Load` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `i3_DialerCallListCO_Load_Backup` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `i3_DialerCallListDC_Load_Backup` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `i3_DialerCallListHH_Load_Backup` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `i3_DialerCallListTOL_Load` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `i3_DialerCallListTOL_Load_Backup` | EDW2SF | Reads via ['tFileInputDelimited'], transforms via ['tMap'], writes via ['tFileOutputDelimited']. | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |

## Orchestration jobs (tRunJob chains)

| Job | Calls | Risk flags |
|---|---|---|
| `CO_Master_Load` | CUBS_Raw_CO_Client_Load, CUBS_Raw_CO_Debtor_Load, CUBS_Raw_CO_ETL_Load, CUBS_Raw_Cellphone_Load, CUBS_Raw_DeskInfo_Load, CUBS_Raw_EM_Load, CUBS_Raw_Empinfo_Load, CUBS_Raw_Letter_Load, CUBS_Raw_Trans_Load, DimFiscal_CO_Load | Uses error-handling/demo components: ['tWarn']; Embeds custom code components (['tJava', 'tJavaRow']) — logic not visible from metadata alone |
| `CUBS_PostDates_Load` | CUBS_Raw_PostDate_Load | Uses error-handling/demo components: ['tDie', 'tWarn']; Embeds custom code components (['tJava', 'tJavaRow']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `CUBS_Raw_Debtor_Load` | CUBS_Raw_CHI_Debtor_Load, CUBS_Raw_CO_Debtor_Load, CUBS_Raw_DC_Debtor_Load, CUBS_Raw_HH_Debtor_Load, CUBS_Raw_PRE_Debtor_Load | Embeds custom code components (['tJava']) — logic not visible from metadata alone |
| `CUBS_Raw_Debtor_Load_Test` | CUBS_Raw_DC_Debtor_Load_No_Delete | Embeds custom code components (['tJava']) — logic not visible from metadata alone |
| `CUBS_Raw_ETL_Load` | CUBS_Raw_CHI_ETL_Load, CUBS_Raw_CO_ETL_Load, CUBS_Raw_DC_ETL_Load, CUBS_Raw_HH_ETL_Load, CUBS_Raw_PRE_ETL_Load, CUBS_Raw_TOL_ETL_Load | Embeds custom code components (['tJava']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `DimCellphone_Load` | CUBS_Raw_Cellphone_Load | Uses error-handling/demo components: ['tDie', 'tWarn']; Embeds custom code components (['tJava', 'tJavaRow']) — logic not visible from metadata alone; Has a credential-like parameter (redacted in extraction) — verify the secret is managed properly, not hardcoded in the job |
| `DimDeskInfo_Load` | CUBS_Raw_File_Load | Uses error-handling/demo components: ['tDie', 'tWarn']; Embeds custom code components (['tJavaRow']) — logic not visible from metadata alone |
| `DimEmployeeInfo_Load` | CUBS_Raw_File_Load | Uses error-handling/demo components: ['tDie', 'tWarn']; Embeds custom code components (['tJavaRow']) — logic not visible from metadata alone |
| `EMail_Address_Load` | CUBS_Raw_EMail_Address_Load | Embeds custom code components (['tJava']) — logic not visible from metadata alone |
| `Export_Hermes_APC_Master_Prediction` | master_prediction_proposal_cubs_extract | Embeds custom code components (['tJava']) — logic not visible from metadata alone |
| `Extract_Hermes_Master_Prediction` | master_prediction_proposal_cubs_extract | Embeds custom code components (['tJava']) — logic not visible from metadata alone |
| `Fact_Electronic_Media_Load` | CUBS_Raw_File_Load | Uses error-handling/demo components: ['tDie', 'tWarn']; Embeds custom code components (['tJavaRow']) — logic not visible from metadata alone |
| `HealthPartners_Close_Rpt_Master` | HealthPartners_Close_Reports_Extract | — |
| `PaymentPlan_Load` | CUBS_Raw_File_Load | Uses error-handling/demo components: ['tDie', 'tWarn']; Embeds custom code components (['tJavaRow']) — logic not visible from metadata alone |

## Read-only / preview jobs

| Job | Description |
|---|---|
| `ADP_Employee_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ADP_Employee_Raw_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ADP_Payroll_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ADP_Roster_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Backfill_Debtor_Cell_Phone_f83` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Backfill_Debtor_Phones` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Bad_Phone_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CFDAILY_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CLT_XFR_DT_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CO_DEBTOR_SPECIAL_BACKFILL_LOAD` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CO_Debtor_TrueUp` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CRPLoad` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Activity_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CHI_Client_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CHI_Debtor_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CHI_Debtor_Load_No_Delete` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CHI_Debtor_Load_Upsert` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CHI_ETL_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CO_Client_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CO_Debtor_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CO_Debtor_Load_No_Delete` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CO_Debtor_Load_Upsert` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_CO_ETL_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Cellphone_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Client_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_DC_Client_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_DC_Debtor_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_DC_Debtor_Load_No_Delete` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_DC_Debtor_Load_Upsert` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_DC_ETL_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_DeskInfo_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_EM_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Empinfo_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_HH_Client_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_HH_Debtor_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_HH_Debtor_Load_No_Delete` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_HH_Debtor_Load_Upsert` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_HH_ETL_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Letter_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_PRE_Client_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_PRE_Debtor_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_PRE_Debtor_Load_No_Delete` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_PRE_Debtor_Load_Upsert` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_PRE_ETL_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Payplan_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_PostDate_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_TOL_Client_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_TOL_Debtor_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_TOL_ETL_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Trans_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CUBS_Raw_Trans_Load_Special` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Collector_Payment_Detail_Load` | Reads via ['tFileInputExcel']; no output target found in the extracted metadata. |
| `DEBTOR_UPDATES_20230807` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `DIMDEBTOR_FISCALS_20230713` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Daily_Fee_Projection_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Debtor_Deleted_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Debtor_Status_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Debtor_Status_Load_MSSQL` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Debtor_Strat_Backfill` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Dialer_Grp_Transform_Inputs_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ERC_Event_Report_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ETR_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Employee_Collector_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `HH_DEBTOR_SPECIAL_20231016_LOAD` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `HH_TRANS_NORTHSHORE_LOAD` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `HH_VAL_LTR_DATE_Backfill` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `HOPE_Credit_Request` | Reads via ['tMysqlInput']; no output target found in the extracted metadata. |
| `HOPE_Goals_Load` | Reads via ['tMysqlInput']; no output target found in the extracted metadata. |
| `HOPE_Notes_Load` | Reads via ['tMysqlInput']; no output target found in the extracted metadata. |
| `HOPE_SPTransactions_Load` | Reads via ['tMysqlInput']; no output target found in the extracted metadata. |
| `HOPE_Transactions_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `INPUT_DIALER_LIST_GOV_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `INPUT_DIALER_LIST_HC_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Ins_Cvg_Debtor_NPI_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Insurance_Discovery_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Livevox_Daily_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Load_837_Files` | Reads via ['tFileInputRaw']; no output target found in the extracted metadata. |
| `Load_Attunely_Data` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Load_Employee_Collector_History` | Reads via ['tFileInputExcel']; no output target found in the extracted metadata. |
| `Load_Evergreen_Hours` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Load_HH_Debtor_Special_20251222` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Mail_Merge_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `MaxRTE_Result_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Migrating_Clients_20260424` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Northwestern_Future_Appts` | Reads via ['tFileInputExcel']; no output target found in the extracted metadata. |
| `Notes_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `PA_Turnpike_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `PCI_LETTERS_TO_DELETE` | Reads via ['tFileInputExcel']; no output target found in the extracted metadata. |
| `PDC_Plan_Txn_Backfill` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `PV_PostDate_Export_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `PaymentVision_Activity_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ProInsight_Analytics_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ProInsight_CCU_Scorecard_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ProInsight_CCU_Scorecard_V2_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ProInsight_HPS_Scorecard_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ProInsight_Scorecard_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Raw_PCI_Letter_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `SMS_IC_Inbound_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `SMS_IC_Outbound_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `SMS_IC_Outbound_Load_Backfill` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `SMS_Inbound_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `SMS_Outbound_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `SendGrid_Report_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Skip_Costs_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Touchstar_DNC_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Trans_History_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `VAT_1394_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `VA_Tax_Report_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Voapp_File_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |

## Utility jobs

| Job | Description |
|---|---|
| `Activity_Load_Daily` | Utility/demo job using: ['tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Activity_Load_Legacy` | Utility/demo job using: ['tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `AgentKPI_Daily_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Avita_Monthly_Report_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileDelete', 'tFileExist', 'tFileOutputDelimited', 'tFileRowCount', 'tFilterRow', 'tFlowMeter', 'tJava', 'tPrejob', 'tSendMail', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `CHI_E_Media_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `CO_E_Media_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `CREATE_RAW_CUBS_CLIENT` | Utility/demo job using: ['tCreateTable', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection']. Not a source-to-target data pipeline. |
| `CUBS_Raw_File_Load` | Utility/demo job using: ['tJava', 'tJavaRow', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSystem']. Not a source-to-target data pipeline. |
| `CallDetail_40_Load_History` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `Call_Campaign_Results_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Callminer_HH_Metadata_Daily_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Carle_Asset_Scrub` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tPrejob', 'tSendMail', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `City_of_Phi_C1A_PDR_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Client_NonCUBS_Attributes` | Utility/demo job using: ['tMSSqlInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Columbia_Doctors_Legal_Rpt` | Utility/demo job using: ['tAggregateRow', 'tDataDecrypt', 'tFileOutputDelimited', 'tFilterRow', 'tReservoirSampling', 'tSendMail', 'tSetKeystore', 'tSnowflakeInput', 'tSortRow']. Not a source-to-target data pipeline. |
| `DC_Call_Contact_Exceptions_1` | Utility/demo job using: ['tFileOutputDelimited', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `DC_Call_Contact_Exceptions_2` | Utility/demo job using: ['tFileArchive', 'tFileDelete', 'tFileList', 'tSendMail', 'tSleep']. Not a source-to-target data pipeline. |
| `DC_E_Media_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `DC_SSN_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tParallelize', 'tPrejob', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `DNIS_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `DNIS_Org_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `Debtor_Derived_Load` | Utility/demo job using: ['tJava', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeRow', 'tSystem']. Not a source-to-target data pipeline. |
| `DimClient_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tParallelize', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `DimDate_Load` | Utility/demo job using: ['tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `DimDebtor_Load` | Utility/demo job using: ['JDBCClose', 'JDBCConnection', 'tFlowMeter', 'tJDBCSCDELT', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimDebtor_NewFields_Load` | Utility/demo job using: ['tDataEncrypt', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `DimDepartment_and_GL_Load` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tParallelize', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `DimFiscal_CHI_Load` | Utility/demo job using: ['tJava', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimFiscal_CO_Load` | Utility/demo job using: ['tJava', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimFiscal_DC_Load` | Utility/demo job using: ['tJava', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimFiscal_HH_B_TrueUp` | Utility/demo job using: ['tDataEncrypt', 'tMSSqlInput', 'tMap', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `DimFiscal_HH_Load` | Utility/demo job using: ['tJava', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimFiscal_PRE_Load` | Utility/demo job using: ['tJava', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimFiscal_TOL_Load` | Utility/demo job using: ['tJava', 'tParallelize', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimScore_Load` | Utility/demo job using: ['tFilterRow', 'tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tParallelize', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `DimStatus_Load` | Utility/demo job using: ['tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `EmployeeHrsWorked_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `EmployeeRates_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Encrypt_CHI_Fiscal_Tax_Code` | Utility/demo job using: ['tDataEncrypt', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `Encrypt_CO_Fiscal_A_F18_A` | Utility/demo job using: ['tDataEncrypt', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Equibli_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_CHI_Hermes_Decile` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_CO_Hermes_Decile` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_DC_Hermes_Decile` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_DDNPII` | Utility/demo job using: ['tJava', 'tSystem']. Not a source-to-target data pipeline. |
| `Extract_Equabli_GOV` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_Equabli_HC_Validation_Score` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_Equabli_Reports` | Utility/demo job using: ['tFileOutputDelimited', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_Equibli_Test` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_HH_Hermes_Decile` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_HH_Hermes_ValDecile` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_Letter_Count` | Utility/demo job using: ['TableauOutput', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_Letter_Count_to_Hyper` | Utility/demo job using: ['tJava', 'tJavaRow', 'tLibraryLoad', 'tPostjob', 'tPrejob', 'tREST', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_MSSQL_COCHI_Debtor` | Utility/demo job using: ['tDataEncrypt', 'tMSSqlInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Extract_No_Dialer_Test_CHI` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_No_Dialer_Test_CO` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_No_Dialer_Test_DC` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_No_Dialer_Test_HH` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_No_Dialer_Test_TOL` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_PRE_Hermes_Decile` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_ProInsights_Data` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Extract_TOL_Hermes_Decile` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `FactLetter_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tJavaRow', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `FactPaymentManager_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `FactPostDates_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tJavaRow', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `FactTrans_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `FactTrans_TCODE_COLLECTOR_Load` | Utility/demo job using: ['tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutputBulkExec']. Not a source-to-target data pipeline. |
| `Fran_Bai_Backlog` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `HH_EMedia_Load` | Utility/demo job using: ['tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeOutputBulkExec']. Not a source-to-target data pipeline. |
| `HH_E_Media_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `HUB_Departments_Load` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `HUB_HH_Employee_Load` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `HUB_Segments_Load` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `HUB_Teams_Load` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `HUB_TempTransaction_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `HUB_Transactions_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutputBulkExec']. Not a source-to-target data pipeline. |
| `HealthPartners_Close_Reports_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `I3_CALLDETAIL_DEDOR_LOAD` | Utility/demo job using: ['tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `IDOR_Amnesty_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `ISO_Request_Export` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Insurance_Discovery_Scrub_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tJavaRow', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Insurance_Report_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_COC_Water_Scrub` | Utility/demo job using: ['tFileDelete', 'tFileExist', 'tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSendMail', 'tSetKeystore', 'tSleep', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Carle_Asset_Scrub` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSendMail', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Dashboard_Base_Report` | Utility/demo job using: ['tFileOutputDelimited', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Dashboard_By_Agent` | Utility/demo job using: ['tFileDelete', 'tFileExist', 'tFileOutputDelimited', 'tJava', 'tPrejob', 'tSetKeystore', 'tSleep', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Dashboard_By_Metric` | Utility/demo job using: ['tFileDelete', 'tFileExist', 'tFileOutputDelimited', 'tJava', 'tPrejob', 'tSetKeystore', 'tSleep', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Delaware_Focus_Attributes` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Delaware_Focus_Attributes_Granular` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Delaware_Scorecard_Report` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Deleware_Audit_Scorecard` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_HPS_Audit_Scorecard` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_HPS_Focus_Attributes` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_HPS_Focus_Attributes_Granular` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Insurance_Pmt_Tracking` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSendMail', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Lurie_Audit_Scorecard` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Lurie_Focus_Attributes` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Lurie_Focus_Attributes_Granular` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Manual_Audit_Scorecard` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_ProMedica_Scrub` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSendMail', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_Property_Scrub` | Utility/demo job using: ['tDataDecrypt', 'tFileDelete', 'tFileExist', 'tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSleep', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_REPORTS` | Utility/demo job using: ['tFileOutputDelimited', 'tParallelize', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_REPORTS_2` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tParallelize', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `LW_TPL_PMT_REPORT` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Last4SSN_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFilterRow', 'tJavaRow', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `LegalMatch_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tFilterRow', 'tForeach', 'tJava', 'tJoin', 'tPrejob', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSortRow']. Not a source-to-target data pipeline. |
| `Legal_Asset_Scrub_Champaign_County_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Legal_Asset_Scrub_Illinois_Counties_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputExcel', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Legal_Asset_Scrub_Illinois_Counties_Extract_2` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tJava', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Legal_Asset_Scrub_KDOR_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Load_Debtor_New_Columns` | Utility/demo job using: ['tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `Load_Misc_Dims` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tParallelize', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Load_PCI_Letter_Disp_Desc` | Utility/demo job using: ['tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `MBoich_Experian_Extracts` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tParallelize', 'tPrejob', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `MaxRTE_Request_Export` | Utility/demo job using: ['tDataDecrypt', 'tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tJavaRow', 'tPrejob', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `PCI_Letter_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `PRE_E_Media_Load` | Utility/demo job using: ['tFlowMeter', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `PaymentPlan_Legacy_Load` | Utility/demo job using: ['tMSSqlInput', 'tMap', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Semaphore_Check` | Utility/demo job using: ['tFileExist', 'tForeach', 'tParallelize', 'tSendMail', 'tWarn']. Not a source-to-target data pipeline. |
| `TEST_Avita_Monthly_Report_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFileDelete', 'tFileOutputDelimited', 'tFileRowCount', 'tFilterRow', 'tFlowMeter', 'tJava', 'tPrejob', 'tSendMail', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `TEST_Email_Alerts` | Utility/demo job using: ['tSendMail']. Not a source-to-target data pipeline. |
| `Test_Encryption` | Utility/demo job using: ['tDataEncrypt', 'tFileOutputDelimited', 'tMSSqlInput']. Not a source-to-target data pipeline. |
| `Top_N_Accounts_All_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Top_N_Accounts_Extract` | Utility/demo job using: ['tFileOutputDelimited', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `VA_Tax_Inventory_Report` | Utility/demo job using: ['tDataDecrypt', 'tFileDelete', 'tFileExist', 'tFileOutputDelimited', 'tJava', 'tPrejob', 'tSendMail', 'tSetKeystore', 'tSleep', 'tSnowflakeConnection', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `VA_Tax_Report_Split` | Utility/demo job using: ['tFileOutputDelimited', 'tFileOutputExcel', 'tFlowToIterate', 'tJava', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `i3_AgentActivityLog_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tJava', 'tJavaRow', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutputBulkExec', 'tSnowflakeRow', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `i3_AgentQueueStats_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `i3_AgentStats` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `i3_CRC_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `i3_CallDetail_40_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tJavaRow', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `i3_CallDetail_40_Load_Copy` | Utility/demo job using: ['tFileOutputExcel', 'tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `i3_CallDetail_viw_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tJavaRow', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutputBulkExec', 'tSnowflakeRow', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `i3_CallHistory_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `i3_Call_Detail_View_Init_Load` | Utility/demo job using: ['tMSSqlInput']. Not a source-to-target data pipeline. |
| `i3_Campaign_Type_Load` | Utility/demo job using: ['tFlowMeter', 'tFlowMeterCatcher', 'tLogRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput', 'tStatCatcher']. Not a source-to-target data pipeline. |
| `i3_DialerCallListCHI_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_DialerCallListDC_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_DialerCallListHH_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput', 'tSnowflakeRow']. Not a source-to-target data pipeline. |
| `i3_DialerCallListPRE_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_DialerCallList_DEDOR_Load` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_Individual_Load` | Utility/demo job using: ['tFlowMeter', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_InteractionCustomAttributes_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_InteractionSummaryEx_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_InteractionSummary_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `i3_InteractionWrapup_Load` | Utility/demo job using: ['tFlowMeter', 'tJava', 'tJavaRow', 'tMSSqlClose', 'tMSSqlConnection', 'tMSSqlInput', 'tMap', 'tPostjob', 'tPrejob', 'tSetKeystore', 'tSnowflakeClose', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `master_prediction_proposal_cubs_extract` | Utility/demo job using: ['tFileOutputDelimited', 'tFlowMeter', 'tJava', 'tPrejob', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |

## Code-only jobs

| Job | Description |
|---|---|
| `TEST_Date_Params` | Runs custom code only (Java/Groovy) — no file/DB source or target components. Purpose not determinable beyond the component list; verify with team. |
