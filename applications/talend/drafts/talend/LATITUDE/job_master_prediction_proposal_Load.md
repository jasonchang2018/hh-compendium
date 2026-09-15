# Talend Job: master_prediction_proposal_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2026-03-11T14:43:22.039-0700
- **Last Modified**: 2026-03-12T19:47:23.647-0700

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 2 | tJava_1 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 3 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |
| 4 | tDBConnection_1 | `tSnowflakeConnection` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":2,"@type":"org.talend.components.snowflake. |
| 5 | tWarn_1 | `tWarn` | `MESSAGE`=context.retValue.toString() + " rows inserted or u, `CODE`=42, `PRIORITY`=4, `CONNECTION_FORMAT`=row |
| 6 | tDBRow_1 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 7 | tJavaRow_1 | `tJavaRow` | `CODE`=context.retValue = row1.RETVALUE;, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 8 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 9 | tFileList_1 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 10 | tJava_2 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 11 | tFileInputDelimited_1 | `tFileInputDelimited` | `COMPONENT_NAME`=tFileInputDelimited, `VERSION`=0.102 (ALPHA), `FAMILY`=File/Input, `START`=false, `STARTABLE`=true |
| 12 | tMap_1 | `tMap` | `LINK_STYLE`=AUTO, `DIE_ON_ERROR`=true, `LKUP_PARALLELIZE`=false, `LEVENSHTEIN`=0, `JACCARD`=0 |
| 13 | tFlowMeter_2 | `tFlowMeter` | `USEROWLABEL`=true, `METTERLABEL`="MyLabel", `ABSOLUTE`=Absolute, `CONNECTION_FORMAT`=row |
| 14 | tDBOutput_1 | `tSnowflakeOutput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":4,"@type":"org.talend.components.snowflake. |
| 15 | tDBRow_2 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 16 | tDie_1 | `tDie` | `MESSAGE`="MERGE failed - error code " + context.retValue.to, `CODE`=4, `PRIORITY`=5, `EXIT_JVM`=false, `CONNECTION_FORMAT`=row |
| 17 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 18 | tJava_3 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 19 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=true, `FOLDER`=false |
| 20 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 21 | tJava_4 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 22 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |

## Schemas

### tDBRow_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| RETVALUE | id_Long | Yes | -1 |
| RETVALUE | id_Long | Yes | -1 |
| RETVALUE | id_Long | Yes | -1 |
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| NUMBER | id_BigDecimal | Yes | -1 |
| PROPOSED_CHANNEL | id_String | Yes | -1 |
| TEMPLATE | id_String | Yes | -1 |
| PHONE_NUMBER | id_String | Yes | -1 |
| SUBTEAM | id_String | Yes | -1 |
| TEXT_TYPE | id_String | Yes | -1 |
| SETTLEMENT_AMT | id_String | Yes | -1 |
| VOAPPS_TARGET_DATE | id_String | Yes | -1 |
| VOAPPS_CALLER_NUMBER | id_String | Yes | -1 |
| VOAPPS_MESSAGE_ID | id_String | Yes | -1 |
| VOAPPS_ZIP_CODE | id_String | Yes | -1 |
| VOAPPS_VOICE_APPEND | id_String | Yes | -1 |
| HERMES_REQUEST_ID | id_String | Yes | -1 |
| NUMBER | id_BigDecimal | Yes | -1 |
| PROPOSED_CHANNEL | id_String | Yes | -1 |
| TEMPLATE | id_String | Yes | -1 |
| PHONE_NUMBER | id_String | Yes | -1 |
| SUBTEAM | id_String | Yes | -1 |
| TEXT_TYPE | id_String | Yes | -1 |
| SETTLEMENT_AMT | id_String | Yes | -1 |
| VOAPPS_TARGET_DATE | id_String | Yes | -1 |
| VOAPPS_CALLER_NUMBER | id_String | Yes | -1 |
| VOAPPS_MESSAGE_ID | id_String | Yes | -1 |
| VOAPPS_ZIP_CODE | id_String | Yes | -1 |
| VOAPPS_VOICE_APPEND | id_String | Yes | -1 |
| HERMES_REQUEST_ID | id_String | Yes | -1 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| NUMBER | id_BigDecimal | Yes | 38 |
| PROPOSED_CHANNEL | id_String | Yes | 16777216 |
| TEMPLATE | id_String | Yes | 16777216 |
| PHONE_NUMBER | id_String | Yes | 16777216 |
| SUBTEAM | id_String | Yes | 16777216 |
| TEXT_TYPE | id_String | Yes | 16777216 |
| SETTLEMENT_AMT | id_String | Yes | 16777216 |
| VOAPPS_TARGET_DATE | id_String | Yes | 16777216 |
| VOAPPS_CALLER_NUMBER | id_String | Yes | 16777216 |
| VOAPPS_MESSAGE_ID | id_String | Yes | 16777216 |
| VOAPPS_ZIP_CODE | id_String | Yes | 16777216 |
| VOAPPS_VOICE_APPEND | id_String | Yes | 16777216 |
| HERMES_REQUEST_ID | id_String | Yes | 16777216 |

### tFlowMeter_2

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| NUMBER | id_BigDecimal | Yes | 38 |
| PROPOSED_CHANNEL | id_String | Yes | 16777216 |
| TEMPLATE | id_String | Yes | 16777216 |
| PHONE_NUMBER | id_String | Yes | 16777216 |
| SUBTEAM | id_String | Yes | 16777216 |
| TEXT_TYPE | id_String | Yes | 16777216 |
| SETTLEMENT_AMT | id_String | Yes | 16777216 |
| VOAPPS_TARGET_DATE | id_String | Yes | 16777216 |
| VOAPPS_CALLER_NUMBER | id_String | Yes | 16777216 |
| VOAPPS_MESSAGE_ID | id_String | Yes | 16777216 |
| VOAPPS_ZIP_CODE | id_String | Yes | 16777216 |
| VOAPPS_VOICE_APPEND | id_String | Yes | 16777216 |
| HERMES_REQUEST_ID | id_String | Yes | 16777216 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| NUMBER | id_BigDecimal | Yes | 38 |
| PROPOSED_CHANNEL | id_String | Yes | 16777216 |
| TEMPLATE | id_String | Yes | 16777216 |
| PHONE_NUMBER | id_String | Yes | 16777216 |
| SUBTEAM | id_String | Yes | 16777216 |
| TEXT_TYPE | id_String | Yes | 16777216 |
| SETTLEMENT_AMT | id_String | Yes | 16777216 |
| VOAPPS_TARGET_DATE | id_String | Yes | 16777216 |
| VOAPPS_CALLER_NUMBER | id_String | Yes | 16777216 |
| VOAPPPS_MESSAGE_ID | id_String | Yes | 16777216 |
| VOAPPS_ZIP_CODE | id_String | Yes | 16777216 |
| VOAPPS_VOICE_APPEND | id_String | Yes | 16777216 |
| HERMES_REQUEST_ID | id_String | Yes | 16777216 |
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
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

## Data Flow

```mermaid
graph LR
    tPrejob_1 -->|COMPONENT_OK| tJava_1
    tJava_1 -->|SUBJOB_OK| tSetKeystore_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
    tDBRow_1 -->|MAIN| tJavaRow_1
    tJavaRow_1 -->|RUN_IF| tDie_1
    tJavaRow_1 -->|RUN_IF| tWarn_1
    tParallelize_1 -->|PARALLELIZE| tFileList_3
    tParallelize_1 -->|PARALLELIZE| tDBRow_1
    tFileList_1 -->|ITERATE| tJava_2
    tFileList_1 -->|SUBJOB_OK| tParallelize_1
    tJava_2 -->|ITERATE| tFileInputDelimited_1
    tFileInputDelimited_1 -->|FLOW| tMap_1
    tMap_1 -->|FLOW| tFlowMeter_2
    tFlowMeter_2 -->|FLOW| tDBOutput_1
    tDBRow_2 -->|SUBJOB_OK| tFileList_1
    tFileList_2 -->|ITERATE| tJava_3
    tJava_3 -->|ITERATE| tFileDelete_1
    tFileList_3 -->|ITERATE| tJava_4
    tFileList_3 -->|SUBJOB_OK| tFileList_2
    tJava_4 -->|ITERATE| tFileArchive_1
```
