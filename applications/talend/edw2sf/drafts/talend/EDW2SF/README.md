# Talend Jobs Index — EDW2SF Project

289 jobs. Click any job name to open its full documentation. See [`../../01_system_architecture.md`](../../01_system_architecture.md), [`../../04_data_lineage_map.md`](../../04_data_lineage_map.md), [`../../05_operational_runbook.md`](../../05_operational_runbook.md), and [`../../06_dependency_matrix.md`](../../06_dependency_matrix.md) for the platform-wide picture, and [`../../06_dependency_matrix.md`](../../06_dependency_matrix.md) specifically for the full `tRunJob` orchestration graph.

## Orchestrator jobs (`tRunJob` chains — no direct data load of their own beyond a merge/dispatch step)

These jobs call other jobs listed elsewhere in this index; see each job's own doc for its full `tRunJob` sequence and `06_dependency_matrix.md` for the project-wide graph.

| Job | Target |
|---|---|
| [`CO_Master_Load`](job_CO_Master_Load.md) | orchestrator (see job list below) |
| [`CUBS_PostDates_Load`](job_CUBS_PostDates_Load.md) | orchestrator (see job list below) |
| [`CUBS_Raw_Debtor_Load`](job_CUBS_Raw_Debtor_Load.md) | orchestrator (see job list below) |
| [`CUBS_Raw_Debtor_Load_Test`](job_CUBS_Raw_Debtor_Load_Test.md) | orchestrator (see job list below) |
| [`CUBS_Raw_ETL_Load`](job_CUBS_Raw_ETL_Load.md) | orchestrator (see job list below) |
| [`DimCellphone_Load`](job_DimCellphone_Load.md) | orchestrator (see job list below) |
| [`DimDeskInfo_Load`](job_DimDeskInfo_Load.md) | orchestrator (see job list below) |
| [`DimEmployeeInfo_Load`](job_DimEmployeeInfo_Load.md) | orchestrator (see job list below) |
| [`EMail_Address_Load`](job_EMail_Address_Load.md) | orchestrator (see job list below) |
| [`Export_Hermes_APC_Master_Prediction`](job_Export_Hermes_APC_Master_Prediction.md) | orchestrator (see job list below) |
| [`Extract_Hermes_Master_Prediction`](job_Extract_Hermes_Master_Prediction.md) | orchestrator (see job list below) |
| [`Fact_Electronic_Media_Load`](job_Fact_Electronic_Media_Load.md) | orchestrator (see job list below) |
| [`HealthPartners_Close_Rpt_Master`](job_HealthPartners_Close_Rpt_Master.md) | orchestrator (see job list below) |
| [`PaymentPlan_Load`](job_PaymentPlan_Load.md) | orchestrator (see job list below) |

## `CUBS_Raw_*` per-site client/debtor/ETL loads

The core per-site raw-load family behind most `_Master_Load` orchestrators and `DimFiscal_*` jobs — client, debtor (including `_No_Delete`/`_Upsert` variants), transaction, and ETL loads for each site code (CHI, CO, DC, HH, PRE, TOL). Site codes are documented in `01_system_architecture.md`.

| Job | Target |
|---|---|
| [`CREATE_RAW_CUBS_CLIENT`](job_CREATE_RAW_CUBS_CLIENT.md) | — |
| [`CUBS_Raw_Activity_Load`](job_CUBS_Raw_Activity_Load.md) | CUBS_ACTIVITY_RAW_CURRENT |
| [`CUBS_Raw_CHI_Client_Load`](job_CUBS_Raw_CHI_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_CHI_Debtor_Load`](job_CUBS_Raw_CHI_Debtor_Load.md) | CUBS_DEBTOR_RAW_CHI_CURRENT |
| [`CUBS_Raw_CHI_Debtor_Load_No_Delete`](job_CUBS_Raw_CHI_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_CHI_CURRENT |
| [`CUBS_Raw_CHI_Debtor_Load_Upsert`](job_CUBS_Raw_CHI_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_CHI_CURRENT |
| [`CUBS_Raw_CHI_ETL_Load`](job_CUBS_Raw_CHI_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_CO_Client_Load`](job_CUBS_Raw_CO_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_CO_Debtor_Load`](job_CUBS_Raw_CO_Debtor_Load.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CUBS_Raw_CO_Debtor_Load_No_Delete`](job_CUBS_Raw_CO_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CUBS_Raw_CO_Debtor_Load_Upsert`](job_CUBS_Raw_CO_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CUBS_Raw_CO_ETL_Load`](job_CUBS_Raw_CO_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Cellphone_Load`](job_CUBS_Raw_Cellphone_Load.md) | CUBS_CELLPHONE_RAW |
| [`CUBS_Raw_Client_Load`](job_CUBS_Raw_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_DC_Client_Load`](job_CUBS_Raw_DC_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_DC_Debtor_Load`](job_CUBS_Raw_DC_Debtor_Load.md) | CUBS_DEBTOR_RAW_DC_CURRENT |
| [`CUBS_Raw_DC_Debtor_Load_No_Delete`](job_CUBS_Raw_DC_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_DC_CURRENT |
| [`CUBS_Raw_DC_Debtor_Load_Upsert`](job_CUBS_Raw_DC_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_DC_CURRENT |
| [`CUBS_Raw_DC_ETL_Load`](job_CUBS_Raw_DC_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_DeskInfo_Load`](job_CUBS_Raw_DeskInfo_Load.md) | CUBS_DESKINFO_RAW |
| [`CUBS_Raw_EM_Load`](job_CUBS_Raw_EM_Load.md) | CUBS_EM_RAW_CURRENT |
| [`CUBS_Raw_EMail_Address_Load`](job_CUBS_Raw_EMail_Address_Load.md) | DIM_ELECTRONIC_MEDIA |
| [`CUBS_Raw_Empinfo_Load`](job_CUBS_Raw_Empinfo_Load.md) | CUBS_EMPINFO_RAW_CURRENT |
| [`CUBS_Raw_File_Load`](job_CUBS_Raw_File_Load.md) | — |
| [`CUBS_Raw_HH_Client_Load`](job_CUBS_Raw_HH_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_HH_Debtor_Load`](job_CUBS_Raw_HH_Debtor_Load.md) | CUBS_DEBTOR_RAW_HH_CURRENT |
| [`CUBS_Raw_HH_Debtor_Load_No_Delete`](job_CUBS_Raw_HH_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_HH_CURRENT |
| [`CUBS_Raw_HH_Debtor_Load_Upsert`](job_CUBS_Raw_HH_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_HH_CURRENT |
| [`CUBS_Raw_HH_ETL_Load`](job_CUBS_Raw_HH_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Letter_Load`](job_CUBS_Raw_Letter_Load.md) | CUBS_LETTER_RAW_CURRENT |
| [`CUBS_Raw_PRE_Client_Load`](job_CUBS_Raw_PRE_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_PRE_Debtor_Load`](job_CUBS_Raw_PRE_Debtor_Load.md) | CUBS_DEBTOR_RAW_PRE_CURRENT |
| [`CUBS_Raw_PRE_Debtor_Load_No_Delete`](job_CUBS_Raw_PRE_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_PRE_CURRENT |
| [`CUBS_Raw_PRE_Debtor_Load_Upsert`](job_CUBS_Raw_PRE_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_PRE_CURRENT |
| [`CUBS_Raw_PRE_ETL_Load`](job_CUBS_Raw_PRE_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Payplan_Load`](job_CUBS_Raw_Payplan_Load.md) | CUBS_PAYPLAN_RAW_CURRENT |
| [`CUBS_Raw_PostDate_Load`](job_CUBS_Raw_PostDate_Load.md) | CUBS_POSTDATE_RAW_CURRENT |
| [`CUBS_Raw_TOL_Client_Load`](job_CUBS_Raw_TOL_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_TOL_Debtor_Load`](job_CUBS_Raw_TOL_Debtor_Load.md) | CUBS_DEBTOR_RAW_TOL_CURRENT |
| [`CUBS_Raw_TOL_ETL_Load`](job_CUBS_Raw_TOL_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Trans_Load`](job_CUBS_Raw_Trans_Load.md) | CUBS_TRANS_RAW_CURRENT |
| [`CUBS_Raw_Trans_Load_Special`](job_CUBS_Raw_Trans_Load_Special.md) | CUBS_TRANS_RAW_CURRENT |

## `i3_*` telephony / dialer loads (Interactive Intelligence)

Call-detail, agent, and dialer-list loads sourced from the I3 telephony platform, mostly via MSSQL. Several per-site `DialerCallList<SITE>_Load` variants exist, plus `_Backup`/`_Copy` duplicates — see each job's own doc for which one is the live version.

| Job | Target |
|---|---|
| [`CallDetail_40_Load_History`](job_CallDetail_40_Load_History.md) | I3_CALLDETAIL_40 |
| [`Copy_of_i3_DialerCallListTOL_Load_Backup`](job_Copy_of_i3_DialerCallListTOL_Load_Backup.md) | I3_DIALERCALLLIST_CO |
| [`I3_CALLDETAIL_DEDOR_LOAD`](job_I3_CALLDETAIL_DEDOR_LOAD.md) | I3_CALLDETAIL_40 |
| [`i3_AgentActivityLog_Load`](job_i3_AgentActivityLog_Load.md) | I3_AGENTACTIVITYLOG |
| [`i3_AgentQueueStats_Load`](job_i3_AgentQueueStats_Load.md) | I3_AGENTQUEUESTATS |
| [`i3_AgentStats`](job_i3_AgentStats.md) | I3_AGENTSTATS |
| [`i3_CRC_Load`](job_i3_CRC_Load.md) | I3_CRC |
| [`i3_CallDetail_40_Load`](job_i3_CallDetail_40_Load.md) | I3_CALLDETAIL_40 |
| [`i3_CallDetail_40_Load_Copy`](job_i3_CallDetail_40_Load_Copy.md) | I3_CALLDETAIL_40 |
| [`i3_CallDetail_viw_Load`](job_i3_CallDetail_viw_Load.md) | I3_CALLDETAIL_VIW |
| [`i3_CallHistory_Load`](job_i3_CallHistory_Load.md) | I3_CALLHISTORY |
| [`i3_Call_Detail_View_Init_Load`](job_i3_Call_Detail_View_Init_Load.md) | — |
| [`i3_Campaign_Type_Load`](job_i3_Campaign_Type_Load.md) | I3_CAMPAIGN_TYPE |
| [`i3_DialerCallListCHI_Load`](job_i3_DialerCallListCHI_Load.md) | I3_DIALERCALLLIST_CHI |
| [`i3_DialerCallListCO_Load`](job_i3_DialerCallListCO_Load.md) | I3_DIALERCALLLIST_CO |
| [`i3_DialerCallListCO_Load_Backup`](job_i3_DialerCallListCO_Load_Backup.md) | I3_DIALERCALLLIST_CO |
| [`i3_DialerCallListDC_Load`](job_i3_DialerCallListDC_Load.md) | I3_DIALERCALLLIST_DC |
| [`i3_DialerCallListDC_Load_Backup`](job_i3_DialerCallListDC_Load_Backup.md) | I3_DIALERCALLLIST_DC |
| [`i3_DialerCallListHH_Load`](job_i3_DialerCallListHH_Load.md) | I3_DIALERCALLLIST_HH |
| [`i3_DialerCallListHH_Load_Backup`](job_i3_DialerCallListHH_Load_Backup.md) | I3_DIALERCALLLIST_HH |
| [`i3_DialerCallListPRE_Load`](job_i3_DialerCallListPRE_Load.md) | I3_DIALERCALLLIST_PRE |
| [`i3_DialerCallListTOL_Load`](job_i3_DialerCallListTOL_Load.md) | I3_DIALERCALLLIST_TOL |
| [`i3_DialerCallListTOL_Load_Backup`](job_i3_DialerCallListTOL_Load_Backup.md) | I3_DIALERCALLLIST_TOL |
| [`i3_DialerCallList_DEDOR_Load`](job_i3_DialerCallList_DEDOR_Load.md) | I3_DIALERCALLLIST_DEDOR |
| [`i3_Individual_Load`](job_i3_Individual_Load.md) | I3_INDIVIDUAL |
| [`i3_InteractionCustomAttributes_Load`](job_i3_InteractionCustomAttributes_Load.md) | I3_INTERACTIONCUSTOMATTRIBUTES |
| [`i3_InteractionSummaryEx_Load`](job_i3_InteractionSummaryEx_Load.md) | I3_INTERACTIONSUMMARYEX |
| [`i3_InteractionSummary_Load`](job_i3_InteractionSummary_Load.md) | I3_INTERACTIONSUMMARY |
| [`i3_InteractionWrapup_Load`](job_i3_InteractionWrapup_Load.md) | I3_INTERACTIONWRAPUP |

## `ADP_*` payroll/HR loads

File-based loads from ADP payroll and HR exports.

| Job | Target |
|---|---|
| [`ADP_Employee_Load`](job_ADP_Employee_Load.md) | ADP_EMPLOYEE |
| [`ADP_Employee_Raw_Load`](job_ADP_Employee_Raw_Load.md) | TRANSFORM_EMPLOYEE_IMPORT_RAW |
| [`ADP_Payroll_Load`](job_ADP_Payroll_Load.md) | ADP_PAYROLL |
| [`ADP_Roster_Load`](job_ADP_Roster_Load.md) | ADP_ROSTER |

## `HOPE_*` / `HUB_*` loads (MySQL source)

Loads sourced from the HOPE/HUB MySQL system (collections workflow data — goals, notes, transactions, teams/segments/departments).

| Job | Target |
|---|---|
| [`HOPE_Credit_Request`](job_HOPE_Credit_Request.md) | CREDIT_REQUEST |
| [`HOPE_Goals_Load`](job_HOPE_Goals_Load.md) | HOPE_GOALS |
| [`HOPE_Notes_Load`](job_HOPE_Notes_Load.md) | NOTES |
| [`HOPE_SPTransactions_Load`](job_HOPE_SPTransactions_Load.md) | TRANS |
| [`HOPE_Transactions_Load`](job_HOPE_Transactions_Load.md) | HOPE_TRANSACTION |
| [`HUB_Departments_Load`](job_HUB_Departments_Load.md) | DEPARTMENTS |
| [`HUB_HH_Employee_Load`](job_HUB_HH_Employee_Load.md) | HH_EMPLOYEES |
| [`HUB_Segments_Load`](job_HUB_Segments_Load.md) | SEGMENTS |
| [`HUB_Teams_Load`](job_HUB_Teams_Load.md) | TEAMS |
| [`HUB_TempTransaction_Load`](job_HUB_TempTransaction_Load.md) | TRANSACTIONTEMP |
| [`HUB_Transactions_Load`](job_HUB_Transactions_Load.md) | TRANSACTIONS |

## `LW_*` / `ProInsight_*` / `VA_Tax_*` reports and scorecards

Reporting and scorecard jobs — client-facing audit scorecards, focus-attribute extracts, and dashboard feeds. Many are per-client variants of the same underlying pattern (e.g. `LW_*_Audit_Scorecard`, `LW_*_Focus_Attributes`).

| Job | Target |
|---|---|
| [`LW_COC_Water_Scrub`](job_LW_COC_Water_Scrub.md) | writes file |
| [`LW_Carle_Asset_Scrub`](job_LW_Carle_Asset_Scrub.md) | writes file |
| [`LW_Dashboard_Base_Report`](job_LW_Dashboard_Base_Report.md) | writes file |
| [`LW_Dashboard_By_Agent`](job_LW_Dashboard_By_Agent.md) | writes file |
| [`LW_Dashboard_By_Metric`](job_LW_Dashboard_By_Metric.md) | writes file |
| [`LW_Delaware_Focus_Attributes`](job_LW_Delaware_Focus_Attributes.md) | writes file |
| [`LW_Delaware_Focus_Attributes_Granular`](job_LW_Delaware_Focus_Attributes_Granular.md) | writes file |
| [`LW_Delaware_Scorecard_Report`](job_LW_Delaware_Scorecard_Report.md) | writes file |
| [`LW_Deleware_Audit_Scorecard`](job_LW_Deleware_Audit_Scorecard.md) | writes file |
| [`LW_HPS_Audit_Scorecard`](job_LW_HPS_Audit_Scorecard.md) | writes file |
| [`LW_HPS_Focus_Attributes`](job_LW_HPS_Focus_Attributes.md) | writes file |
| [`LW_HPS_Focus_Attributes_Granular`](job_LW_HPS_Focus_Attributes_Granular.md) | writes file |
| [`LW_Insurance_Pmt_Tracking`](job_LW_Insurance_Pmt_Tracking.md) | writes file |
| [`LW_Lurie_Audit_Scorecard`](job_LW_Lurie_Audit_Scorecard.md) | writes file |
| [`LW_Lurie_Focus_Attributes`](job_LW_Lurie_Focus_Attributes.md) | writes file |
| [`LW_Lurie_Focus_Attributes_Granular`](job_LW_Lurie_Focus_Attributes_Granular.md) | writes file |
| [`LW_Manual_Audit_Scorecard`](job_LW_Manual_Audit_Scorecard.md) | writes file |
| [`LW_ProMedica_Scrub`](job_LW_ProMedica_Scrub.md) | writes file |
| [`LW_Property_Scrub`](job_LW_Property_Scrub.md) | writes file |
| [`LW_REPORTS`](job_LW_REPORTS.md) | writes file |
| [`LW_REPORTS_2`](job_LW_REPORTS_2.md) | writes file |
| [`LW_TPL_PMT_REPORT`](job_LW_TPL_PMT_REPORT.md) | writes file |
| [`ProInsight_Analytics_Load`](job_ProInsight_Analytics_Load.md) | PROINSIGHT_ANALYTICS |
| [`ProInsight_CCU_Scorecard_Load`](job_ProInsight_CCU_Scorecard_Load.md) | PROINSIGHT_CCU_SCORECARD |
| [`ProInsight_CCU_Scorecard_V2_Load`](job_ProInsight_CCU_Scorecard_V2_Load.md) | PROINSIGHT_CCU_V2_SCORECARD |
| [`ProInsight_HPS_Scorecard_Load`](job_ProInsight_HPS_Scorecard_Load.md) | PROINSIGHT_HPS_SCORECARD |
| [`ProInsight_Scorecard_Load`](job_ProInsight_Scorecard_Load.md) | PROINSIGHT_SCORECARD |
| [`VAT_1394_Load`](job_VAT_1394_Load.md) | VAT_1394 |
| [`VA_Tax_Inventory_Report`](job_VA_Tax_Inventory_Report.md) | writes file |
| [`VA_Tax_Report_Load`](job_VA_Tax_Report_Load.md) | VA_TAX_RECON_REPORT |
| [`VA_Tax_Report_Split`](job_VA_Tax_Report_Split.md) | writes file |

## `SMS_*` inbound/outbound loads

SMS messaging platform inbound/outbound loads, including a backfill variant.

| Job | Target |
|---|---|
| [`SMS_IC_Inbound_Load`](job_SMS_IC_Inbound_Load.md) | TEXTS_IC_INBOUND |
| [`SMS_IC_Outbound_Load`](job_SMS_IC_Outbound_Load.md) | TEXTS_IC_OUTBOUND |
| [`SMS_IC_Outbound_Load_Backfill`](job_SMS_IC_Outbound_Load_Backfill.md) | TEXTS_IC_OUTBOUND |
| [`SMS_Inbound_Load`](job_SMS_Inbound_Load.md) | TEXTS_SBT_INBOUND |
| [`SMS_Outbound_Load`](job_SMS_Outbound_Load.md) | TEXTS_SBT_OUTBOUND |

## `Test_*` / `TEST_*` jobs

Explicitly named test/scratch jobs (not part of the production job graph, as far as can be determined from metadata alone — see each job's own doc).

| Job | Target |
|---|---|
| [`TEST_Avita_Monthly_Report_Extract`](job_TEST_Avita_Monthly_Report_Extract.md) | writes file |
| [`TEST_Date_Params`](job_TEST_Date_Params.md) | — |
| [`TEST_Email_Alerts`](job_TEST_Email_Alerts.md) | — |
| [`Test_Decryption`](job_Test_Decryption.md) | writes file |
| [`Test_Encryption`](job_Test_Encryption.md) | writes file |

## Encryption / decryption utility jobs

Standalone jobs that encrypt or decrypt values (SSNs, tax codes, etc.) rather than loading business data end to end.

| Job | Target |
|---|---|
| [`EncryptValue_ContextVariable`](job_EncryptValue_ContextVariable.md) | — |
| [`Encrypt_CHI_Fiscal_Tax_Code`](job_Encrypt_CHI_Fiscal_Tax_Code.md) | TMP_CHI_TAXCODE |
| [`Encrypt_CO_Fiscal_A_F18_A`](job_Encrypt_CO_Fiscal_A_F18_A.md) | DIMFISCAL_CO_A_UPDATE |
| [`Initial_Ins_Discovery_V2_Decrypted`](job_Initial_Ins_Discovery_V2_Decrypted.md) | writes file |

## `Extract_*` / `*_Extract` jobs (Snowflake/source → file, or reporting extracts)

Read-out jobs producing files or downstream extracts rather than loading into Snowflake staging tables — decile/score extracts, client-specific legal/asset-scrub extracts, and ad hoc reporting pulls.

| Job | Target |
|---|---|
| [`Avita_Monthly_Report_Extract`](job_Avita_Monthly_Report_Extract.md) | writes file |
| [`Call_Campaign_Results_Extract`](job_Call_Campaign_Results_Extract.md) | writes file |
| [`Callminer_HH_Metadata_Daily_Extract`](job_Callminer_HH_Metadata_Daily_Extract.md) | writes file |
| [`City_of_Phi_C1A_PDR_Extract`](job_City_of_Phi_C1A_PDR_Extract.md) | writes file |
| [`DC_SSN_Extract`](job_DC_SSN_Extract.md) | writes file |
| [`Equibli_Extract`](job_Equibli_Extract.md) | writes file |
| [`Extract_CHI_Hermes_Decile`](job_Extract_CHI_Hermes_Decile.md) | writes file |
| [`Extract_CO_Hermes_Decile`](job_Extract_CO_Hermes_Decile.md) | writes file |
| [`Extract_DC_Hermes_Decile`](job_Extract_DC_Hermes_Decile.md) | writes file |
| [`Extract_DDNPII`](job_Extract_DDNPII.md) | — |
| [`Extract_Equabli_GOV`](job_Extract_Equabli_GOV.md) | writes file |
| [`Extract_Equabli_HC_Validation_Score`](job_Extract_Equabli_HC_Validation_Score.md) | writes file |
| [`Extract_Equabli_Reports`](job_Extract_Equabli_Reports.md) | writes file |
| [`Extract_Equibli_Test`](job_Extract_Equibli_Test.md) | writes file |
| [`Extract_HH_Hermes_Decile`](job_Extract_HH_Hermes_Decile.md) | writes file |
| [`Extract_HH_Hermes_ValDecile`](job_Extract_HH_Hermes_ValDecile.md) | writes file |
| [`Extract_Letter_Count`](job_Extract_Letter_Count.md) | — |
| [`Extract_Letter_Count_to_Hyper`](job_Extract_Letter_Count_to_Hyper.md) | — |
| [`Extract_MSSQL_COCHI_Debtor`](job_Extract_MSSQL_COCHI_Debtor.md) | CHI_DEBTOR |
| [`Extract_No_Dialer_Test_CHI`](job_Extract_No_Dialer_Test_CHI.md) | writes file |
| [`Extract_No_Dialer_Test_CO`](job_Extract_No_Dialer_Test_CO.md) | writes file |
| [`Extract_No_Dialer_Test_DC`](job_Extract_No_Dialer_Test_DC.md) | writes file |
| [`Extract_No_Dialer_Test_HH`](job_Extract_No_Dialer_Test_HH.md) | writes file |
| [`Extract_No_Dialer_Test_TOL`](job_Extract_No_Dialer_Test_TOL.md) | writes file |
| [`Extract_PRE_Hermes_Decile`](job_Extract_PRE_Hermes_Decile.md) | writes file |
| [`Extract_ProInsights_Data`](job_Extract_ProInsights_Data.md) | writes file |
| [`Extract_TOL_Hermes_Decile`](job_Extract_TOL_Hermes_Decile.md) | writes file |
| [`HealthPartners_Close_Reports_Extract`](job_HealthPartners_Close_Reports_Extract.md) | writes file |
| [`IDOR_Amnesty_Extract`](job_IDOR_Amnesty_Extract.md) | writes file |
| [`Insurance_Discovery_Scrub_Extract`](job_Insurance_Discovery_Scrub_Extract.md) | writes file |
| [`Insurance_Report_Extract`](job_Insurance_Report_Extract.md) | writes file |
| [`Last4SSN_Extract`](job_Last4SSN_Extract.md) | LAST4SSN |
| [`LegalMatch_Extract`](job_LegalMatch_Extract.md) | writes file |
| [`Legal_Asset_Scrub_Champaign_County_Extract`](job_Legal_Asset_Scrub_Champaign_County_Extract.md) | writes file |
| [`Legal_Asset_Scrub_Illinois_Counties_Extract`](job_Legal_Asset_Scrub_Illinois_Counties_Extract.md) | writes file |
| [`Legal_Asset_Scrub_Illinois_Counties_Extract_2`](job_Legal_Asset_Scrub_Illinois_Counties_Extract_2.md) | writes file |
| [`Legal_Asset_Scrub_KDOR_Extract`](job_Legal_Asset_Scrub_KDOR_Extract.md) | writes file |
| [`Top_N_Accounts_All_Extract`](job_Top_N_Accounts_All_Extract.md) | writes file |
| [`Top_N_Accounts_Extract`](job_Top_N_Accounts_Extract.md) | writes file |

## `Dim*_Load` / `Fact*_Load` dimensional-model loads

Loads that populate the star-schema dimension and fact tables consumed by downstream reporting.

| Job | Target |
|---|---|
| [`DimClient_Load`](job_DimClient_Load.md) | DIMCLIENT, DIMDEPARTMENT, DIMGLCODE, STG_DIM_CLIENT |
| [`DimDate_Load`](job_DimDate_Load.md) | DIMDATE |
| [`DimDebtor_Load`](job_DimDebtor_Load.md) | DIMDEBTOR, STG_DIM_DEBTOR |
| [`DimDebtor_NewFields_Load`](job_DimDebtor_NewFields_Load.md) | DIMDEBTOR_NEWFIELDS |
| [`DimDepartment_and_GL_Load`](job_DimDepartment_and_GL_Load.md) | DIMDEPARTMENT, DIMGLCODE |
| [`DimFiscal_CHI_Load`](job_DimFiscal_CHI_Load.md) | — |
| [`DimFiscal_CO_Load`](job_DimFiscal_CO_Load.md) | — |
| [`DimFiscal_DC_Load`](job_DimFiscal_DC_Load.md) | — |
| [`DimFiscal_HH_B_TrueUp`](job_DimFiscal_HH_B_TrueUp.md) | DIMFISCAL_HH_B_TRUEUP |
| [`DimFiscal_HH_Load`](job_DimFiscal_HH_Load.md) | — |
| [`DimFiscal_PRE_Load`](job_DimFiscal_PRE_Load.md) | — |
| [`DimFiscal_TOL_Load`](job_DimFiscal_TOL_Load.md) | — |
| [`DimScore_Load`](job_DimScore_Load.md) | FISCAL_HH_E, FISCAL_HH_C, SUNGARD_SCORE |
| [`DimStatus_Load`](job_DimStatus_Load.md) | DIMSTATUSCODE |
| [`FactLetter_Load`](job_FactLetter_Load.md) | FACTLETTERS |
| [`FactPaymentManager_Load`](job_FactPaymentManager_Load.md) | FACTPAYMENTMANAGER |
| [`FactPostDates_Load`](job_FactPostDates_Load.md) | FACTPOSTDATES |
| [`FactTrans_Load`](job_FactTrans_Load.md) | FACTTRANS |
| [`FactTrans_TCODE_COLLECTOR_Load`](job_FactTrans_TCODE_COLLECTOR_Load.md) | TRANS_TCODE_COLLECTOR |

## Other loads, utilities, and one-off jobs

Everything else — single-purpose loads, backfills, one-time fixes, and utility jobs that don't fit a larger family.

| Job | Target |
|---|---|
| [`Activity_Load_Daily`](job_Activity_Load_Daily.md) | ACTIVITY |
| [`Activity_Load_Legacy`](job_Activity_Load_Legacy.md) | ACTIVITY_BACKFILL |
| [`AgentKPI_Daily_Load`](job_AgentKPI_Daily_Load.md) | AGENTKPI_DAILYV3 |
| [`Backfill_Debtor_Cell_Phone_f83`](job_Backfill_Debtor_Cell_Phone_f83.md) | DEBTOR_CELL_PHONE_F83 |
| [`Backfill_Debtor_Phones`](job_Backfill_Debtor_Phones.md) | DEBTOR_PHONE_SP |
| [`Bad_Phone_Load`](job_Bad_Phone_Load.md) | BADPHN_DONOTCALL_STAGING |
| [`CFDAILY_Load`](job_CFDAILY_Load.md) | CFDAILY |
| [`CHI_E_Media_Load`](job_CHI_E_Media_Load.md) | CHI_ELECTRONICSMEDIA |
| [`CLT_XFR_DT_Load`](job_CLT_XFR_DT_Load.md) | CLT_XFR_DT_CATCHUP |
| [`CO_DEBTOR_SPECIAL_BACKFILL_LOAD`](job_CO_DEBTOR_SPECIAL_BACKFILL_LOAD.md) | CO_DEBTOR_SPECIAL |
| [`CO_Debtor_TrueUp`](job_CO_Debtor_TrueUp.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CO_E_Media_Load`](job_CO_E_Media_Load.md) | CO_ELECTRONICSMEDIA |
| [`CRPLoad`](job_CRPLoad.md) | CRPDATA |
| [`CUBS_EMail_Address_Load`](job_CUBS_EMail_Address_Load.md) | DIM_ELECTRONIC_MEDIA |
| [`Carle_Asset_Scrub`](job_Carle_Asset_Scrub.md) | writes file |
| [`Client_NonCUBS_Attributes`](job_Client_NonCUBS_Attributes.md) | CLIENT_ATTRIBUTES |
| [`Collector_Payment_Detail_Load`](job_Collector_Payment_Detail_Load.md) | COLLECTOR_PAYMENT_DETAIL |
| [`Columbia_Doctors_Legal_Rpt`](job_Columbia_Doctors_Legal_Rpt.md) | writes file |
| [`DC_Call_Contact_Exceptions_1`](job_DC_Call_Contact_Exceptions_1.md) | writes file |
| [`DC_Call_Contact_Exceptions_2`](job_DC_Call_Contact_Exceptions_2.md) | — |
| [`DC_E_Media_Load`](job_DC_E_Media_Load.md) | DC_ELECTRONICSMEDIA |
| [`DEBTOR_UPDATES_20230807`](job_DEBTOR_UPDATES_20230807.md) | DEBTOR_UPDATE_20230807 |
| [`DIMDEBTOR_FISCALS_20230713`](job_DIMDEBTOR_FISCALS_20230713.md) | DIMDEBTOR_FISCALS |
| [`DNIS_Load`](job_DNIS_Load.md) | I3_DNIS |
| [`DNIS_Org_Load`](job_DNIS_Org_Load.md) | I3_DNIS_ORG |
| [`Daily_Fee_Projection_Load`](job_Daily_Fee_Projection_Load.md) | TRANSFORM_DAILY_FEE_MANUALS |
| [`Debtor_Deleted_Load`](job_Debtor_Deleted_Load.md) | DEBTOR_DELETED |
| [`Debtor_Derived_Load`](job_Debtor_Derived_Load.md) | — |
| [`Debtor_Status_Load`](job_Debtor_Status_Load.md) | DEBTOR_STATUS_UPDATE |
| [`Debtor_Status_Load_MSSQL`](job_Debtor_Status_Load_MSSQL.md) | — |
| [`Debtor_Strat_Backfill`](job_Debtor_Strat_Backfill.md) | TMP_DIMDEBTOR_BACKFILL |
| [`Dialer_Grp_Transform_Inputs_Load`](job_Dialer_Grp_Transform_Inputs_Load.md) | DIALERGRP_TRANSFORM_AGG_OVERRIDE, DIALERGRP_TRANSFORM_LOOKUP_DISTRIBUTION |
| [`DoNotCall_Load`](job_DoNotCall_Load.md) | DNC_DONOTCALL_STAGING |
| [`DoNotCall_Load_Full`](job_DoNotCall_Load_Full.md) | DNC_DONOTCALL_STAGING |
| [`ERC_Event_Report_Load`](job_ERC_Event_Report_Load.md) | ERC_EVENT_REPORT |
| [`ETR_Load`](job_ETR_Load.md) | ETR |
| [`EmployeeHrsWorked_Load`](job_EmployeeHrsWorked_Load.md) | EMPLOYEEHRSWORKED |
| [`EmployeeRates_Load`](job_EmployeeRates_Load.md) | EMPLOYEERATES |
| [`Employee_Collector_Load`](job_Employee_Collector_Load.md) | EMPLOYEE_COLLECTOR |
| [`Fran_Bai_Backlog`](job_Fran_Bai_Backlog.md) | writes file |
| [`HH_DEBTOR_SPECIAL_20231016_LOAD`](job_HH_DEBTOR_SPECIAL_20231016_LOAD.md) | HH_DEBTOR_LAST_BILL_DT |
| [`HH_EMedia_Load`](job_HH_EMedia_Load.md) | HH_EMESSAGE |
| [`HH_E_Media_Load`](job_HH_E_Media_Load.md) | HH_ELECTRONICSMEDIA |
| [`HH_TRANS_NORTHSHORE_LOAD`](job_HH_TRANS_NORTHSHORE_LOAD.md) | HH_TRANS_NORTHSHORE |
| [`HH_VAL_LTR_DATE_Backfill`](job_HH_VAL_LTR_DATE_Backfill.md) | TMP_HH_VAL_LTR_DATE |
| [`INPUT_DIALER_LIST_GOV_Load`](job_INPUT_DIALER_LIST_GOV_Load.md) | INPUT_DIALER_LIST_UNIONED_GOV |
| [`INPUT_DIALER_LIST_HC_Load`](job_INPUT_DIALER_LIST_HC_Load.md) | INPUT_DIALER_LIST_UNIONED_HC |
| [`ISO_Request_Export`](job_ISO_Request_Export.md) | writes file |
| [`Initial_Insurance_Discovery_File`](job_Initial_Insurance_Discovery_File.md) | writes file |
| [`Ins_Cvg_Debtor_NPI_Load`](job_Ins_Cvg_Debtor_NPI_Load.md) | INS_CVG_DEBTOR_NPI |
| [`Insurance_Discovery_Load`](job_Insurance_Discovery_Load.md) | INSURANCE_DISCOVERY |
| [`Insurance_Discovery_Test`](job_Insurance_Discovery_Test.md) | writes file |
| [`Livevox_Daily_Load`](job_Livevox_Daily_Load.md) | LIVEVOX_CALLS |
| [`Livevox_Sample_Load`](job_Livevox_Sample_Load.md) | LIVEVOX_CALLS |
| [`LoadLegalRpt20231130`](job_LoadLegalRpt20231130.md) | writes file |
| [`Load_837_Files`](job_Load_837_Files.md) | — |
| [`Load_Attunely_Data`](job_Load_Attunely_Data.md) | ATTUNELY_PERFORM_DATA |
| [`Load_Debtor_New_Columns`](job_Load_Debtor_New_Columns.md) | SPRING_FOUR |
| [`Load_Employee_Collector_History`](job_Load_Employee_Collector_History.md) | EMPLOYEE_COLLECTOR_HISTORY |
| [`Load_Evergreen_Hours`](job_Load_Evergreen_Hours.md) | EVERGREEN_AGENT_HOURS |
| [`Load_HH_Debtor_Special_20251222`](job_Load_HH_Debtor_Special_20251222.md) | HH_DEBTOR_SPECIAL_20251222 |
| [`Load_Misc_Dims`](job_Load_Misc_Dims.md) | DIMLOGON, DIMDESKINFO, DIMEMPLOYEEINFO |
| [`Load_PCI_Letter_Disp_Desc`](job_Load_PCI_Letter_Disp_Desc.md) | PCI_Letter_Disp |
| [`MBoich_Experian_Extracts`](job_MBoich_Experian_Extracts.md) | writes file |
| [`Mail_Merge_Load`](job_Mail_Merge_Load.md) | MAIL_MERGE |
| [`MaxRTE_Request_Export`](job_MaxRTE_Request_Export.md) | writes file |
| [`MaxRTE_Result_Load`](job_MaxRTE_Result_Load.md) | MAXRTE_RESPONSE_LOG |
| [`Migrating_Clients_20260424`](job_Migrating_Clients_20260424.md) | UTILITY_CLIENT_EXCLUDE_LIST |
| [`Northwestern_Future_Appts`](job_Northwestern_Future_Appts.md) | NORTHWESTERN_UPCOMING_APPTS |
| [`Notes_Load`](job_Notes_Load.md) | NOTES |
| [`PA_Turnpike_Load`](job_PA_Turnpike_Load.md) | PA_TURNPIKE |
| [`PCI_LETTERS_TO_DELETE`](job_PCI_LETTERS_TO_DELETE.md) | PCI_LETTERS_TO_DELETE |
| [`PCI_Letter_Load`](job_PCI_Letter_Load.md) | PCI_LETTERS |
| [`PDC_Plan_Txn_Backfill`](job_PDC_Plan_Txn_Backfill.md) | TMP_TRANS_BACKFILE |
| [`PRE_E_Media_Load`](job_PRE_E_Media_Load.md) | PRE_ELECTRONICSMEDIA |
| [`PV_PostDate_Export_Load`](job_PV_PostDate_Export_Load.md) | PV_POSTDATE |
| [`PaymentPlan_Legacy_Load`](job_PaymentPlan_Legacy_Load.md) | PAYMENTPLAN |
| [`PaymentVision_Activity_Load`](job_PaymentVision_Activity_Load.md) | PAYMENTVISION_ACTIVITY |
| [`Raw_PCI_Letter_Load`](job_Raw_PCI_Letter_Load.md) | PCI_LETTERS, DEBTOR_ADDRESSES |
| [`Semaphore_Check`](job_Semaphore_Check.md) | — |
| [`SendGrid_Report_Load`](job_SendGrid_Report_Load.md) | FACT_EMAILS_SENDGRID |
| [`Skip_Costs_Load`](job_Skip_Costs_Load.md) | SKIP_COSTS |
| [`Touchstar_DNC_Load`](job_Touchstar_DNC_Load.md) | TOUCHSTAR_DONOTCALL_STAGING |
| [`Trans_History_Load`](job_Trans_History_Load.md) | TEMP_TRANS |
| [`Voapp_File_Load`](job_Voapp_File_Load.md) | VOAPPS |
| [`master_prediction_proposal_cubs_extract`](job_master_prediction_proposal_cubs_extract.md) | writes file |

## Full alphabetical list (all 289 jobs)

| Job | Target |
|---|---|
| [`ADP_Employee_Load`](job_ADP_Employee_Load.md) | ADP_EMPLOYEE |
| [`ADP_Employee_Raw_Load`](job_ADP_Employee_Raw_Load.md) | TRANSFORM_EMPLOYEE_IMPORT_RAW |
| [`ADP_Payroll_Load`](job_ADP_Payroll_Load.md) | ADP_PAYROLL |
| [`ADP_Roster_Load`](job_ADP_Roster_Load.md) | ADP_ROSTER |
| [`Activity_Load_Daily`](job_Activity_Load_Daily.md) | ACTIVITY |
| [`Activity_Load_Legacy`](job_Activity_Load_Legacy.md) | ACTIVITY_BACKFILL |
| [`AgentKPI_Daily_Load`](job_AgentKPI_Daily_Load.md) | AGENTKPI_DAILYV3 |
| [`Avita_Monthly_Report_Extract`](job_Avita_Monthly_Report_Extract.md) | writes file |
| [`Backfill_Debtor_Cell_Phone_f83`](job_Backfill_Debtor_Cell_Phone_f83.md) | DEBTOR_CELL_PHONE_F83 |
| [`Backfill_Debtor_Phones`](job_Backfill_Debtor_Phones.md) | DEBTOR_PHONE_SP |
| [`Bad_Phone_Load`](job_Bad_Phone_Load.md) | BADPHN_DONOTCALL_STAGING |
| [`CFDAILY_Load`](job_CFDAILY_Load.md) | CFDAILY |
| [`CHI_E_Media_Load`](job_CHI_E_Media_Load.md) | CHI_ELECTRONICSMEDIA |
| [`CLT_XFR_DT_Load`](job_CLT_XFR_DT_Load.md) | CLT_XFR_DT_CATCHUP |
| [`CO_DEBTOR_SPECIAL_BACKFILL_LOAD`](job_CO_DEBTOR_SPECIAL_BACKFILL_LOAD.md) | CO_DEBTOR_SPECIAL |
| [`CO_Debtor_TrueUp`](job_CO_Debtor_TrueUp.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CO_E_Media_Load`](job_CO_E_Media_Load.md) | CO_ELECTRONICSMEDIA |
| [`CO_Master_Load`](job_CO_Master_Load.md) | orchestrator (see job list below) |
| [`CREATE_RAW_CUBS_CLIENT`](job_CREATE_RAW_CUBS_CLIENT.md) | — |
| [`CRPLoad`](job_CRPLoad.md) | CRPDATA |
| [`CUBS_EMail_Address_Load`](job_CUBS_EMail_Address_Load.md) | DIM_ELECTRONIC_MEDIA |
| [`CUBS_PostDates_Load`](job_CUBS_PostDates_Load.md) | orchestrator (see job list below) |
| [`CUBS_Raw_Activity_Load`](job_CUBS_Raw_Activity_Load.md) | CUBS_ACTIVITY_RAW_CURRENT |
| [`CUBS_Raw_CHI_Client_Load`](job_CUBS_Raw_CHI_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_CHI_Debtor_Load`](job_CUBS_Raw_CHI_Debtor_Load.md) | CUBS_DEBTOR_RAW_CHI_CURRENT |
| [`CUBS_Raw_CHI_Debtor_Load_No_Delete`](job_CUBS_Raw_CHI_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_CHI_CURRENT |
| [`CUBS_Raw_CHI_Debtor_Load_Upsert`](job_CUBS_Raw_CHI_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_CHI_CURRENT |
| [`CUBS_Raw_CHI_ETL_Load`](job_CUBS_Raw_CHI_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_CO_Client_Load`](job_CUBS_Raw_CO_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_CO_Debtor_Load`](job_CUBS_Raw_CO_Debtor_Load.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CUBS_Raw_CO_Debtor_Load_No_Delete`](job_CUBS_Raw_CO_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CUBS_Raw_CO_Debtor_Load_Upsert`](job_CUBS_Raw_CO_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_CO_CURRENT |
| [`CUBS_Raw_CO_ETL_Load`](job_CUBS_Raw_CO_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Cellphone_Load`](job_CUBS_Raw_Cellphone_Load.md) | CUBS_CELLPHONE_RAW |
| [`CUBS_Raw_Client_Load`](job_CUBS_Raw_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_DC_Client_Load`](job_CUBS_Raw_DC_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_DC_Debtor_Load`](job_CUBS_Raw_DC_Debtor_Load.md) | CUBS_DEBTOR_RAW_DC_CURRENT |
| [`CUBS_Raw_DC_Debtor_Load_No_Delete`](job_CUBS_Raw_DC_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_DC_CURRENT |
| [`CUBS_Raw_DC_Debtor_Load_Upsert`](job_CUBS_Raw_DC_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_DC_CURRENT |
| [`CUBS_Raw_DC_ETL_Load`](job_CUBS_Raw_DC_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Debtor_Load`](job_CUBS_Raw_Debtor_Load.md) | orchestrator (see job list below) |
| [`CUBS_Raw_Debtor_Load_Test`](job_CUBS_Raw_Debtor_Load_Test.md) | orchestrator (see job list below) |
| [`CUBS_Raw_DeskInfo_Load`](job_CUBS_Raw_DeskInfo_Load.md) | CUBS_DESKINFO_RAW |
| [`CUBS_Raw_EM_Load`](job_CUBS_Raw_EM_Load.md) | CUBS_EM_RAW_CURRENT |
| [`CUBS_Raw_EMail_Address_Load`](job_CUBS_Raw_EMail_Address_Load.md) | DIM_ELECTRONIC_MEDIA |
| [`CUBS_Raw_ETL_Load`](job_CUBS_Raw_ETL_Load.md) | orchestrator (see job list below) |
| [`CUBS_Raw_Empinfo_Load`](job_CUBS_Raw_Empinfo_Load.md) | CUBS_EMPINFO_RAW_CURRENT |
| [`CUBS_Raw_File_Load`](job_CUBS_Raw_File_Load.md) | — |
| [`CUBS_Raw_HH_Client_Load`](job_CUBS_Raw_HH_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_HH_Debtor_Load`](job_CUBS_Raw_HH_Debtor_Load.md) | CUBS_DEBTOR_RAW_HH_CURRENT |
| [`CUBS_Raw_HH_Debtor_Load_No_Delete`](job_CUBS_Raw_HH_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_HH_CURRENT |
| [`CUBS_Raw_HH_Debtor_Load_Upsert`](job_CUBS_Raw_HH_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_HH_CURRENT |
| [`CUBS_Raw_HH_ETL_Load`](job_CUBS_Raw_HH_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Letter_Load`](job_CUBS_Raw_Letter_Load.md) | CUBS_LETTER_RAW_CURRENT |
| [`CUBS_Raw_PRE_Client_Load`](job_CUBS_Raw_PRE_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_PRE_Debtor_Load`](job_CUBS_Raw_PRE_Debtor_Load.md) | CUBS_DEBTOR_RAW_PRE_CURRENT |
| [`CUBS_Raw_PRE_Debtor_Load_No_Delete`](job_CUBS_Raw_PRE_Debtor_Load_No_Delete.md) | CUBS_DEBTOR_RAW_PRE_CURRENT |
| [`CUBS_Raw_PRE_Debtor_Load_Upsert`](job_CUBS_Raw_PRE_Debtor_Load_Upsert.md) | CUBS_DEBTOR_RAW_PRE_CURRENT |
| [`CUBS_Raw_PRE_ETL_Load`](job_CUBS_Raw_PRE_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Payplan_Load`](job_CUBS_Raw_Payplan_Load.md) | CUBS_PAYPLAN_RAW_CURRENT |
| [`CUBS_Raw_PostDate_Load`](job_CUBS_Raw_PostDate_Load.md) | CUBS_POSTDATE_RAW_CURRENT |
| [`CUBS_Raw_TOL_Client_Load`](job_CUBS_Raw_TOL_Client_Load.md) | CUBS_CLIENT_RAW_CURRENT |
| [`CUBS_Raw_TOL_Debtor_Load`](job_CUBS_Raw_TOL_Debtor_Load.md) | CUBS_DEBTOR_RAW_TOL_CURRENT |
| [`CUBS_Raw_TOL_ETL_Load`](job_CUBS_Raw_TOL_ETL_Load.md) | CUBS_ETL_RAW_CURRENT |
| [`CUBS_Raw_Trans_Load`](job_CUBS_Raw_Trans_Load.md) | CUBS_TRANS_RAW_CURRENT |
| [`CUBS_Raw_Trans_Load_Special`](job_CUBS_Raw_Trans_Load_Special.md) | CUBS_TRANS_RAW_CURRENT |
| [`CallDetail_40_Load_History`](job_CallDetail_40_Load_History.md) | I3_CALLDETAIL_40 |
| [`Call_Campaign_Results_Extract`](job_Call_Campaign_Results_Extract.md) | writes file |
| [`Callminer_HH_Metadata_Daily_Extract`](job_Callminer_HH_Metadata_Daily_Extract.md) | writes file |
| [`Carle_Asset_Scrub`](job_Carle_Asset_Scrub.md) | writes file |
| [`City_of_Phi_C1A_PDR_Extract`](job_City_of_Phi_C1A_PDR_Extract.md) | writes file |
| [`Client_NonCUBS_Attributes`](job_Client_NonCUBS_Attributes.md) | CLIENT_ATTRIBUTES |
| [`Collector_Payment_Detail_Load`](job_Collector_Payment_Detail_Load.md) | COLLECTOR_PAYMENT_DETAIL |
| [`Columbia_Doctors_Legal_Rpt`](job_Columbia_Doctors_Legal_Rpt.md) | writes file |
| [`Copy_of_i3_DialerCallListTOL_Load_Backup`](job_Copy_of_i3_DialerCallListTOL_Load_Backup.md) | I3_DIALERCALLLIST_CO |
| [`DC_Call_Contact_Exceptions_1`](job_DC_Call_Contact_Exceptions_1.md) | writes file |
| [`DC_Call_Contact_Exceptions_2`](job_DC_Call_Contact_Exceptions_2.md) | — |
| [`DC_E_Media_Load`](job_DC_E_Media_Load.md) | DC_ELECTRONICSMEDIA |
| [`DC_SSN_Extract`](job_DC_SSN_Extract.md) | writes file |
| [`DEBTOR_UPDATES_20230807`](job_DEBTOR_UPDATES_20230807.md) | DEBTOR_UPDATE_20230807 |
| [`DIMDEBTOR_FISCALS_20230713`](job_DIMDEBTOR_FISCALS_20230713.md) | DIMDEBTOR_FISCALS |
| [`DNIS_Load`](job_DNIS_Load.md) | I3_DNIS |
| [`DNIS_Org_Load`](job_DNIS_Org_Load.md) | I3_DNIS_ORG |
| [`Daily_Fee_Projection_Load`](job_Daily_Fee_Projection_Load.md) | TRANSFORM_DAILY_FEE_MANUALS |
| [`Debtor_Deleted_Load`](job_Debtor_Deleted_Load.md) | DEBTOR_DELETED |
| [`Debtor_Derived_Load`](job_Debtor_Derived_Load.md) | — |
| [`Debtor_Status_Load`](job_Debtor_Status_Load.md) | DEBTOR_STATUS_UPDATE |
| [`Debtor_Status_Load_MSSQL`](job_Debtor_Status_Load_MSSQL.md) | — |
| [`Debtor_Strat_Backfill`](job_Debtor_Strat_Backfill.md) | TMP_DIMDEBTOR_BACKFILL |
| [`Dialer_Grp_Transform_Inputs_Load`](job_Dialer_Grp_Transform_Inputs_Load.md) | DIALERGRP_TRANSFORM_AGG_OVERRIDE, DIALERGRP_TRANSFORM_LOOKUP_DISTRIBUTION |
| [`DimCellphone_Load`](job_DimCellphone_Load.md) | orchestrator (see job list below) |
| [`DimClient_Load`](job_DimClient_Load.md) | DIMCLIENT, DIMDEPARTMENT, DIMGLCODE, STG_DIM_CLIENT |
| [`DimDate_Load`](job_DimDate_Load.md) | DIMDATE |
| [`DimDebtor_Load`](job_DimDebtor_Load.md) | DIMDEBTOR, STG_DIM_DEBTOR |
| [`DimDebtor_NewFields_Load`](job_DimDebtor_NewFields_Load.md) | DIMDEBTOR_NEWFIELDS |
| [`DimDepartment_and_GL_Load`](job_DimDepartment_and_GL_Load.md) | DIMDEPARTMENT, DIMGLCODE |
| [`DimDeskInfo_Load`](job_DimDeskInfo_Load.md) | orchestrator (see job list below) |
| [`DimEmployeeInfo_Load`](job_DimEmployeeInfo_Load.md) | orchestrator (see job list below) |
| [`DimFiscal_CHI_Load`](job_DimFiscal_CHI_Load.md) | — |
| [`DimFiscal_CO_Load`](job_DimFiscal_CO_Load.md) | — |
| [`DimFiscal_DC_Load`](job_DimFiscal_DC_Load.md) | — |
| [`DimFiscal_HH_B_TrueUp`](job_DimFiscal_HH_B_TrueUp.md) | DIMFISCAL_HH_B_TRUEUP |
| [`DimFiscal_HH_Load`](job_DimFiscal_HH_Load.md) | — |
| [`DimFiscal_PRE_Load`](job_DimFiscal_PRE_Load.md) | — |
| [`DimFiscal_TOL_Load`](job_DimFiscal_TOL_Load.md) | — |
| [`DimScore_Load`](job_DimScore_Load.md) | FISCAL_HH_E, FISCAL_HH_C, SUNGARD_SCORE |
| [`DimStatus_Load`](job_DimStatus_Load.md) | DIMSTATUSCODE |
| [`DoNotCall_Load`](job_DoNotCall_Load.md) | DNC_DONOTCALL_STAGING |
| [`DoNotCall_Load_Full`](job_DoNotCall_Load_Full.md) | DNC_DONOTCALL_STAGING |
| [`EMail_Address_Load`](job_EMail_Address_Load.md) | orchestrator (see job list below) |
| [`ERC_Event_Report_Load`](job_ERC_Event_Report_Load.md) | ERC_EVENT_REPORT |
| [`ETR_Load`](job_ETR_Load.md) | ETR |
| [`EmployeeHrsWorked_Load`](job_EmployeeHrsWorked_Load.md) | EMPLOYEEHRSWORKED |
| [`EmployeeRates_Load`](job_EmployeeRates_Load.md) | EMPLOYEERATES |
| [`Employee_Collector_Load`](job_Employee_Collector_Load.md) | EMPLOYEE_COLLECTOR |
| [`EncryptValue_ContextVariable`](job_EncryptValue_ContextVariable.md) | — |
| [`Encrypt_CHI_Fiscal_Tax_Code`](job_Encrypt_CHI_Fiscal_Tax_Code.md) | TMP_CHI_TAXCODE |
| [`Encrypt_CO_Fiscal_A_F18_A`](job_Encrypt_CO_Fiscal_A_F18_A.md) | DIMFISCAL_CO_A_UPDATE |
| [`Equibli_Extract`](job_Equibli_Extract.md) | writes file |
| [`Export_Hermes_APC_Master_Prediction`](job_Export_Hermes_APC_Master_Prediction.md) | orchestrator (see job list below) |
| [`Extract_CHI_Hermes_Decile`](job_Extract_CHI_Hermes_Decile.md) | writes file |
| [`Extract_CO_Hermes_Decile`](job_Extract_CO_Hermes_Decile.md) | writes file |
| [`Extract_DC_Hermes_Decile`](job_Extract_DC_Hermes_Decile.md) | writes file |
| [`Extract_DDNPII`](job_Extract_DDNPII.md) | — |
| [`Extract_Equabli_GOV`](job_Extract_Equabli_GOV.md) | writes file |
| [`Extract_Equabli_HC_Validation_Score`](job_Extract_Equabli_HC_Validation_Score.md) | writes file |
| [`Extract_Equabli_Reports`](job_Extract_Equabli_Reports.md) | writes file |
| [`Extract_Equibli_Test`](job_Extract_Equibli_Test.md) | writes file |
| [`Extract_HH_Hermes_Decile`](job_Extract_HH_Hermes_Decile.md) | writes file |
| [`Extract_HH_Hermes_ValDecile`](job_Extract_HH_Hermes_ValDecile.md) | writes file |
| [`Extract_Hermes_Master_Prediction`](job_Extract_Hermes_Master_Prediction.md) | orchestrator (see job list below) |
| [`Extract_Letter_Count`](job_Extract_Letter_Count.md) | — |
| [`Extract_Letter_Count_to_Hyper`](job_Extract_Letter_Count_to_Hyper.md) | — |
| [`Extract_MSSQL_COCHI_Debtor`](job_Extract_MSSQL_COCHI_Debtor.md) | CHI_DEBTOR |
| [`Extract_No_Dialer_Test_CHI`](job_Extract_No_Dialer_Test_CHI.md) | writes file |
| [`Extract_No_Dialer_Test_CO`](job_Extract_No_Dialer_Test_CO.md) | writes file |
| [`Extract_No_Dialer_Test_DC`](job_Extract_No_Dialer_Test_DC.md) | writes file |
| [`Extract_No_Dialer_Test_HH`](job_Extract_No_Dialer_Test_HH.md) | writes file |
| [`Extract_No_Dialer_Test_TOL`](job_Extract_No_Dialer_Test_TOL.md) | writes file |
| [`Extract_PRE_Hermes_Decile`](job_Extract_PRE_Hermes_Decile.md) | writes file |
| [`Extract_ProInsights_Data`](job_Extract_ProInsights_Data.md) | writes file |
| [`Extract_TOL_Hermes_Decile`](job_Extract_TOL_Hermes_Decile.md) | writes file |
| [`FactLetter_Load`](job_FactLetter_Load.md) | FACTLETTERS |
| [`FactPaymentManager_Load`](job_FactPaymentManager_Load.md) | FACTPAYMENTMANAGER |
| [`FactPostDates_Load`](job_FactPostDates_Load.md) | FACTPOSTDATES |
| [`FactTrans_Load`](job_FactTrans_Load.md) | FACTTRANS |
| [`FactTrans_TCODE_COLLECTOR_Load`](job_FactTrans_TCODE_COLLECTOR_Load.md) | TRANS_TCODE_COLLECTOR |
| [`Fact_Electronic_Media_Load`](job_Fact_Electronic_Media_Load.md) | orchestrator (see job list below) |
| [`Fran_Bai_Backlog`](job_Fran_Bai_Backlog.md) | writes file |
| [`HH_DEBTOR_SPECIAL_20231016_LOAD`](job_HH_DEBTOR_SPECIAL_20231016_LOAD.md) | HH_DEBTOR_LAST_BILL_DT |
| [`HH_EMedia_Load`](job_HH_EMedia_Load.md) | HH_EMESSAGE |
| [`HH_E_Media_Load`](job_HH_E_Media_Load.md) | HH_ELECTRONICSMEDIA |
| [`HH_TRANS_NORTHSHORE_LOAD`](job_HH_TRANS_NORTHSHORE_LOAD.md) | HH_TRANS_NORTHSHORE |
| [`HH_VAL_LTR_DATE_Backfill`](job_HH_VAL_LTR_DATE_Backfill.md) | TMP_HH_VAL_LTR_DATE |
| [`HOPE_Credit_Request`](job_HOPE_Credit_Request.md) | CREDIT_REQUEST |
| [`HOPE_Goals_Load`](job_HOPE_Goals_Load.md) | HOPE_GOALS |
| [`HOPE_Notes_Load`](job_HOPE_Notes_Load.md) | NOTES |
| [`HOPE_SPTransactions_Load`](job_HOPE_SPTransactions_Load.md) | TRANS |
| [`HOPE_Transactions_Load`](job_HOPE_Transactions_Load.md) | HOPE_TRANSACTION |
| [`HUB_Departments_Load`](job_HUB_Departments_Load.md) | DEPARTMENTS |
| [`HUB_HH_Employee_Load`](job_HUB_HH_Employee_Load.md) | HH_EMPLOYEES |
| [`HUB_Segments_Load`](job_HUB_Segments_Load.md) | SEGMENTS |
| [`HUB_Teams_Load`](job_HUB_Teams_Load.md) | TEAMS |
| [`HUB_TempTransaction_Load`](job_HUB_TempTransaction_Load.md) | TRANSACTIONTEMP |
| [`HUB_Transactions_Load`](job_HUB_Transactions_Load.md) | TRANSACTIONS |
| [`HealthPartners_Close_Reports_Extract`](job_HealthPartners_Close_Reports_Extract.md) | writes file |
| [`HealthPartners_Close_Rpt_Master`](job_HealthPartners_Close_Rpt_Master.md) | orchestrator (see job list below) |
| [`I3_CALLDETAIL_DEDOR_LOAD`](job_I3_CALLDETAIL_DEDOR_LOAD.md) | I3_CALLDETAIL_40 |
| [`IDOR_Amnesty_Extract`](job_IDOR_Amnesty_Extract.md) | writes file |
| [`INPUT_DIALER_LIST_GOV_Load`](job_INPUT_DIALER_LIST_GOV_Load.md) | INPUT_DIALER_LIST_UNIONED_GOV |
| [`INPUT_DIALER_LIST_HC_Load`](job_INPUT_DIALER_LIST_HC_Load.md) | INPUT_DIALER_LIST_UNIONED_HC |
| [`ISO_Request_Export`](job_ISO_Request_Export.md) | writes file |
| [`Initial_Ins_Discovery_V2_Decrypted`](job_Initial_Ins_Discovery_V2_Decrypted.md) | writes file |
| [`Initial_Insurance_Discovery_File`](job_Initial_Insurance_Discovery_File.md) | writes file |
| [`Ins_Cvg_Debtor_NPI_Load`](job_Ins_Cvg_Debtor_NPI_Load.md) | INS_CVG_DEBTOR_NPI |
| [`Insurance_Discovery_Load`](job_Insurance_Discovery_Load.md) | INSURANCE_DISCOVERY |
| [`Insurance_Discovery_Scrub_Extract`](job_Insurance_Discovery_Scrub_Extract.md) | writes file |
| [`Insurance_Discovery_Test`](job_Insurance_Discovery_Test.md) | writes file |
| [`Insurance_Report_Extract`](job_Insurance_Report_Extract.md) | writes file |
| [`LW_COC_Water_Scrub`](job_LW_COC_Water_Scrub.md) | writes file |
| [`LW_Carle_Asset_Scrub`](job_LW_Carle_Asset_Scrub.md) | writes file |
| [`LW_Dashboard_Base_Report`](job_LW_Dashboard_Base_Report.md) | writes file |
| [`LW_Dashboard_By_Agent`](job_LW_Dashboard_By_Agent.md) | writes file |
| [`LW_Dashboard_By_Metric`](job_LW_Dashboard_By_Metric.md) | writes file |
| [`LW_Delaware_Focus_Attributes`](job_LW_Delaware_Focus_Attributes.md) | writes file |
| [`LW_Delaware_Focus_Attributes_Granular`](job_LW_Delaware_Focus_Attributes_Granular.md) | writes file |
| [`LW_Delaware_Scorecard_Report`](job_LW_Delaware_Scorecard_Report.md) | writes file |
| [`LW_Deleware_Audit_Scorecard`](job_LW_Deleware_Audit_Scorecard.md) | writes file |
| [`LW_HPS_Audit_Scorecard`](job_LW_HPS_Audit_Scorecard.md) | writes file |
| [`LW_HPS_Focus_Attributes`](job_LW_HPS_Focus_Attributes.md) | writes file |
| [`LW_HPS_Focus_Attributes_Granular`](job_LW_HPS_Focus_Attributes_Granular.md) | writes file |
| [`LW_Insurance_Pmt_Tracking`](job_LW_Insurance_Pmt_Tracking.md) | writes file |
| [`LW_Lurie_Audit_Scorecard`](job_LW_Lurie_Audit_Scorecard.md) | writes file |
| [`LW_Lurie_Focus_Attributes`](job_LW_Lurie_Focus_Attributes.md) | writes file |
| [`LW_Lurie_Focus_Attributes_Granular`](job_LW_Lurie_Focus_Attributes_Granular.md) | writes file |
| [`LW_Manual_Audit_Scorecard`](job_LW_Manual_Audit_Scorecard.md) | writes file |
| [`LW_ProMedica_Scrub`](job_LW_ProMedica_Scrub.md) | writes file |
| [`LW_Property_Scrub`](job_LW_Property_Scrub.md) | writes file |
| [`LW_REPORTS`](job_LW_REPORTS.md) | writes file |
| [`LW_REPORTS_2`](job_LW_REPORTS_2.md) | writes file |
| [`LW_TPL_PMT_REPORT`](job_LW_TPL_PMT_REPORT.md) | writes file |
| [`Last4SSN_Extract`](job_Last4SSN_Extract.md) | LAST4SSN |
| [`LegalMatch_Extract`](job_LegalMatch_Extract.md) | writes file |
| [`Legal_Asset_Scrub_Champaign_County_Extract`](job_Legal_Asset_Scrub_Champaign_County_Extract.md) | writes file |
| [`Legal_Asset_Scrub_Illinois_Counties_Extract`](job_Legal_Asset_Scrub_Illinois_Counties_Extract.md) | writes file |
| [`Legal_Asset_Scrub_Illinois_Counties_Extract_2`](job_Legal_Asset_Scrub_Illinois_Counties_Extract_2.md) | writes file |
| [`Legal_Asset_Scrub_KDOR_Extract`](job_Legal_Asset_Scrub_KDOR_Extract.md) | writes file |
| [`Livevox_Daily_Load`](job_Livevox_Daily_Load.md) | LIVEVOX_CALLS |
| [`Livevox_Sample_Load`](job_Livevox_Sample_Load.md) | LIVEVOX_CALLS |
| [`LoadLegalRpt20231130`](job_LoadLegalRpt20231130.md) | writes file |
| [`Load_837_Files`](job_Load_837_Files.md) | — |
| [`Load_Attunely_Data`](job_Load_Attunely_Data.md) | ATTUNELY_PERFORM_DATA |
| [`Load_Debtor_New_Columns`](job_Load_Debtor_New_Columns.md) | SPRING_FOUR |
| [`Load_Employee_Collector_History`](job_Load_Employee_Collector_History.md) | EMPLOYEE_COLLECTOR_HISTORY |
| [`Load_Evergreen_Hours`](job_Load_Evergreen_Hours.md) | EVERGREEN_AGENT_HOURS |
| [`Load_HH_Debtor_Special_20251222`](job_Load_HH_Debtor_Special_20251222.md) | HH_DEBTOR_SPECIAL_20251222 |
| [`Load_Misc_Dims`](job_Load_Misc_Dims.md) | DIMLOGON, DIMDESKINFO, DIMEMPLOYEEINFO |
| [`Load_PCI_Letter_Disp_Desc`](job_Load_PCI_Letter_Disp_Desc.md) | PCI_Letter_Disp |
| [`MBoich_Experian_Extracts`](job_MBoich_Experian_Extracts.md) | writes file |
| [`Mail_Merge_Load`](job_Mail_Merge_Load.md) | MAIL_MERGE |
| [`MaxRTE_Request_Export`](job_MaxRTE_Request_Export.md) | writes file |
| [`MaxRTE_Result_Load`](job_MaxRTE_Result_Load.md) | MAXRTE_RESPONSE_LOG |
| [`Migrating_Clients_20260424`](job_Migrating_Clients_20260424.md) | UTILITY_CLIENT_EXCLUDE_LIST |
| [`Northwestern_Future_Appts`](job_Northwestern_Future_Appts.md) | NORTHWESTERN_UPCOMING_APPTS |
| [`Notes_Load`](job_Notes_Load.md) | NOTES |
| [`PA_Turnpike_Load`](job_PA_Turnpike_Load.md) | PA_TURNPIKE |
| [`PCI_LETTERS_TO_DELETE`](job_PCI_LETTERS_TO_DELETE.md) | PCI_LETTERS_TO_DELETE |
| [`PCI_Letter_Load`](job_PCI_Letter_Load.md) | PCI_LETTERS |
| [`PDC_Plan_Txn_Backfill`](job_PDC_Plan_Txn_Backfill.md) | TMP_TRANS_BACKFILE |
| [`PRE_E_Media_Load`](job_PRE_E_Media_Load.md) | PRE_ELECTRONICSMEDIA |
| [`PV_PostDate_Export_Load`](job_PV_PostDate_Export_Load.md) | PV_POSTDATE |
| [`PaymentPlan_Legacy_Load`](job_PaymentPlan_Legacy_Load.md) | PAYMENTPLAN |
| [`PaymentPlan_Load`](job_PaymentPlan_Load.md) | orchestrator (see job list below) |
| [`PaymentVision_Activity_Load`](job_PaymentVision_Activity_Load.md) | PAYMENTVISION_ACTIVITY |
| [`ProInsight_Analytics_Load`](job_ProInsight_Analytics_Load.md) | PROINSIGHT_ANALYTICS |
| [`ProInsight_CCU_Scorecard_Load`](job_ProInsight_CCU_Scorecard_Load.md) | PROINSIGHT_CCU_SCORECARD |
| [`ProInsight_CCU_Scorecard_V2_Load`](job_ProInsight_CCU_Scorecard_V2_Load.md) | PROINSIGHT_CCU_V2_SCORECARD |
| [`ProInsight_HPS_Scorecard_Load`](job_ProInsight_HPS_Scorecard_Load.md) | PROINSIGHT_HPS_SCORECARD |
| [`ProInsight_Scorecard_Load`](job_ProInsight_Scorecard_Load.md) | PROINSIGHT_SCORECARD |
| [`Raw_PCI_Letter_Load`](job_Raw_PCI_Letter_Load.md) | PCI_LETTERS, DEBTOR_ADDRESSES |
| [`SMS_IC_Inbound_Load`](job_SMS_IC_Inbound_Load.md) | TEXTS_IC_INBOUND |
| [`SMS_IC_Outbound_Load`](job_SMS_IC_Outbound_Load.md) | TEXTS_IC_OUTBOUND |
| [`SMS_IC_Outbound_Load_Backfill`](job_SMS_IC_Outbound_Load_Backfill.md) | TEXTS_IC_OUTBOUND |
| [`SMS_Inbound_Load`](job_SMS_Inbound_Load.md) | TEXTS_SBT_INBOUND |
| [`SMS_Outbound_Load`](job_SMS_Outbound_Load.md) | TEXTS_SBT_OUTBOUND |
| [`Semaphore_Check`](job_Semaphore_Check.md) | — |
| [`SendGrid_Report_Load`](job_SendGrid_Report_Load.md) | FACT_EMAILS_SENDGRID |
| [`Skip_Costs_Load`](job_Skip_Costs_Load.md) | SKIP_COSTS |
| [`TEST_Avita_Monthly_Report_Extract`](job_TEST_Avita_Monthly_Report_Extract.md) | writes file |
| [`TEST_Date_Params`](job_TEST_Date_Params.md) | — |
| [`TEST_Email_Alerts`](job_TEST_Email_Alerts.md) | — |
| [`Test_Decryption`](job_Test_Decryption.md) | writes file |
| [`Test_Encryption`](job_Test_Encryption.md) | writes file |
| [`Top_N_Accounts_All_Extract`](job_Top_N_Accounts_All_Extract.md) | writes file |
| [`Top_N_Accounts_Extract`](job_Top_N_Accounts_Extract.md) | writes file |
| [`Touchstar_DNC_Load`](job_Touchstar_DNC_Load.md) | TOUCHSTAR_DONOTCALL_STAGING |
| [`Trans_History_Load`](job_Trans_History_Load.md) | TEMP_TRANS |
| [`VAT_1394_Load`](job_VAT_1394_Load.md) | VAT_1394 |
| [`VA_Tax_Inventory_Report`](job_VA_Tax_Inventory_Report.md) | writes file |
| [`VA_Tax_Report_Load`](job_VA_Tax_Report_Load.md) | VA_TAX_RECON_REPORT |
| [`VA_Tax_Report_Split`](job_VA_Tax_Report_Split.md) | writes file |
| [`Voapp_File_Load`](job_Voapp_File_Load.md) | VOAPPS |
| [`i3_AgentActivityLog_Load`](job_i3_AgentActivityLog_Load.md) | I3_AGENTACTIVITYLOG |
| [`i3_AgentQueueStats_Load`](job_i3_AgentQueueStats_Load.md) | I3_AGENTQUEUESTATS |
| [`i3_AgentStats`](job_i3_AgentStats.md) | I3_AGENTSTATS |
| [`i3_CRC_Load`](job_i3_CRC_Load.md) | I3_CRC |
| [`i3_CallDetail_40_Load`](job_i3_CallDetail_40_Load.md) | I3_CALLDETAIL_40 |
| [`i3_CallDetail_40_Load_Copy`](job_i3_CallDetail_40_Load_Copy.md) | I3_CALLDETAIL_40 |
| [`i3_CallDetail_viw_Load`](job_i3_CallDetail_viw_Load.md) | I3_CALLDETAIL_VIW |
| [`i3_CallHistory_Load`](job_i3_CallHistory_Load.md) | I3_CALLHISTORY |
| [`i3_Call_Detail_View_Init_Load`](job_i3_Call_Detail_View_Init_Load.md) | — |
| [`i3_Campaign_Type_Load`](job_i3_Campaign_Type_Load.md) | I3_CAMPAIGN_TYPE |
| [`i3_DialerCallListCHI_Load`](job_i3_DialerCallListCHI_Load.md) | I3_DIALERCALLLIST_CHI |
| [`i3_DialerCallListCO_Load`](job_i3_DialerCallListCO_Load.md) | I3_DIALERCALLLIST_CO |
| [`i3_DialerCallListCO_Load_Backup`](job_i3_DialerCallListCO_Load_Backup.md) | I3_DIALERCALLLIST_CO |
| [`i3_DialerCallListDC_Load`](job_i3_DialerCallListDC_Load.md) | I3_DIALERCALLLIST_DC |
| [`i3_DialerCallListDC_Load_Backup`](job_i3_DialerCallListDC_Load_Backup.md) | I3_DIALERCALLLIST_DC |
| [`i3_DialerCallListHH_Load`](job_i3_DialerCallListHH_Load.md) | I3_DIALERCALLLIST_HH |
| [`i3_DialerCallListHH_Load_Backup`](job_i3_DialerCallListHH_Load_Backup.md) | I3_DIALERCALLLIST_HH |
| [`i3_DialerCallListPRE_Load`](job_i3_DialerCallListPRE_Load.md) | I3_DIALERCALLLIST_PRE |
| [`i3_DialerCallListTOL_Load`](job_i3_DialerCallListTOL_Load.md) | I3_DIALERCALLLIST_TOL |
| [`i3_DialerCallListTOL_Load_Backup`](job_i3_DialerCallListTOL_Load_Backup.md) | I3_DIALERCALLLIST_TOL |
| [`i3_DialerCallList_DEDOR_Load`](job_i3_DialerCallList_DEDOR_Load.md) | I3_DIALERCALLLIST_DEDOR |
| [`i3_Individual_Load`](job_i3_Individual_Load.md) | I3_INDIVIDUAL |
| [`i3_InteractionCustomAttributes_Load`](job_i3_InteractionCustomAttributes_Load.md) | I3_INTERACTIONCUSTOMATTRIBUTES |
| [`i3_InteractionSummaryEx_Load`](job_i3_InteractionSummaryEx_Load.md) | I3_INTERACTIONSUMMARYEX |
| [`i3_InteractionSummary_Load`](job_i3_InteractionSummary_Load.md) | I3_INTERACTIONSUMMARY |
| [`i3_InteractionWrapup_Load`](job_i3_InteractionWrapup_Load.md) | I3_INTERACTIONWRAPUP |
| [`master_prediction_proposal_cubs_extract`](job_master_prediction_proposal_cubs_extract.md) | writes file |
