# Job-by-Job Documentation


56 job(s) across 1 project(s). Grouped by inferred kind rather than one write-up per job, so large sets of near-identical tutorial/demo jobs don't drown out the jobs that actually move data.

## Kind breakdown

| Kind | Count | What it means |
|---|---|---|
| read-only / preview | 50 | Reads data but only logs/previews it — no persisted output |
| utility | 6 | Neither a clear pipeline nor a named component match |

## Read-only / preview jobs

| Job | Description |
|---|---|
| `Address_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Bankruptcy_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `CBR_Metro2_Accounts_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Carrier_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Custom_cmi_Email_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Customer_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `DebtorCC_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Debtor_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Deceased_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `DeskChangeHistory_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Desk_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Dialer_CallTracking_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Email_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `HH_Violation_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Insurance_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `LetterRequest_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `LetterType_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Livevox_Daily_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Master_Special_Info_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Master_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Master_Table_Text_Load_HC15` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `MiscExtra_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `PDC_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `PatientInfo_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `PayHistory_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Phones_Consent_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Phones_Master_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Promises_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Result_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Roles_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ScheduledPayment_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ServiceHistory_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Services_LexisNexis_Batch_A2_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `StatusHistory_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Users_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `ValidationNotice_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `Voapps_Response_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_CapioSellerContracts_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_CustomerGrouping_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_Customer_Ext_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_Dialer_Plan_History_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_Dialer_SBT_History_Table_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_Hermes_Recommendations_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_Score_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_VoApp_Results_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_dialer_SubscriberStatusHistory_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_dialer_SubscriberStatus_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `cmi_renkim_ReturnHistory_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `letter_Text_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |
| `master_prediction_proposal_Load` | Reads via ['tFileInputDelimited']; no output target found in the extracted metadata. |

## Utility jobs

| Job | Description |
|---|---|
| `Export_File_Check` | Utility/demo job using: ['tDie', 'tFileCopy', 'tJava', 'tSendMail', 'tWaitForFile']. Not a source-to-target data pipeline. |
| `Hermes_Latitude_Recommendations` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Last4SSN_Extract` | Utility/demo job using: ['tDataDecrypt', 'tFilterRow', 'tJavaRow', 'tPrejob', 'tSetKeystore', 'tSnowflakeConnection', 'tSnowflakeInput', 'tSnowflakeOutput']. Not a source-to-target data pipeline. |
| `Master_Config_Val_Segs_Export` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Master_Prediction_Scores_Export` | Utility/demo job using: ['tFileOutputDelimited', 'tSetKeystore', 'tSnowflakeInput']. Not a source-to-target data pipeline. |
| `Plan_Success_Alert` | Utility/demo job using: ['tSendMail']. Not a source-to-target data pipeline. |
