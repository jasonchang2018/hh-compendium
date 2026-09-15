# Talend Job: cmi_Hermes_Recommendations_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2026-03-04T10:25:20.254-0800
- **Last Modified**: 2026-03-04T16:11:38.780-0800

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 2 | tJava_1 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 3 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |
| 4 | tDBConnection_1 | `tSnowflakeConnection` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":2,"@type":"org.talend.components.snowflake. |
| 5 | tDBRow_1 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 6 | tFileList_1 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 7 | tJava_2 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 8 | tFileInputDelimited_1 | `tFileInputDelimited` | `USE_EXISTING_DYNAMIC`=false, `FILENAMETEXT`="When the input source is a stream or a zip file,f, `FILENAME`=context.filePath, `CSV_OPTION`=false, `ROWSEPARATOR`="|$|" |
| 9 | tMap_1 | `tMap` | `LINK_STYLE`=AUTO, `DIE_ON_ERROR`=true, `LKUP_PARALLELIZE`=false, `LEVENSHTEIN`=0, `JACCARD`=0 |
| 10 | tFlowMeter_2 | `tFlowMeter` | `USEROWLABEL`=true, `METTERLABEL`="MyLabel", `ABSOLUTE`=Absolute, `CONNECTION_FORMAT`=row |
| 11 | tDBOutput_1 | `tSnowflakeOutput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 12 | tDBRow_2 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 13 | tJavaRow_1 | `tJavaRow` | `CODE`=context.retValue = row3.RETVALUE;, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 14 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 15 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 16 | tJava_3 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 17 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=true, `FOLDER`=false |
| 18 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 19 | tJava_4 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 20 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 21 | tDie_1 | `tDie` | `MESSAGE`="MERGE failed - error code " + context.retValue.to, `CODE`=4, `PRIORITY`=5, `EXIT_JVM`=false, `CONNECTION_FORMAT`=row |
| 22 | tWarn_1 | `tWarn` | `MESSAGE`=context.retValue.toString() + " rows inserted or u, `CODE`=42, `PRIORITY`=4, `CONNECTION_FORMAT`=row |

## Schemas

### tDBRow_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| Id | id_BigDecimal | Yes | -1 |
| NUMBER | id_BigDecimal | Yes | -1 |
| PROPOSED_CHANNEL | id_String | Yes | -1 |
| phonenumber | id_String | Yes | -1 |
| hermes_request_id | id_String | Yes | -1 |
| CreatedWhenUTC | id_String | Yes | -1 |
| UpdatedWhenUTC | id_String | Yes | -1 |
| ProcessOutcome | id_String | Yes | -1 |
| Comments | id_String | Yes | -1 |
| Id | id_BigDecimal | Yes | -1 |
| NUMBER | id_BigDecimal | Yes | -1 |
| PROPOSED_CHANNEL | id_String | Yes | -1 |
| phonenumber | id_String | Yes | -1 |
| hermes_request_id | id_String | Yes | -1 |
| CreatedWhenUTC | id_String | Yes | -1 |
| UpdatedWhenUTC | id_String | Yes | -1 |
| ProcessOutcome | id_String | Yes | -1 |
| Comments | id_String | Yes | -1 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_BigDecimal | No | 38 |
| NUMBER | id_BigDecimal | Yes | 38 |
| PROPOSED_CHANNEL | id_String | Yes | 50 |
| PHONENUMBER | id_String | Yes | 20 |
| HERMES_REQUEST_ID | id_String | Yes | 50 |
| CREATEDWHEN_UTC | id_String | Yes | 50 |
| UPDATEDWHEN_UTC | id_String | Yes | 50 |
| PROCESS_OUTCOME | id_String | Yes | 50 |
| COMMENTS | id_String | Yes | 16777216 |

### tFlowMeter_2

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_BigDecimal | No | 38 |
| NUMBER | id_BigDecimal | Yes | 38 |
| PROPOSED_CHANNEL | id_String | Yes | 50 |
| PHONENUMBER | id_String | Yes | 20 |
| HERMES_REQUEST_ID | id_String | Yes | 50 |
| CREATEDWHEN_UTC | id_String | Yes | 50 |
| UPDATEDWHEN_UTC | id_String | Yes | 50 |
| PROCESS_OUTCOME | id_String | Yes | 50 |
| COMMENTS | id_String | Yes | 16777216 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_BigDecimal | No | 38 |
| NUMBER | id_BigDecimal | Yes | 38 |
| PROPOSED_CHANNEL | id_String | Yes | 50 |
| PHONENUMBER | id_String | Yes | 20 |
| HERMES_REQUEST_ID | id_String | Yes | 50 |
| CREATEDWHEN_UTC | id_String | Yes | 50 |
| UPDATEDWHEN_UTC | id_String | Yes | 50 |
| PROCESS_OUTCOME | id_String | Yes | 50 |
| COMMENTS | id_String | Yes | 16777216 |
| columnName | id_String | No | 255 |
| rowNumber | id_String | No | 255 |
| category | id_String | No | 255 |
| character | id_String | No | 255 |
| errorMessage | id_String | No | 255 |
| byteOffset | id_String | No | 255 |
| line | id_String | No | 255 |
| sqlState | id_String | No | 255 |
| code | id_String | No | 255 |

### tDBRow_2

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| RETVALUE | id_Long | Yes | -1 |
| RETVALUE | id_Long | Yes | -1 |
| RETVALUE | id_Long | Yes | -1 |
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

## Data Flow

```mermaid
graph LR
    tPrejob_1 -->|COMPONENT_OK| tJava_1
    tJava_1 -->|SUBJOB_OK| tSetKeystore_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
    tDBRow_1 -->|SUBJOB_OK| tFileList_1
    tFileList_1 -->|ITERATE| tJava_2
    tFileList_1 -->|SUBJOB_OK| tParallelize_1
    tJava_2 -->|ITERATE| tFileInputDelimited_1
    tFileInputDelimited_1 -->|FLOW| tMap_1
    tMap_1 -->|FLOW| tFlowMeter_2
    tFlowMeter_2 -->|FLOW| tDBOutput_1
    tDBRow_2 -->|MAIN| tJavaRow_1
    tJavaRow_1 -->|RUN_IF| tDie_1
    tJavaRow_1 -->|RUN_IF| tWarn_1
    tParallelize_1 -->|PARALLELIZE| tFileList_3
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tFileList_2 -->|ITERATE| tJava_3
    tJava_3 -->|ITERATE| tFileDelete_1
    tFileList_3 -->|ITERATE| tJava_4
    tFileList_3 -->|SUBJOB_OK| tFileList_2
    tJava_4 -->|ITERATE| tFileArchive_1
```
