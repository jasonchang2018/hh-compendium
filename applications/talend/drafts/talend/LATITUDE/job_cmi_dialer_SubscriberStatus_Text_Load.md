# Talend Job: cmi_dialer_SubscriberStatus_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2024-11-06T09:59:10.313-0800
- **Last Modified**: 2026-07-12T13:56:39.605-0700

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tDBConnection_1 | `tSnowflakeConnection` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":2,"@type":"org.talend.components.snowflake. |
| 2 | tFileList_1 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 3 | tJava_1 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 4 | tFileInputDelimited_1 | `tFileInputDelimited` | `USE_EXISTING_DYNAMIC`=false, `FILENAMETEXT`="When the input source is a stream or a zip file,f, `FILENAME`=context.filePath, `CSV_OPTION`=false, `ROWSEPARATOR`="|$|" |
| 5 | tMap_1 | `tMap` | `LINK_STYLE`=AUTO, `DIE_ON_ERROR`=true, `LKUP_PARALLELIZE`=false, `LEVENSHTEIN`=0, `JACCARD`=0 |
| 6 | tDBOutput_1 | `tSnowflakeOutput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":4,"@type":"org.talend.components.snowflake. |
| 7 | tDBRow_1 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 8 | tDBRow_2 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 9 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 10 | tJava_2 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 11 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 12 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 13 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 14 | tJava_3 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 15 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=true, `FOLDER`=false |
| 16 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 17 | tJava_4 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 18 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| SubscriberStatusID | id_Integer | Yes | -1 |
| PhoneNumber | id_String | Yes | -1 |
| OptedIn | id_Integer | Yes | -1 |
| OptInPending | id_Integer | Yes | -1 |
| CanAutoOptIn | id_Integer | Yes | -1 |
| OptInDelivered | id_Integer | Yes | -1 |
| OptOutOverride | id_Integer | Yes | -1 |
| CompanyCode | id_String | Yes | -1 |
| SubscriberStatusID | id_Integer | Yes | -1 |
| PhoneNumber | id_String | Yes | -1 |
| OptedIn | id_Integer | Yes | -1 |
| OptInPending | id_Integer | Yes | -1 |
| CanAutoOptIn | id_Integer | Yes | -1 |
| OptInDelivered | id_Integer | Yes | -1 |
| OptOutOverride | id_Integer | Yes | -1 |
| CompanyCode | id_String | Yes | -1 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| SUBSCRIBERSTATUSID | id_Integer | No | -1 |
| PHONENUMBER | id_String | No | -1 |
| OPTEDIN | id_Integer | No | -1 |
| OPTINPENDING | id_Integer | No | -1 |
| CANAUTOOPTIN | id_Integer | No | -1 |
| OPTINDELIVERED | id_Integer | Yes | -1 |
| OPTOUTOVERRIDE | id_Integer | Yes | -1 |
| COMPANYCODE | id_String | Yes | -1 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| SUBSCRIBERSTATUSID | id_Integer | No | -1 |
| PHONENUMBER | id_String | No | -1 |
| OPTEDIN | id_Integer | No | -1 |
| OPTINPENDING | id_Integer | No | -1 |
| CANAUTOOPTIN | id_Integer | No | -1 |
| OPTINDELIVERED | id_Integer | Yes | -1 |
| OPTOUTOVERRIDE | id_Integer | Yes | -1 |
| COMPANYCODE | id_String | Yes | -1 |
| columnName | id_String | No | 255 |
| rowNumber | id_String | No | 255 |
| category | id_String | No | 255 |
| character | id_String | No | 255 |
| errorMessage | id_String | No | 255 |
| byteOffset | id_String | No | 255 |
| line | id_String | No | 255 |
| sqlState | id_String | No | 255 |
| code | id_String | No | 255 |

### tDBRow_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

### tDBRow_2

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

## Data Flow

```mermaid
graph LR
    tFileList_1 -->|ITERATE| tJava_1
    tFileList_1 -->|SUBJOB_OK| tParallelize_1
    tJava_1 -->|ITERATE| tFileInputDelimited_1
    tFileInputDelimited_1 -->|FLOW| tMap_1
    tMap_1 -->|FLOW| tDBOutput_1
    tDBRow_1 -->|SUBJOB_OK| tFileList_1
    tFileList_2 -->|ITERATE| tJava_2
    tFileList_2 -->|SUBJOB_OK| tFileList_3
    tJava_2 -->|ITERATE| tFileArchive_1
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tParallelize_1 -->|PARALLELIZE| tFileList_2
    tFileList_3 -->|ITERATE| tJava_3
    tJava_3 -->|ITERATE| tFileDelete_1
    tPrejob_1 -->|COMPONENT_OK| tJava_4
    tJava_4 -->|SUBJOB_OK| tSetKeystore_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
