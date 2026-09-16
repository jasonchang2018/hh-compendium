# Talend Job: cmi_CustomerGrouping_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2024-12-03T12:31:21.830-0800
- **Last Modified**: 2026-06-22T09:55:45.657-0700

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tDBConnection_1 | `tSnowflakeConnection` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":2,"@type":"org.talend.components.snowflake. |
| 2 | tFileList_1 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 3 | tJava_1 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 4 | tFileInputDelimited_1 | `tFileInputDelimited` | `USE_EXISTING_DYNAMIC`=false, `FILENAMETEXT`="When the input source is a stream or a zip file,f, `FILENAME`=context.filePath, `CSV_OPTION`=false, `ROWSEPARATOR`="|$|" |
| 5 | tMap_1 | `tMap` | `LINK_STYLE`=AUTO, `DIE_ON_ERROR`=true, `LKUP_PARALLELIZE`=false, `LEVENSHTEIN`=0, `JACCARD`=0 |
| 6 | tFlowMeter_3 | `tFlowMeter` | `USEROWLABEL`=true, `METTERLABEL`="MyLabel", `ABSOLUTE`=Absolute, `CONNECTION_FORMAT`=row |
| 7 | tDBOutput_1 | `tSnowflakeOutput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":4,"@type":"org.talend.components.snowflake. |
| 8 | tDBRow_1 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 9 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 10 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 11 | tJava_2 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 12 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 13 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 14 | tJava_3 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 15 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=false, `FOLDER`=false |
| 16 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 17 | tJava_4 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 18 | tDBRow_2 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 19 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| CUSTOMER | id_String | Yes | 7 |
| CHANNEL | id_String | Yes | 20 |
| MSO | id_String | Yes | 100 |
| REGION | id_String | Yes | 100 |
| DIVISION | id_String | Yes | 100 |
| MARKET | id_String | Yes | 100 |
| GOALSROLLUP | id_String | Yes | 100 |
| LEGACYPLATFORM | id_String | Yes | 20 |
| LEGACYCLIENTNUMBER | id_String | Yes | 10 |
| OLD_CHANNEL | id_String | Yes | 20 |
| OLD_MSO | id_String | Yes | 100 |
| OLD_REGION | id_String | Yes | 100 |
| OLD_DIVISION | id_String | Yes | 100 |
| OLD_MARKET | id_String | Yes | 100 |
| OLD_GOALSROLLUP | id_String | Yes | 100 |
| OLD_CUSTOMERNAME | id_String | Yes | 100 |
| ISHARRISCUSTOMER | id_Integer | Yes | -1 |
| PLGROUP | id_String | Yes | 100 |
| DEPARTMENT | id_String | Yes | 100 |
| ACCTGRP1 | id_String | Yes | 100 |
| ACCTGRP2 | id_String | Yes | 100 |
| CUSTOMER | id_String | Yes | 7 |
| CHANNEL | id_String | Yes | 20 |
| MSO | id_String | Yes | 100 |
| REGION | id_String | Yes | 100 |
| DIVISION | id_String | Yes | 100 |
| MARKET | id_String | Yes | 100 |
| GOALSROLLUP | id_String | Yes | 100 |
| LEGACYPLATFORM | id_String | Yes | 20 |
| LEGACYCLIENTNUMBER | id_String | Yes | 10 |
| OLD_CHANNEL | id_String | Yes | 20 |
| OLD_MSO | id_String | Yes | 100 |
| OLD_REGION | id_String | Yes | 100 |
| OLD_DIVISION | id_String | Yes | 100 |
| OLD_MARKET | id_String | Yes | 100 |
| OLD_GOALSROLLUP | id_String | Yes | 100 |
| OLD_CUSTOMERNAME | id_String | Yes | 100 |
| ISHARRISCUSTOMER | id_Integer | Yes | -1 |
| PLGROUP | id_String | Yes | 100 |
| DEPARTMENT | id_String | Yes | 100 |
| ACCTGRP1 | id_String | Yes | 100 |
| ACCTGRP2 | id_String | Yes | 100 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| CUSTOMER | id_String | No | 7 |
| CHANNEL | id_String | Yes | 20 |
| MSO | id_String | Yes | 100 |
| REGION | id_String | Yes | 100 |
| DIVISION | id_String | Yes | 100 |
| MARKET | id_String | Yes | 100 |
| GOALSROLLUP | id_String | Yes | 100 |
| LEGACYPLATFORM | id_String | Yes | 20 |
| LEGACYCLIENTNUMBER | id_String | Yes | 10 |
| OLD_CHANNEL | id_String | Yes | 20 |
| OLD_MSO | id_String | Yes | 100 |
| OLD_REGION | id_String | Yes | 100 |
| OLD_DIVISION | id_String | Yes | 100 |
| OLD_MARKET | id_String | Yes | 100 |
| OLD_GOALSROLLUP | id_String | Yes | 100 |
| OLD_CUSTOMERNAME | id_String | Yes | 100 |
| ISHARRISCUSTOMER | id_Integer | Yes | -1 |
| PLGROUP | id_String | Yes | 100 |
| DEPARTMENT | id_String | Yes | 100 |
| ACCTGRP1 | id_String | Yes | 100 |
| ACCTGRP2 | id_String | Yes | 100 |

### tFlowMeter_3

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| CUSTOMER | id_String | No | 7 |
| CHANNEL | id_String | Yes | 20 |
| MSO | id_String | Yes | 100 |
| REGION | id_String | Yes | 100 |
| DIVISION | id_String | Yes | 100 |
| MARKET | id_String | Yes | 100 |
| GOALSROLLUP | id_String | Yes | 100 |
| LEGACYPLATFORM | id_String | Yes | 20 |
| LEGACYCLIENTNUMBER | id_String | Yes | 10 |
| OLD_CHANNEL | id_String | Yes | 20 |
| OLD_MSO | id_String | Yes | 100 |
| OLD_REGION | id_String | Yes | 100 |
| OLD_DIVISION | id_String | Yes | 100 |
| OLD_MARKET | id_String | Yes | 100 |
| OLD_GOALSROLLUP | id_String | Yes | 100 |
| OLD_CUSTOMERNAME | id_String | Yes | 100 |
| ISHARRISCUSTOMER | id_Integer | Yes | -1 |
| PLGROUP | id_String | Yes | 100 |
| DEPARTMENT | id_String | Yes | 100 |
| ACCTGRP1 | id_String | Yes | 100 |
| ACCTGRP2 | id_String | Yes | 100 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| CUSTOMER | id_String | No | 7 |
| CHANNEL | id_String | Yes | 20 |
| MSO | id_String | Yes | 100 |
| REGION | id_String | Yes | 100 |
| DIVISION | id_String | Yes | 100 |
| MARKET | id_String | Yes | 100 |
| GOALSROLLUP | id_String | Yes | 100 |
| LEGACYPLATFORM | id_String | Yes | 20 |
| LEGACYCLIENTNUMBER | id_String | Yes | 10 |
| OLD_CHANNEL | id_String | Yes | 20 |
| OLD_MSO | id_String | Yes | 100 |
| OLD_REGION | id_String | Yes | 100 |
| OLD_DIVISION | id_String | Yes | 100 |
| OLD_MARKET | id_String | Yes | 100 |
| OLD_GOALSROLLUP | id_String | Yes | 100 |
| OLD_CUSTOMERNAME | id_String | Yes | 100 |
| ISHARRISCUSTOMER | id_Integer | Yes | -1 |
| PLGROUP | id_String | Yes | 100 |
| DEPARTMENT | id_String | Yes | 100 |
| ACCTGRP1 | id_String | Yes | 100 |
| ACCTGRP2 | id_String | Yes | 100 |
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
    tMap_1 -->|FLOW| tFlowMeter_3
    tFlowMeter_3 -->|FLOW| tDBOutput_1
    tDBRow_1 -->|SUBJOB_OK| tFileList_1
    tPrejob_1 -->|COMPONENT_OK| tJava_4
    tFileList_2 -->|ITERATE| tJava_2
    tFileList_2 -->|SUBJOB_OK| tFileList_3
    tJava_2 -->|ITERATE| tFileArchive_1
    tFileList_3 -->|ITERATE| tJava_3
    tJava_3 -->|ITERATE| tFileDelete_1
    tParallelize_1 -->|PARALLELIZE| tFileList_2
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tJava_4 -->|SUBJOB_OK| tSetKeystore_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
