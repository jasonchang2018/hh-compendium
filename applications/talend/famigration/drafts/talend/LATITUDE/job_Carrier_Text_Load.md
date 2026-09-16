# Talend Job: Carrier_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2026-01-19T09:03:18.128-0800
- **Last Modified**: 2026-01-19T09:23:43.426-0800

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
| 9 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 10 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 11 | tJava_2 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 12 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 13 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 14 | tJava_4 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 15 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=false, `FOLDER`=false |
| 16 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 17 | tJava_3 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 18 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| CARRIERID | id_BigDecimal | No | 38 |
| CARRIERNAME | id_String | Yes | 200 |
| CARRIERSTREET1 | id_String | Yes | 250 |
| CARRIERSTREET2 | id_String | Yes | 250 |
| CARRIERCITY | id_String | Yes | 100 |
| CARRIERSTATE | id_String | Yes | 3 |
| CARRIERZIP | id_String | Yes | 10 |
| CARRIERCOUNTRY | id_String | Yes | 250 |
| CARRIERCOUNTY | id_String | Yes | 250 |
| CARRIERPHONE | id_String | Yes | 60 |
| CARRIERFAX | id_String | Yes | 60 |
| CREATEDDATE | id_String | Yes | 30 |
| CREATEDBY | id_BigDecimal | Yes | 38 |
| UPDATEDDATE | id_String | Yes | 30 |
| UPDATEDBY | id_BigDecimal | Yes | 38 |
| ENABLED | id_BigDecimal | No | 38 |
| PAYOR_CODE | id_String | Yes | 50 |
| CARRIERDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CARRIERREFDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CONVERSATION_LIMIT | id_BigDecimal | Yes | 38 |
| WEBSITE | id_String | Yes | 50 |
| PHONENUMBER | id_String | Yes | 50 |
| CONTACTORGANIZATION | id_String | Yes | 50 |
| CARRIERID | id_BigDecimal | No | 38 |
| CARRIERNAME | id_String | Yes | 200 |
| CARRIERSTREET1 | id_String | Yes | 250 |
| CARRIERSTREET2 | id_String | Yes | 250 |
| CARRIERCITY | id_String | Yes | 100 |
| CARRIERSTATE | id_String | Yes | 3 |
| CARRIERZIP | id_String | Yes | 10 |
| CARRIERCOUNTRY | id_String | Yes | 250 |
| CARRIERCOUNTY | id_String | Yes | 250 |
| CARRIERPHONE | id_String | Yes | 60 |
| CARRIERFAX | id_String | Yes | 60 |
| CREATEDDATE | id_String | Yes | 30 |
| CREATEDBY | id_BigDecimal | Yes | 38 |
| UPDATEDDATE | id_String | Yes | 30 |
| UPDATEDBY | id_BigDecimal | Yes | 38 |
| ENABLED | id_BigDecimal | No | 38 |
| PAYOR_CODE | id_String | Yes | 50 |
| CARRIERDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CARRIERREFDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CONVERSATION_LIMIT | id_BigDecimal | Yes | 38 |
| WEBSITE | id_String | Yes | 50 |
| PHONENUMBER | id_String | Yes | 50 |
| CONTACTORGANIZATION | id_String | Yes | 50 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| CARRIERID | id_BigDecimal | No | 38 |
| CARRIERNAME | id_String | Yes | 200 |
| CARRIERSTREET1 | id_String | Yes | 250 |
| CARRIERSTREET2 | id_String | Yes | 250 |
| CARRIERCITY | id_String | Yes | 100 |
| CARRIERSTATE | id_String | Yes | 3 |
| CARRIERZIP | id_String | Yes | 10 |
| CARRIERCOUNTRY | id_String | Yes | 250 |
| CARRIERCOUNTY | id_String | Yes | 250 |
| CARRIERPHONE | id_String | Yes | 60 |
| CARRIERFAX | id_String | Yes | 60 |
| CREATEDDATE | id_String | Yes | 30 |
| CREATEDBY | id_BigDecimal | Yes | 38 |
| UPDATEDDATE | id_String | Yes | 30 |
| UPDATEDBY | id_BigDecimal | Yes | 38 |
| ENABLED | id_BigDecimal | No | 38 |
| PAYOR_CODE | id_String | Yes | 50 |
| CARRIERDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CARRIERREFDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CONVERSATION_LIMIT | id_BigDecimal | Yes | 38 |
| WEBSITE | id_String | Yes | 50 |
| PHONENUMBER | id_String | Yes | 50 |
| CONTACTORGANIZATION | id_String | Yes | 50 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| CARRIERID | id_BigDecimal | No | 38 |
| CARRIERNAME | id_String | Yes | 200 |
| CARRIERSTREET1 | id_String | Yes | 250 |
| CARRIERSTREET2 | id_String | Yes | 250 |
| CARRIERCITY | id_String | Yes | 100 |
| CARRIERSTATE | id_String | Yes | 3 |
| CARRIERZIP | id_String | Yes | 10 |
| CARRIERCOUNTRY | id_String | Yes | 250 |
| CARRIERCOUNTY | id_String | Yes | 250 |
| CARRIERPHONE | id_String | Yes | 60 |
| CARRIERFAX | id_String | Yes | 60 |
| CREATEDDATE | id_String | Yes | 30 |
| CREATEDBY | id_BigDecimal | Yes | 38 |
| UPDATEDDATE | id_String | Yes | 30 |
| UPDATEDBY | id_BigDecimal | Yes | 38 |
| ENABLED | id_BigDecimal | No | 38 |
| PAYOR_CODE | id_String | Yes | 50 |
| CARRIERDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CARRIERREFDOCPROVIDERNUMBER | id_String | Yes | 50 |
| CONVERSATION_LIMIT | id_BigDecimal | Yes | 38 |
| WEBSITE | id_String | Yes | 50 |
| PHONENUMBER | id_String | Yes | 50 |
| CONTACTORGANIZATION | id_String | Yes | 50 |
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
    tPrejob_1 -->|COMPONENT_OK| tJava_3
    tFileList_2 -->|SUBJOB_OK| tFileList_3
    tFileList_2 -->|ITERATE| tJava_2
    tJava_2 -->|ITERATE| tFileArchive_1
    tFileList_3 -->|ITERATE| tJava_4
    tJava_4 -->|ITERATE| tFileDelete_1
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tParallelize_1 -->|PARALLELIZE| tFileList_2
    tJava_3 -->|SUBJOB_OK| tSetKeystore_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
