# Dependency Matrix — EDW2SF Project

## Overview

This matrix shows what each job depends on to run: which logical connection (see `01_system_architecture.md` for why the 9 repository connection entries themselves are blank), which context group, and — new for this project — which other jobs it triggers or is triggered by. Read the Notes section before assuming any shared piece here is safe to change without telling the whole team.

## Jobs → connection label

| Connection label | Type | Job count |
|---|---|---|
| `LEGACY_STAGING` | Snowflake | 100 |
| `SF_CXN` | Snowflake | 44 |
| `LEGACY_DW` | Snowflake | 38 |
| `MSSQL_CXN` | MSSQL | 30 |
| `SF_PUB_LW` | Snowflake | 21 |
| `EDWProdHH` | MSSQL | 12 |
| `I3_Dialer_40` | MSSQL | 7 |
| `HERMES` | Snowflake | 7 |
| `HUB` | MSSQL | 6 |
| `LEGACY_HUB` | Snowflake | 6 |
| `I3_IC_40` | MSSQL | 6 |
| `PUB_JCHANG` | Snowflake | 5 |
| `HOPE` | MySQL | 4 |
| `LEGACY_HOPE` | Snowflake | 3 |
| `LEGACY_DM` | Snowflake | 3 |
| `DIALER_I3` | Snowflake | 2 |
| `SnowflakeJDBC` | JDBC | 1 |
| `SF_STG_CXN` | Snowflake | 1 |
| `DEDOR_DW` | Snowflake | 1 |
| `SF_Equabli` | Snowflake | 1 |
| `SF_Equabli_2` | Snowflake | 1 |
| `SF_DW` | Snowflake | 1 |
| `DW` | Snowflake | 1 |

None of the 9 repository connection *entries* (`EDWProdHH_0.1`, `EDWStage_0.1`, `HOPE_0.1`, `HUB_0.1`, `I3_Dialer_40_0.1`, `I3_GBHQ_0.1`, `I3_IC_40_0.1`, `SnowflakeJDBC_0.1`, `TalendLog_0.1`) have host/port/database populated — every job instead uses one of the hand-labeled connection components above, whose real settings live in a same- or similarly-named context group.

## Jobs → context group

| Context group | Jobs referencing it (by variable name) |
|---|---|
| `StandardFolders_0.1` | 176 |
| `LEGACY_STAGING_0.1` | 129 |
| `LEGACY_DW1_0.1` | 107 |
| `LEGACY_DW_0.1` | 105 |
| `EDWProdHH_0.1` | 47 |
| `EXPORT_DEBTOR_0.1` | 14 |
| `EXPORT_TRANS_0.1` | 14 |
| `I3_IC_40_0.1` | 10 |
| `EXPORT_CLIENT_0.1` | 7 |
| `TableauVariables_0.1` | 3 |
| `ContextManagement_GlobalVariables_0.1` | 1 |
| `DEDOR_DW_0.1` | 1 |
| `EXPORT_EM_0.1` | 1 |
| `EXPORT_EMPINFO_0.1` | 1 |
| `HOPE_Archive1_0.1` | 1 |
| `PAYPLAN_0.1` | 1 |
| `POSTDATE_0.1` | 1 |

`StandardFolders_0.1` (176 jobs) holds shared source/archive/log-folder paths used across most jobs regardless of what they load. `LEGACY_STAGING_0.1`, `LEGACY_DW1_0.1`, `LEGACY_DW_0.1`, and `EDWProdHH_0.1` are the next most widely used — the actual Snowflake/MSSQL credentials behind the connection labels in the table above.

## Jobs → jobs (`tRunJob` orchestration)

65 `tRunJob` links exist across 14 calling jobs (all resolve to a job inside this project — none point outside it). Full list:

| Calling job | Target job | Times called |
|---|---|---|
| `CO_Master_Load` | `CUBS_Raw_CO_Client_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_CO_Debtor_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_CO_ETL_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_Cellphone_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_DeskInfo_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_EM_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_Empinfo_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_Letter_Load` | 1 |
| `CO_Master_Load` | `CUBS_Raw_Trans_Load` | 1 |
| `CO_Master_Load` | `DimFiscal_CO_Load` | 1 |
| `CUBS_PostDates_Load` | `CUBS_Raw_PostDate_Load` | 5 |
| `CUBS_Raw_Debtor_Load` | `CUBS_Raw_CHI_Debtor_Load` | 1 |
| `CUBS_Raw_Debtor_Load` | `CUBS_Raw_CO_Debtor_Load` | 1 |
| `CUBS_Raw_Debtor_Load` | `CUBS_Raw_DC_Debtor_Load` | 1 |
| `CUBS_Raw_Debtor_Load` | `CUBS_Raw_HH_Debtor_Load` | 1 |
| `CUBS_Raw_Debtor_Load` | `CUBS_Raw_PRE_Debtor_Load` | 1 |
| `CUBS_Raw_Debtor_Load_Test` | `CUBS_Raw_DC_Debtor_Load_No_Delete` | 1 |
| `CUBS_Raw_ETL_Load` | `CUBS_Raw_CHI_ETL_Load` | 1 |
| `CUBS_Raw_ETL_Load` | `CUBS_Raw_CO_ETL_Load` | 1 |
| `CUBS_Raw_ETL_Load` | `CUBS_Raw_DC_ETL_Load` | 1 |
| `CUBS_Raw_ETL_Load` | `CUBS_Raw_HH_ETL_Load` | 1 |
| `CUBS_Raw_ETL_Load` | `CUBS_Raw_PRE_ETL_Load` | 1 |
| `CUBS_Raw_ETL_Load` | `CUBS_Raw_TOL_ETL_Load` | 1 |
| `DimCellphone_Load` | `CUBS_Raw_Cellphone_Load` | 6 |
| `DimDeskInfo_Load` | `CUBS_Raw_File_Load` | 1 |
| `DimEmployeeInfo_Load` | `CUBS_Raw_File_Load` | 1 |
| `EMail_Address_Load` | `CUBS_Raw_EMail_Address_Load` | 6 |
| `Export_Hermes_APC_Master_Prediction` | `master_prediction_proposal_cubs_extract` | 5 |
| `Extract_Hermes_Master_Prediction` | `master_prediction_proposal_cubs_extract` | 5 |
| `Fact_Electronic_Media_Load` | `CUBS_Raw_File_Load` | 1 |
| `HealthPartners_Close_Rpt_Master` | `HealthPartners_Close_Reports_Extract` | 12 |
| `PaymentPlan_Load` | `CUBS_Raw_File_Load` | 1 |

## Notes — what looks risky here

- **`StandardFolders_0.1` is a single point of failure for the majority of the platform** — 176 of 289 jobs depend on it for where they read/write files.
- **All 9 repository connection entries are unconfigured placeholders**. Whether these are meant to be filled in eventually, or are simply vestigial now that every job uses a hand-labeled component instead, is unable to determine from metadata — worth a cleanup conversation.
- **`SF_Equabli`, `SF_Equabli_2`, and `PUB_JCHANG` look individually owned** (one external partner name, one person's initials) rather than shared platform infrastructure. If the underlying person or relationship changes, whatever jobs use those connections could silently break with no one else aware they existed.
- **Only one site (`CO`) has a dedicated `_Master_Load` orchestrator** even though the same per-site job pattern (`CUBS_Raw_<Site>_Debtor_Load`, `_Client_Load`, `_ETL_Load`, etc.) repeats for CHI, DC, HH, PRE, and TOL. If those sites are triggered some other way (individually scheduled, or by a Master job not present in this export), that's undocumented here — verify with team so no site's pipeline is accidentally assumed to not exist.
- **`CO_Master_Load` failing gives the least specific signal of any job** — as an orchestrator of 10 sub-jobs, its own error doesn't say which sub-job actually broke (see `05_operational_runbook.md`).
- **`HealthPartners_Close_Rpt_Master` calls the same job 12 times** and `Export_Hermes_APC_Master_Prediction`/`Extract_Hermes_Master_Prediction` each call `master_prediction_proposal_cubs_extract` 5 times — almost certainly once per site/partner context, but confirming exactly what differs per call requires opening each `tRunJob` component's context settings individually; this summary can't distinguish the calls from metadata alone.

