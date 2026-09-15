# Operational Runbook


## Scope limitation

This extraction contains no scheduling/execution metadata — `talend_extractor.py` reads job *definitions* only (not Talend Administration Center execution plans), and Qlik reload tasks are read directly from the tenant. Run `talend_cloud_extractor.py` and pass its output via --talend-cloud for schedule/execution info. This section covers what monitoring/restart guidance the definitions themselves imply.

## Jobs with explicit failure/warning logic

| Job | Components | Guidance |
|---|---|---|
| `cmi_Hermes_Recommendations_Load` | ['tDie', 'tWarn'] | Check Talend job execution logs for the triggering condition before retrying |
| `cmi_VoApp_Results_Load` | ['tDie', 'tWarn'] | Check Talend job execution logs for the triggering condition before retrying |
| `Dialer_CallTracking_Load` | ['tDie', 'tWarn'] | Check Talend job execution logs for the triggering condition before retrying |
| `Export_File_Check` | ['tDie'] | Check Talend job execution logs for the triggering condition before retrying |
| `HH_Violation_Text_Load` | ['tDie'] | Check Talend job execution logs for the triggering condition before retrying |
| `Livevox_Daily_Load` | ['tWarn'] | Check Talend job execution logs for the triggering condition before retrying |
| `master_prediction_proposal_Load` | ['tDie', 'tWarn'] | Check Talend job execution logs for the triggering condition before retrying |
| `PatientInfo_Text_Load` | ['tDie', 'tWarn'] | Check Talend job execution logs for the triggering condition before retrying |

## Database connections needing configuration

- `TalendLog_0.1` — host/port/database blank in the repository entry; configure in Talend Studio before any dependent job can run against real data.
