# Dependency Matrix

## Tooling note

`talend_extractor.py`'s `JobMetadata.context_groups` field is defined but never populated by the extractor. Context-variable usage below is instead inferred by scanning component parameter values for `context.` references — a reasonable proxy, but it may miss indirect usage (e.g. variables passed through tRunJob context propagation).

## Jobs → database connection

`Liquid_0.1` — no component family in the job set correlates to this connection's name.

`TalendLog_0.1` — no component family in the job set correlates to this connection's name.

**54 job(s)** use `Snowflake`-family components with no matching defined connection:

- `Address_Text_Load`
- `Bankruptcy_Text_Load`
- `CBR_Metro2_Accounts_Table_Text_Load`
- `Carrier_Text_Load`
- `Custom_cmi_Email_Text_Load`
- `Customer_Table_Text_Load`
- `DebtorCC_Table_Text_Load`
- `Debtor_Table_Text_Load`
- `Deceased_Text_Load`
- `DeskChangeHistory_Text_Load`
- `Desk_Text_Load`
- `Dialer_CallTracking_Load`
- `Email_Text_Load`
- `HH_Violation_Text_Load`
- `Hermes_Latitude_Recommendations`
- `Insurance_Text_Load`
- `Last4SSN_Extract`
- `LetterRequest_Table_Text_Load`
- `LetterType_Text_Load`
- `Livevox_Daily_Load`
- `Master_Config_Val_Segs_Export`
- `Master_Prediction_Scores_Export`
- `Master_Special_Info_Text_Load`
- `Master_Table_Text_Load`
- `Master_Table_Text_Load_HC15`
- `MiscExtra_Text_Load`
- `PDC_Text_Load`
- `PatientInfo_Text_Load`
- `PayHistory_Table_Text_Load`
- `Phones_Consent_Table_Text_Load`
- `Phones_Master_Table_Text_Load`
- `Promises_Text_Load`
- `Result_Table_Text_Load`
- `Roles_Text_Load`
- `ScheduledPayment_Text_Load`
- `ServiceHistory_Text_Load`
- `Services_LexisNexis_Batch_A2_Text_Load`
- `StatusHistory_Text_Load`
- `Users_Text_Load`
- `ValidationNotice_Text_Load`
- `Voapps_Response_Load`
- `cmi_CapioSellerContracts_Table_Text_Load`
- `cmi_CustomerGrouping_Text_Load`
- `cmi_Customer_Ext_Text_Load`
- `cmi_Dialer_Plan_History_Table_Text_Load`
- `cmi_Dialer_SBT_History_Table_Text_Load`
- `cmi_Hermes_Recommendations_Load`
- `cmi_Score_Text_Load`
- `cmi_VoApp_Results_Load`
- `cmi_dialer_SubscriberStatusHistory_Text_Load`
- `cmi_dialer_SubscriberStatus_Text_Load`
- `cmi_renkim_ReturnHistory_Text_Load`
- `letter_Text_Load`
- `master_prediction_proposal_Load`

**1 job(s)** use `Filter`-family components with no matching defined connection:

- `Last4SSN_Extract`

**13 job(s)** use `Java`-family components with no matching defined connection:

- `Address_Text_Load`
- `Debtor_Table_Text_Load`
- `DeskChangeHistory_Text_Load`
- `Desk_Text_Load`
- `Dialer_CallTracking_Load`
- `HH_Violation_Text_Load`
- `Last4SSN_Extract`
- `MiscExtra_Text_Load`
- `PatientInfo_Text_Load`
- `Users_Text_Load`
- `cmi_Hermes_Recommendations_Load`
- `cmi_VoApp_Results_Load`
- `master_prediction_proposal_Load`

## Jobs → context group (Directories_0.1, LEGACY_DW_0.1)

**56 job(s)** reference `context.*` in a component parameter:

- `Address_Text_Load`
- `Bankruptcy_Text_Load`
- `CBR_Metro2_Accounts_Table_Text_Load`
- `Carrier_Text_Load`
- `Custom_cmi_Email_Text_Load`
- `Customer_Table_Text_Load`
- `DebtorCC_Table_Text_Load`
- `Debtor_Table_Text_Load`
- `Deceased_Text_Load`
- `DeskChangeHistory_Text_Load`
- `Desk_Text_Load`
- `Dialer_CallTracking_Load`
- `Email_Text_Load`
- `Export_File_Check`
- `HH_Violation_Text_Load`
- `Hermes_Latitude_Recommendations`
- `Insurance_Text_Load`
- `Last4SSN_Extract`
- `LetterRequest_Table_Text_Load`
- `LetterType_Text_Load`
- `Livevox_Daily_Load`
- `Master_Config_Val_Segs_Export`
- `Master_Prediction_Scores_Export`
- `Master_Special_Info_Text_Load`
- `Master_Table_Text_Load`
- `Master_Table_Text_Load_HC15`
- `MiscExtra_Text_Load`
- `PDC_Text_Load`
- `PatientInfo_Text_Load`
- `PayHistory_Table_Text_Load`
- `Phones_Consent_Table_Text_Load`
- `Phones_Master_Table_Text_Load`
- `Plan_Success_Alert`
- `Promises_Text_Load`
- `Result_Table_Text_Load`
- `Roles_Text_Load`
- `ScheduledPayment_Text_Load`
- `ServiceHistory_Text_Load`
- `Services_LexisNexis_Batch_A2_Text_Load`
- `StatusHistory_Text_Load`
- `Users_Text_Load`
- `ValidationNotice_Text_Load`
- `Voapps_Response_Load`
- `cmi_CapioSellerContracts_Table_Text_Load`
- `cmi_CustomerGrouping_Text_Load`
- `cmi_Customer_Ext_Text_Load`
- `cmi_Dialer_Plan_History_Table_Text_Load`
- `cmi_Dialer_SBT_History_Table_Text_Load`
- `cmi_Hermes_Recommendations_Load`
- `cmi_Score_Text_Load`
- `cmi_VoApp_Results_Load`
- `cmi_dialer_SubscriberStatusHistory_Text_Load`
- `cmi_dialer_SubscriberStatus_Text_Load`
- `cmi_renkim_ReturnHistory_Text_Load`
- `letter_Text_Load`
- `master_prediction_proposal_Load`

## Job → job (tRunJob orchestration)

```mermaid
graph TD
```
