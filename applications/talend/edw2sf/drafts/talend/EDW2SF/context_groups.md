# Context Groups — EDW2SF

## ContextManagement_DB_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| globalContext_DB_Port | id_String | `3306` | Port for connecting Database  |
| globalContext_DB__AdditionalParams | id_String | `` | String to specify any additional JDBC Connection parameters |
| globalContext_DB_Username | id_String | `` | Database username |
| globalContext_DB_Password | id_Password | `*(redacted)*` | Database Password |
| globalContext_DB_Host | id_String | `` | Database Hostname |
| globalContext_DB_Database_Schema | id_String | `` | Database schema |
| globalContext_DB_Port | id_String | `3306` | Port for connecting Database  |
| globalContext_DB__AdditionalParams | id_String | `` | String to specify any additional JDBC Connection parameters |
| globalContext_DB_Username | id_String | `root` | Database username |
| globalContext_DB_Password | id_Password | `*(redacted)*` | Database Password |
| globalContext_DB_Host | id_String | `dev` | Database Hostname |
| globalContext_DB_Database_Schema | id_String | `dev` | Database schema |
| globalContext_DB_Port | id_String | `3306` | Port for connecting Database  |
| globalContext_DB__AdditionalParams | id_String | `` | String to specify any additional JDBC Connection parameters |
| globalContext_DB_Username | id_String | `` | Database username |
| globalContext_DB_Password | id_Password | `*(redacted)*` | Database Password |
| globalContext_DB_Host | id_String | `` | Database Hostname |
| globalContext_DB_Database_Schema | id_String | `` | Database schema |

## ContextManagement_GlobalVariables_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| resource_directory_contextFiles | id_String | `/opt/talend/contextmanagement` | Location of Context Files (Local or Cloud Engine or Remote Engine) |
| contextStorageType | id_String | `"File"` | Context Storage Type to read from (File or DB). |
| environment | id_String | `` | Environment parameter that can be leveraged to drive different logic based on execution environment |
| enableProjectLevelContextFileLoad | id_Boolean | `false` | Load Project Level Context File |
| enableJobLevelContextFileLoad | id_Boolean | `false` | Load Job Level Context File |
| enableTaskLevelContextFileLoad | id_Boolean | `false` | Load Task Level Context File |
| taskName | id_String | `` | Task Name or Id for loading Context File |
| printContextVariableValues | id_Boolean | `false` | Print Context Variable Values (Password always hidden by default) |
| loadContextInJob | id_Boolean | `true` | Flag to set to load context variables in Job.  This is handy if there are child jobs and we do not want child jobs to load the context values again, but instead use the values from the parent job. Default Value is true and then overridden to false at the end of the first context load |
| temp_dir_path | id_String | `` | Allocate the directory path to hold temporary file for tMap disk mode |
| crytographic_PWD | id_Password | `*(redacted)*` | password for cryptographic file |
| crytographicFilePath | id_String | `"C:/Users/vmehra.TALEND/Documents/Project/MBO\MBO-DataPrivac` | file path for crytographic |
| resource_directory_contextFiles | id_String | `"C:/Temp/contextmanagement"` | Location of Context Files (Local or Cloud Engine or Remote Engine) |
| contextStorageType | id_String | `"File"` | Context Storage Type to read from (File or DB). |
| environment | id_String | `"dev"` | Environment parameter that can be leveraged to drive different logic based on execution environment |
| enableProjectLevelContextFileLoad | id_Boolean | `false` | Load Project Level Context File |
| enableJobLevelContextFileLoad | id_Boolean | `false` | Load Job Level Context File |
| enableTaskLevelContextFileLoad | id_Boolean | `false` | Load Task Level Context File |
| taskName | id_String | `` | Task Name or Id for loading Context File |
| printContextVariableValues | id_Boolean | `false` | Print Context Variable Values (Password always hidden by default) |
| loadContextInJob | id_Boolean | `true` | Flag to set to load context variables in Job.  This is handy if there are child jobs and we do not want child jobs to load the context values again, but instead use the values from the parent job. Default Value is true and then overridden to false at the end of the first context load |
| temp_dir_path | id_String | `"C:/Temp/"` | Allocate the directory path to hold temporary file for tMap disk mode |
| crytographic_PWD | id_Password | `*(redacted)*` | password for cryptographic file |
| crytographicFilePath | id_String | `"C:/Temp/password"` | file path for crytographic |
| resource_directory_contextFiles | id_String | `"C:/Temp/contextmanagement"` | Location of Context Files (Local or Cloud Engine or Remote Engine) |
| contextStorageType | id_String | `"File"` | Context Storage Type to read from (File or DB). |
| environment | id_String | `"test"` | Environment parameter that can be leveraged to drive different logic based on execution environment |
| enableProjectLevelContextFileLoad | id_Boolean | `false` | Load Project Level Context File |
| enableJobLevelContextFileLoad | id_Boolean | `false` | Load Job Level Context File |
| enableTaskLevelContextFileLoad | id_Boolean | `false` | Load Task Level Context File |
| taskName | id_String | `` | Task Name or Id for loading Context File |
| printContextVariableValues | id_Boolean | `true` | Print Context Variable Values (Password always hidden by default) |
| loadContextInJob | id_Boolean | `true` | Flag to set to load context variables in Job.  This is handy if there are child jobs and we do not want child jobs to load the context values again, but instead use the values from the parent job. Default Value is true and then overridden to false at the end of the first context load |
| temp_dir_path | id_String | `"C:/Temp/"` | Allocate the directory path to hold temporary file for tMap disk mode |
| crytographic_PWD | id_Password | `*(redacted)*` | password for cryptographic file |
| crytographicFilePath | id_String | `"C:/Temp/password"` | file path for crytographic |

## DEDOR_DW_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| DEDOR_DW_oauthProperties_clientId | id_String | `*(redacted)*` |  |
| DEDOR_DW_role | id_String | `DATALOADER` |  |
| DEDOR_DW_oauthProperties_scope | id_String | `*(redacted)*` |  |
| DEDOR_DW_db | id_String | `DEDOR` |  |
| DEDOR_DW_regionID | id_String | `` |  |
| DEDOR_DW_jdbcParameters | id_String | `` |  |
| DEDOR_DW_oauthProperties_oauthUserName | id_String | `*(redacted)*` |  |
| DEDOR_DW_oauthProperties_oauthPassword | id_Password | `*(redacted)*` |  |
| DEDOR_DW_oauthProperties_clientSecret | id_Password | `*(redacted)*` |  |
| DEDOR_DW_account | id_String | `ubb72400.us-east-1` |  |
| DEDOR_DW_userPassword_userId | id_String | `*(redacted)*` |  |
| DEDOR_DW_warehouse | id_String | `COMPUTE_WH` |  |
| DEDOR_DW_oauthProperties_oauthTokenEndpoint | id_String | `*(redacted)*` |  |
| DEDOR_DW_userPassword_password | id_Password | `*(redacted)*` |  |
| DEDOR_DW_schemaName | id_String | `DW` |  |
| DEDOR_DW_keyAlias | id_String | `` |  |
| DEDOR_DW_loginTimeout | id_Integer | `15` |  |

## EDWProdHH_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EDWProdHH_AdditionalParams | id_String | `` |  |
| EDWProdHH_Database | id_String | `EDWProdHH` |  |
| EDWProdHH_Login | id_String | `dwuser` |  |
| EDWProdHH_Server | id_String | `MP-BI-V01` |  |
| EDWProdHH_Schema | id_String | `dbo` |  |
| EDWProdHH_Port | id_String | `1433` |  |
| EDWProdHH_Password | id_Password | `*(redacted)*` |  |

## EXPORT_ACTIVITY_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_ACTIVITY_RowSeparator | id_String | `"\n"` |  |
| EXPORT_ACTIVITY_File | id_File | `Z:/EDW/2021-11-27/HH/HH-EDW-EXPORT-ACTIVITY.txt` |  |
| EXPORT_ACTIVITY_Header | id_Integer | `1` |  |
| EXPORT_ACTIVITY_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_ACTIVITY_Encoding | id_String | `US-ASCII` |  |

## EXPORT_CLIENT_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_CLIENT_RowSeparator | id_String | `"\n"` |  |
| EXPORT_CLIENT_File | id_File | `HH-EDW-EXPORT-CLIENT.txt` |  |
| EXPORT_CLIENT_Header | id_Integer | `1` |  |
| EXPORT_CLIENT_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_CLIENT_Encoding | id_String | `US-ASCII` |  |

## EXPORT_DEBTOR_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_DEBTOR_RowSeparator | id_String | `"\n"` |  |
| EXPORT_DEBTOR_File | id_File | `Z:/EDW/2021-11-27/HH/HH-EDW-EXPORT-DEBTOR1.txt` |  |
| EXPORT_DEBTOR_Header | id_Integer | `1` |  |
| EXPORT_DEBTOR_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_DEBTOR_Encoding | id_String | `US-ASCII` |  |

## EXPORT_DESKINFO_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_DESKINFO_RowSeparator | id_String | `"\n"` |  |
| EXPORT_DESKINFO_File | id_File | `Z:/EDW/2021-11-27/HH/HH-EDW-EXPORT-DESKINFO.txt` |  |
| EXPORT_DESKINFO_Header | id_Integer | `1` |  |
| EXPORT_DESKINFO_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_DESKINFO_Encoding | id_String | `US-ASCII` |  |

## EXPORT_EM_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_EM_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_EM_File | id_File | `Q:/HH-EDW-EXPORT-EM.txt` |  |
| EXPORT_EM_RowSeparator | id_String | `"\n"` |  |
| EXPORT_EM_Encoding | id_String | `US-ASCII` |  |
| EXPORT_EM_Header | id_Integer | `1` |  |

## EXPORT_EMAIL_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_EMAIL_RowSeparator | id_String | `"\n"` |  |
| EXPORT_EMAIL_File | id_File | `Z:/EDW/2021-11-27/HH/HH-EDW-EXPORT-EM.txt` |  |
| EXPORT_EMAIL_Header | id_Integer | `1` |  |
| EXPORT_EMAIL_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_EMAIL_Encoding | id_String | `US-ASCII` |  |

## EXPORT_EMPINFO_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_EMPINFO_RowSeparator | id_String | `"\n"` |  |
| EXPORT_EMPINFO_File | id_File | `Z:/EDW/2021-11-27/HH/HH-EDW-EXPORT-EMPINFO.txt` |  |
| EXPORT_EMPINFO_Header | id_Integer | `1` |  |
| EXPORT_EMPINFO_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_EMPINFO_Encoding | id_String | `US-ASCII` |  |

## EXPORT_TRANS_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| EXPORT_TRANS_RowSeparator | id_String | `"\n"` |  |
| EXPORT_TRANS_File | id_File | `Z:/EDW/2021-11-27/HH/HH-EDW-EXPORT-TRANS.txt` |  |
| EXPORT_TRANS_Header | id_Integer | `1` |  |
| EXPORT_TRANS_FieldSeparator | id_String | `"\t"` |  |
| EXPORT_TRANS_Encoding | id_String | `US-ASCII` |  |

## HOPE_Archive1_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| HOPE_archive1_DecimalSeparator | id_String | `'.'` |  |
| HOPE_archive1_Encoding | id_String | `UTF-8` |  |
| HOPE_archive1_File | id_File | `G:/Analytics_Team/HOPE HISTORICAL/FINAL COLLECTOR DETAIL APR` |  |
| HOPE_archive1_Header | id_Integer | `1` |  |
| HOPE_archive1_LastColumn | id_Integer | `12` |  |
| HOPE_archive1_FirstColumn | id_Integer | `1` |  |
| HOPE_archive1_ThousandSeparator | id_String | `','` |  |
| HOPE_archive1_FilePath | id_String | `/extracts` |  |

## HOPE_archive_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| HOPE_archive_File | id_File | `G:/Analytics_Team/HOPE HISTORICAL/FINAL COLLECTOR DETAIL APR` |  |
| HOPE_archive_Header | id_Integer | `1` |  |
| HOPE_archive_FirstColumn | id_Integer | `1` |  |

## I3_IC_40_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| I3_IC_40_Login | id_String | `svc_ssa_snflk` |  |
| I3_IC_40_Schema | id_String | `dbo` |  |
| I3_IC_40_Password | id_Password | `*(redacted)*` |  |
| I3_IC_40_Database | id_String | `I3_IC_40` |  |
| I3_IC_40_Server | id_String | `MP-ININSQL-V01` |  |
| I3_IC_40_Port | id_String | `1433` |  |
| I3_IC_40_AdditionalParams | id_String | `` |  |

## LEGACY_DW1_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| LEGACY_DW1_jdbcUrlSuffix | id_String | `.snowflakecomputing.com` |  |
| LEGACY_DW1_oauthProperties_oauthTokenEndpoint | id_String | `*(redacted)*` |  |
| LEGACY_DW1_jdbcParameters | id_String | `` |  |
| LEGACY_DW1_userPassword_userId | id_String | `*(redacted)*` |  |
| LEGACY_DW1_account | id_String | `xca26579.us-east-1` |  |
| LEGACY_DW1_userPassword_password | id_Password | `*(redacted)*` |  |
| LEGACY_DW1_warehouse | id_String | `COMPUTE_WH` |  |
| LEGACY_DW1_oauthProperties_clientId | id_String | `*(redacted)*` |  |
| LEGACY_DW1_oauthProperties_oauthUserName | id_String | `*(redacted)*` |  |
| LEGACY_DW1_schemaName | id_String | `DW` |  |
| LEGACY_DW1_oauthProperties_clientSecret | id_Password | `*(redacted)*` |  |
| LEGACY_DW1_role | id_String | `` |  |
| LEGACY_DW1_regionID | id_String | `` |  |
| LEGACY_DW1_oauthProperties_scope | id_String | `*(redacted)*` |  |
| LEGACY_DW1_db | id_String | `EDWPRODHH` |  |
| LEGACY_DW1_loginTimeout | id_Integer | `15` |  |
| LEGACY_DW1_oauthProperties_oauthPassword | id_Password | `*(redacted)*` |  |
| LEGACY_DW1_keyAlias | id_String | `snowflake` |  |

## LEGACY_DW_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| LEGACY_DW_role | id_String | `` |  |
| LEGACY_DW_userPassword_password | id_Password | `*(redacted)*` |  |
| LEGACY_DW_jdbcParameters | id_String | `` |  |
| LEGACY_DW_regionID | id_String | `` |  |
| LEGACY_DW_oauthProperties_clientSecret | id_Password | `*(redacted)*` |  |
| LEGACY_DW_account | id_String | `xca26579.us-east-1` |  |
| LEGACY_DW_oauthProperties_clientId | id_String | `*(redacted)*` |  |
| LEGACY_DW_schemaName | id_String | `DW` |  |
| LEGACY_DW_oauthProperties_oauthTokenEndpoint | id_String | `*(redacted)*` |  |
| LEGACY_DW_userPassword_userId | id_String | `*(redacted)*` |  |
| LEGACY_DW_oauthProperties_oauthUserName | id_String | `*(redacted)*` |  |
| LEGACY_DW_oauthProperties_scope | id_String | `*(redacted)*` |  |
| LEGACY_DW_warehouse | id_String | `COMPUTE_WH` |  |
| LEGACY_DW_keyAlias | id_String | `snowflake` |  |
| LEGACY_DW_db | id_String | `EDWPRODHH` |  |
| LEGACY_DW_oauthProperties_oauthPassword | id_Password | `*(redacted)*` |  |
| LEGACY_DW_loginTimeout | id_Integer | `15` |  |

## LEGACY_STAGING_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| LEGACY_STAGING_regionID | id_String | `` |  |
| LEGACY_STAGING_account | id_String | `xca26579.us-east-1` |  |
| LEGACY_STAGING_userPassword_password | id_Password | `*(redacted)*` |  |
| LEGACY_STAGING_oauthProperties_clientSecret | id_Password | `*(redacted)*` |  |
| LEGACY_STAGING_schemaName | id_String | `STAGING` |  |
| LEGACY_STAGING_keyAlias | id_String | `snowflake` |  |
| LEGACY_STAGING_oauthProperties_oauthTokenEndpoint | id_String | `*(redacted)*` |  |
| LEGACY_STAGING_db | id_String | `EDWPRODHH` |  |
| LEGACY_STAGING_oauthProperties_scope | id_String | `*(redacted)*` |  |
| LEGACY_STAGING_role | id_String | `DATALOADER` |  |
| LEGACY_STAGING_jdbcUrlSuffix | id_String | `.snowflakecomputing.com` |  |
| LEGACY_STAGING_oauthProperties_oauthUserName | id_String | `*(redacted)*` |  |
| LEGACY_STAGING_oauthProperties_oauthPassword | id_Password | `*(redacted)*` |  |
| LEGACY_STAGING_warehouse | id_String | `COMPUTE_WH` |  |
| LEGACY_STAGING_userPassword_userId | id_String | `*(redacted)*` |  |
| LEGACY_STAGING_loginTimeout | id_Integer | `15` |  |
| LEGACY_STAGING_jdbcParameters | id_String | `CLIENT_SESSION_KEEP_ALIVE=true` |  |
| LEGACY_STAGING_oauthProperties_clientId | id_String | `*(redacted)*` |  |

## PAYPLAN_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| PAYPLAN_FieldSeparator | id_String | `"\t"` |  |
| PAYPLAN_Encoding | id_String | `US-ASCII` |  |
| PAYPLAN_File | id_File | `Q:/HH_PAYPLAN.TXT` |  |
| PAYPLAN_Header | id_Integer | `1` |  |
| PAYPLAN_RowSeparator | id_String | `"\n"` |  |

## POSTDATE_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| POSTDATE_Header | id_Integer | `1` |  |
| POSTDATE_File | id_File | `X:/CHI_POSTDATE.TXT` |  |
| POSTDATE_RowSeparator | id_String | `"\n"` |  |
| POSTDATE_FieldSeparator | id_String | `"\t"` |  |
| POSTDATE_Encoding | id_String | `US-ASCII` |  |

## PUB_JCHANG_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| PUB_JCHANG_oauthProperties_oauthPassword | id_Password | `*(redacted)*` |  |
| PUB_JCHANG_oauthProperties_scope | id_String | `*(redacted)*` |  |
| PUB_JCHANG_oauthProperties_clientId | id_String | `*(redacted)*` |  |
| PUB_JCHANG_role | id_String | `` |  |
| PUB_JCHANG_regionID | id_String | `` |  |
| PUB_JCHANG_account | id_String | `xca26579.us-east-1` |  |
| PUB_JCHANG_db | id_String | `EDWPROD_HH` |  |
| PUB_JCHANG_schemaName | id_String | `PUB_JCHANG` |  |
| PUB_JCHANG_warehouse | id_String | `COMPUTE_WH` |  |
| PUB_JCHANG_oauthProperties_oauthUserName | id_String | `*(redacted)*` |  |
| PUB_JCHANG_jdbcParameters | id_String | `` |  |
| PUB_JCHANG_loginTimeout | id_Integer | `15` |  |
| PUB_JCHANG_keyAlias | id_String | `` |  |
| PUB_JCHANG_userPassword_userId | id_String | `*(redacted)*` |  |
| PUB_JCHANG_userPassword_password | id_Password | `*(redacted)*` |  |
| PUB_JCHANG_oauthProperties_clientSecret | id_Password | `*(redacted)*` |  |
| PUB_JCHANG_oauthProperties_oauthTokenEndpoint | id_String | `*(redacted)*` |  |

## StandardFolders_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| archiveDir | id_String | `/archive/` |  |
| logDir | id_String | `/logs/` |  |
| sourceDir | id_String | `/mnt/cubs/` |  |
| sourceDCDir | id_String | `/mnt/cubs_dc/` |  |
| keystorePath | id_String | `/etc/keys/keystore.p12` |  |
| archiveDir | id_String | `C:/Data/` |  |
| logDir | id_String | `C:/Data/` |  |
| sourceDir | id_String | `X:/` |  |
| sourceDCDir | id_String | `W:/` |  |
| keystorePath | id_String | `C:/users/jmach/.ssl/keystore.p12` |  |

## TableauVariables_0.1

| Variable | Type | Value | Comment |
|----------|------|-------|---------|
| pyScriptDir | id_String | `/scripts/` |  |
| tabServer | id_String | `http://mp-tab-v01` |  |
| tabUser | id_String | `svc_tableau` |  |
| tabPass | id_String | `*(redacted)*` |  |
| tabFile | id_String | `/output/Letter_Extract_SF.hyper` |  |
| tabName | id_String | `LETTERS_EXTRACT_SF` |  |
| tabProject | id_String | `15a5f1f8-63b0-4dc2-bfde-8ab27644d28b` |  |
| pyCmd | id_String | `` |  |
