# Talend Jobs Index — LATITUDE Project

56 jobs. Click any job name to open its full documentation. See [`../../01_system_architecture.md`](../../01_system_architecture.md), [`../../04_data_lineage_map.md`](../../04_data_lineage_map.md), [`../../05_operational_runbook.md`](../../05_operational_runbook.md), and [`../../06_dependency_matrix.md`](../../06_dependency_matrix.md) for the platform-wide picture.

## Gatekeeper & alert-only jobs (no data load)

| Job | What it does |
|---|---|
| [`Export_File_Check`](job_Export_File_Check.md) | Waits up to ~4 hours for an upstream "export done" marker file; emails and fails the run if it never appears. |
| [`Plan_Success_Alert`](job_Plan_Success_Alert.md) | Single-component job that only sends a notification email. |

## Reverse-direction jobs (Snowflake → file export)

| Job | Target Snowflake table | What it does |
|---|---|---|
| [`Hermes_Latitude_Recommendations`](job_Hermes_Latitude_Recommendations.md) | reads from Snowflake | Exports recommendation data from Snowflake out to a delimited file. |
| [`Master_Config_Val_Segs_Export`](job_Master_Config_Val_Segs_Export.md) | reads from Snowflake | Exports configuration/validation segment data from Snowflake to a file. |
| [`Master_Prediction_Scores_Export`](job_Master_Prediction_Scores_Export.md) | reads from Snowflake | Exports prediction scores from Snowflake to a file. |

## Jobs with explicit merge-result checking (`tDie`/`tWarn` on the Snowflake merge outcome)

| Job | Target table | Notes |
|---|---|---|
| [`Dialer_CallTracking_Load`](job_Dialer_CallTracking_Load.md) | DIALER_CALLTRACKING |  |
| [`Export_File_Check`](job_Export_File_Check.md) | — |  |
| [`HH_Violation_Text_Load`](job_HH_Violation_Text_Load.md) | HH_VIOLATION |  |
| [`Livevox_Daily_Load`](job_Livevox_Daily_Load.md) | LIVEVOX_CALLS |  |
| [`PatientInfo_Text_Load`](job_PatientInfo_Text_Load.md) | PATIENTINFO |  |
| [`cmi_Hermes_Recommendations_Load`](job_cmi_Hermes_Recommendations_Load.md) | CMI_HERMES_RECOMMENDATIONS |  |
| [`cmi_VoApp_Results_Load`](job_cmi_VoApp_Results_Load.md) | CMI_VOAPPS_RESULTS |  |
| [`master_prediction_proposal_Load`](job_master_prediction_proposal_Load.md) | MASTER_PREDICTION_PROPOSAL | calls an INSERT procedure, not a MERGE — see Issues observed |

## Extract / utility outlier

| Job | Target table | What it does |
|---|---|---|
| [`Last4SSN_Extract`](job_Last4SSN_Extract.md) | LAST4SSN | Reads from Snowflake, decrypts SSNs, extracts the last 4 digits, and inserts into `LAST4SSN` — no truncate/merge step found (see Issues observed in that doc). |

## Standard file → Snowflake staging → merge loads

All of the following follow the pattern documented in full in [`job_Address_Text_Load.md`](job_Address_Text_Load.md): watch `context.sourceDir` for a delimited file, load it into a `LIQUID_STAGING`-schema staging table, merge into the permanent table, then archive and delete the source file. Check each job's own doc for its specific table name, file format, and any deviation.

| Job | Target Snowflake table |
|---|---|
| [`Address_Text_Load`](job_Address_Text_Load.md) | ADDRESS |
| [`Bankruptcy_Text_Load`](job_Bankruptcy_Text_Load.md) | BANKRUPTCY |
| [`CBR_Metro2_Accounts_Table_Text_Load`](job_CBR_Metro2_Accounts_Table_Text_Load.md) | CBR_METRO2_ACCOUNTS_TXT |
| [`Carrier_Text_Load`](job_Carrier_Text_Load.md) | CARRIER |
| [`Custom_cmi_Email_Text_Load`](job_Custom_cmi_Email_Text_Load.md) | CUSTOM_CMI_EMAIL_TXT |
| [`Customer_Table_Text_Load`](job_Customer_Table_Text_Load.md) | CUSTOMER_TXT |
| [`DebtorCC_Table_Text_Load`](job_DebtorCC_Table_Text_Load.md) | DEBTORCREDITCARDS_TXT |
| [`Debtor_Table_Text_Load`](job_Debtor_Table_Text_Load.md) | DEBTOR_TXT |
| [`Deceased_Text_Load`](job_Deceased_Text_Load.md) | DECEASED |
| [`DeskChangeHistory_Text_Load`](job_DeskChangeHistory_Text_Load.md) | DESKCHANGEHISTORY |
| [`Desk_Text_Load`](job_Desk_Text_Load.md) | DESK |
| [`Email_Text_Load`](job_Email_Text_Load.md) | EMAIL_TXT |
| [`Insurance_Text_Load`](job_Insurance_Text_Load.md) | INSURANCE |
| [`LetterRequest_Table_Text_Load`](job_LetterRequest_Table_Text_Load.md) | LETTERREQUEST_TXT |
| [`LetterType_Text_Load`](job_LetterType_Text_Load.md) | LETTERTYPE_TXT |
| [`Master_Special_Info_Text_Load`](job_Master_Special_Info_Text_Load.md) | MASTER_SPECIAL_INFO_TXT |
| [`Master_Table_Text_Load`](job_Master_Table_Text_Load.md) | MASTER_TXT |
| [`Master_Table_Text_Load_HC15`](job_Master_Table_Text_Load_HC15.md) | MASTER_TXT |
| [`MiscExtra_Text_Load`](job_MiscExtra_Text_Load.md) | MISCEXTRA_TXT |
| [`PDC_Text_Load`](job_PDC_Text_Load.md) | PDC_TXT |
| [`PayHistory_Table_Text_Load`](job_PayHistory_Table_Text_Load.md) | PAYHIST_TXT |
| [`Phones_Consent_Table_Text_Load`](job_Phones_Consent_Table_Text_Load.md) | PHONES_CONSENT_TXT |
| [`Phones_Master_Table_Text_Load`](job_Phones_Master_Table_Text_Load.md) | PHONES_MASTER_TXT |
| [`Promises_Text_Load`](job_Promises_Text_Load.md) | PROMISES_TXT |
| [`Result_Table_Text_Load`](job_Result_Table_Text_Load.md) | RESULT_TXT |
| [`Roles_Text_Load`](job_Roles_Text_Load.md) | ROLES |
| [`ScheduledPayment_Text_Load`](job_ScheduledPayment_Text_Load.md) | SCHEDULEDPAYMENT_TXT |
| [`ServiceHistory_Text_Load`](job_ServiceHistory_Text_Load.md) | SERVICEHISTORY_TXT |
| [`Services_LexisNexis_Batch_A2_Text_Load`](job_Services_LexisNexis_Batch_A2_Text_Load.md) | SERVICES_LEXISNEXIS_BATCH_A2_TXT |
| [`StatusHistory_Text_Load`](job_StatusHistory_Text_Load.md) | STATUSHISTORY_TXT |
| [`Users_Text_Load`](job_Users_Text_Load.md) | Users |
| [`ValidationNotice_Text_Load`](job_ValidationNotice_Text_Load.md) | VALIDATIONNOTICE |
| [`Voapps_Response_Load`](job_Voapps_Response_Load.md) | VOAPPS |
| [`cmi_CapioSellerContracts_Table_Text_Load`](job_cmi_CapioSellerContracts_Table_Text_Load.md) | CMI_CAPIOSELLERCONTRACTS_TXT |
| [`cmi_CustomerGrouping_Text_Load`](job_cmi_CustomerGrouping_Text_Load.md) | CMI_CUSTOMERGROUPING_TXT |
| [`cmi_Customer_Ext_Text_Load`](job_cmi_Customer_Ext_Text_Load.md) | CMI_CUSTOMER_EXT_TXT |
| [`cmi_Dialer_Plan_History_Table_Text_Load`](job_cmi_Dialer_Plan_History_Table_Text_Load.md) | cmi_Dialer_Plan_History_TXT |
| [`cmi_Dialer_SBT_History_Table_Text_Load`](job_cmi_Dialer_SBT_History_Table_Text_Load.md) | CMI_DIALER_SBT_HISTORY_TXT |
| [`cmi_Score_Text_Load`](job_cmi_Score_Text_Load.md) | CMI_SCORE_TXT |
| [`cmi_dialer_SubscriberStatusHistory_Text_Load`](job_cmi_dialer_SubscriberStatusHistory_Text_Load.md) | CMI_DIALER_SUBSCRIBERSTATUSHISTORY_TXT |
| [`cmi_dialer_SubscriberStatus_Text_Load`](job_cmi_dialer_SubscriberStatus_Text_Load.md) | CMI_DIALER_SUBSCRIBERSTATUS_TXT |
| [`cmi_renkim_ReturnHistory_Text_Load`](job_cmi_renkim_ReturnHistory_Text_Load.md) | CMI_RENKIM_RETURNHISTORY_TXT |
| [`letter_Text_Load`](job_letter_Text_Load.md) | LETTER_TXT |

## Full alphabetical list (all 56 jobs)

| Job | Target Snowflake table |
|---|---|
| [`Address_Text_Load`](job_Address_Text_Load.md) | ADDRESS |
| [`Bankruptcy_Text_Load`](job_Bankruptcy_Text_Load.md) | BANKRUPTCY |
| [`CBR_Metro2_Accounts_Table_Text_Load`](job_CBR_Metro2_Accounts_Table_Text_Load.md) | CBR_METRO2_ACCOUNTS_TXT |
| [`Carrier_Text_Load`](job_Carrier_Text_Load.md) | CARRIER |
| [`Custom_cmi_Email_Text_Load`](job_Custom_cmi_Email_Text_Load.md) | CUSTOM_CMI_EMAIL_TXT |
| [`Customer_Table_Text_Load`](job_Customer_Table_Text_Load.md) | CUSTOMER_TXT |
| [`DebtorCC_Table_Text_Load`](job_DebtorCC_Table_Text_Load.md) | DEBTORCREDITCARDS_TXT |
| [`Debtor_Table_Text_Load`](job_Debtor_Table_Text_Load.md) | DEBTOR_TXT |
| [`Deceased_Text_Load`](job_Deceased_Text_Load.md) | DECEASED |
| [`DeskChangeHistory_Text_Load`](job_DeskChangeHistory_Text_Load.md) | DESKCHANGEHISTORY |
| [`Desk_Text_Load`](job_Desk_Text_Load.md) | DESK |
| [`Dialer_CallTracking_Load`](job_Dialer_CallTracking_Load.md) | DIALER_CALLTRACKING |
| [`Email_Text_Load`](job_Email_Text_Load.md) | EMAIL_TXT |
| [`Export_File_Check`](job_Export_File_Check.md) | — |
| [`HH_Violation_Text_Load`](job_HH_Violation_Text_Load.md) | HH_VIOLATION |
| [`Hermes_Latitude_Recommendations`](job_Hermes_Latitude_Recommendations.md) | reads Snowflake, writes file |
| [`Insurance_Text_Load`](job_Insurance_Text_Load.md) | INSURANCE |
| [`Last4SSN_Extract`](job_Last4SSN_Extract.md) | LAST4SSN |
| [`LetterRequest_Table_Text_Load`](job_LetterRequest_Table_Text_Load.md) | LETTERREQUEST_TXT |
| [`LetterType_Text_Load`](job_LetterType_Text_Load.md) | LETTERTYPE_TXT |
| [`Livevox_Daily_Load`](job_Livevox_Daily_Load.md) | LIVEVOX_CALLS |
| [`Master_Config_Val_Segs_Export`](job_Master_Config_Val_Segs_Export.md) | reads Snowflake, writes file |
| [`Master_Prediction_Scores_Export`](job_Master_Prediction_Scores_Export.md) | reads Snowflake, writes file |
| [`Master_Special_Info_Text_Load`](job_Master_Special_Info_Text_Load.md) | MASTER_SPECIAL_INFO_TXT |
| [`Master_Table_Text_Load`](job_Master_Table_Text_Load.md) | MASTER_TXT |
| [`Master_Table_Text_Load_HC15`](job_Master_Table_Text_Load_HC15.md) | MASTER_TXT |
| [`MiscExtra_Text_Load`](job_MiscExtra_Text_Load.md) | MISCEXTRA_TXT |
| [`PDC_Text_Load`](job_PDC_Text_Load.md) | PDC_TXT |
| [`PatientInfo_Text_Load`](job_PatientInfo_Text_Load.md) | PATIENTINFO |
| [`PayHistory_Table_Text_Load`](job_PayHistory_Table_Text_Load.md) | PAYHIST_TXT |
| [`Phones_Consent_Table_Text_Load`](job_Phones_Consent_Table_Text_Load.md) | PHONES_CONSENT_TXT |
| [`Phones_Master_Table_Text_Load`](job_Phones_Master_Table_Text_Load.md) | PHONES_MASTER_TXT |
| [`Plan_Success_Alert`](job_Plan_Success_Alert.md) | — |
| [`Promises_Text_Load`](job_Promises_Text_Load.md) | PROMISES_TXT |
| [`Result_Table_Text_Load`](job_Result_Table_Text_Load.md) | RESULT_TXT |
| [`Roles_Text_Load`](job_Roles_Text_Load.md) | ROLES |
| [`ScheduledPayment_Text_Load`](job_ScheduledPayment_Text_Load.md) | SCHEDULEDPAYMENT_TXT |
| [`ServiceHistory_Text_Load`](job_ServiceHistory_Text_Load.md) | SERVICEHISTORY_TXT |
| [`Services_LexisNexis_Batch_A2_Text_Load`](job_Services_LexisNexis_Batch_A2_Text_Load.md) | SERVICES_LEXISNEXIS_BATCH_A2_TXT |
| [`StatusHistory_Text_Load`](job_StatusHistory_Text_Load.md) | STATUSHISTORY_TXT |
| [`Users_Text_Load`](job_Users_Text_Load.md) | Users |
| [`ValidationNotice_Text_Load`](job_ValidationNotice_Text_Load.md) | VALIDATIONNOTICE |
| [`Voapps_Response_Load`](job_Voapps_Response_Load.md) | VOAPPS |
| [`cmi_CapioSellerContracts_Table_Text_Load`](job_cmi_CapioSellerContracts_Table_Text_Load.md) | CMI_CAPIOSELLERCONTRACTS_TXT |
| [`cmi_CustomerGrouping_Text_Load`](job_cmi_CustomerGrouping_Text_Load.md) | CMI_CUSTOMERGROUPING_TXT |
| [`cmi_Customer_Ext_Text_Load`](job_cmi_Customer_Ext_Text_Load.md) | CMI_CUSTOMER_EXT_TXT |
| [`cmi_Dialer_Plan_History_Table_Text_Load`](job_cmi_Dialer_Plan_History_Table_Text_Load.md) | cmi_Dialer_Plan_History_TXT |
| [`cmi_Dialer_SBT_History_Table_Text_Load`](job_cmi_Dialer_SBT_History_Table_Text_Load.md) | CMI_DIALER_SBT_HISTORY_TXT |
| [`cmi_Hermes_Recommendations_Load`](job_cmi_Hermes_Recommendations_Load.md) | CMI_HERMES_RECOMMENDATIONS |
| [`cmi_Score_Text_Load`](job_cmi_Score_Text_Load.md) | CMI_SCORE_TXT |
| [`cmi_VoApp_Results_Load`](job_cmi_VoApp_Results_Load.md) | CMI_VOAPPS_RESULTS |
| [`cmi_dialer_SubscriberStatusHistory_Text_Load`](job_cmi_dialer_SubscriberStatusHistory_Text_Load.md) | CMI_DIALER_SUBSCRIBERSTATUSHISTORY_TXT |
| [`cmi_dialer_SubscriberStatus_Text_Load`](job_cmi_dialer_SubscriberStatus_Text_Load.md) | CMI_DIALER_SUBSCRIBERSTATUS_TXT |
| [`cmi_renkim_ReturnHistory_Text_Load`](job_cmi_renkim_ReturnHistory_Text_Load.md) | CMI_RENKIM_RETURNHISTORY_TXT |
| [`letter_Text_Load`](job_letter_Text_Load.md) | LETTER_TXT |
| [`master_prediction_proposal_Load`](job_master_prediction_proposal_Load.md) | MASTER_PREDICTION_PROPOSAL |
