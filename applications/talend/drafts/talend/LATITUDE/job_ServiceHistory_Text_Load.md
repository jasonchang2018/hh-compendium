# Talend Job: ServiceHistory_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2024-11-21T14:01:01.406-0800
- **Last Modified**: 2025-10-02T10:57:17.878-0700

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tDBConnection_1 | `tSnowflakeConnection` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":2,"@type":"org.talend.components.snowflake. |
| 2 | tFileList_1 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 3 | tJava_1 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 4 | tFileInputDelimited_1 | `tFileInputDelimited` | `USE_EXISTING_DYNAMIC`=false, `FILENAMETEXT`="When the input source is a stream or a zip file,f, `FILENAME`=context.filePath, `CSV_OPTION`=false, `ROWSEPARATOR`="|$|" |
| 5 | tMap_1 | `tMap` | `LINK_STYLE`=AUTO, `DIE_ON_ERROR`=true, `LKUP_PARALLELIZE`=false, `LEVENSHTEIN`=0, `JACCARD`=0 |
| 6 | tDBOutput_1 | `tSnowflakeOutput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 7 | tDBRow_1 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 8 | tDBRow_2 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 9 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 10 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 11 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 12 | tJava_3 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 13 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 14 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 15 | tJava_4 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 16 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=false, `FOLDER`=false |
| 17 | tJava_2 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 18 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| RequestID | id_Integer | Yes | -1 |
| AcctID | id_Integer | Yes | -1 |
| DebtorID | id_Integer | Yes | -1 |
| CreationDate | id_String | Yes | 30 |
| ReturnedDate | id_String | Yes | 30 |
| ServiceID | id_Integer | Yes | -1 |
| RequestedBY | id_String | Yes | 256 |
| RequestedProgram | id_String | Yes | 256 |
| Processed | id_Integer | Yes | -1 |
| XMLInfoRequested | id_String | Yes | -1 |
| XMLInfoReturned | id_String | Yes | -1 |
| FileName | id_String | Yes | -1 |
| Cost | id_String | Yes | 30 |
| SystemYear | id_Integer | Yes | -1 |
| SystemMonth | id_Integer | Yes | -1 |
| ServiceBatch | id_String | Yes | 20 |
| VerifiedBy | id_String | Yes | 10 |
| VerifiedDate | id_String | Yes | 30 |
| BatchId | id_String | Yes | 30 |
| ProfileID | id_String | Yes | -1 |
| PackageID | id_Integer | Yes | -1 |
| RequestingDate | id_String | Yes | 30 |
| RequestedDate | id_String | Yes | 30 |
| ResponseBatchID | id_String | Yes | -1 |
| TypeName | id_String | Yes | 25 |
| RequestID | id_Integer | Yes | -1 |
| AcctID | id_Integer | Yes | -1 |
| DebtorID | id_Integer | Yes | -1 |
| CreationDate | id_String | Yes | 30 |
| ReturnedDate | id_String | Yes | 30 |
| ServiceID | id_Integer | Yes | -1 |
| RequestedBY | id_String | Yes | 256 |
| RequestedProgram | id_String | Yes | 256 |
| Processed | id_Integer | Yes | -1 |
| XMLInfoRequested | id_String | Yes | -1 |
| XMLInfoReturned | id_String | Yes | -1 |
| FileName | id_String | Yes | -1 |
| Cost | id_String | Yes | 30 |
| SystemYear | id_Integer | Yes | -1 |
| SystemMonth | id_Integer | Yes | -1 |
| ServiceBatch | id_String | Yes | 20 |
| VerifiedBy | id_String | Yes | 10 |
| VerifiedDate | id_String | Yes | 30 |
| BatchId | id_String | Yes | 30 |
| ProfileID | id_String | Yes | -1 |
| PackageID | id_Integer | Yes | -1 |
| RequestingDate | id_String | Yes | 30 |
| RequestedDate | id_String | Yes | 30 |
| ResponseBatchID | id_String | Yes | -1 |
| TypeName | id_String | Yes | 25 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| REQUESTID | id_Integer | No | -1 |
| ACCTID | id_Integer | Yes | -1 |
| DEBTORID | id_Integer | Yes | -1 |
| CREATIONDATE | id_String | Yes | 30 |
| RETURNEDDATE | id_String | Yes | 30 |
| SERVICEID | id_Integer | Yes | -1 |
| REQUESTEDBY | id_String | Yes | 256 |
| REQUESTEDPROGRAM | id_String | Yes | 256 |
| PROCESSED | id_Integer | Yes | -1 |
| XMLINFOREQUESTED | id_String | Yes | 16777216 |
| XMLINFORETURNED | id_String | Yes | 16777216 |
| FILENAME | id_String | Yes | 2000 |
| COST | id_String | Yes | 30 |
| SYSTEMYEAR | id_Integer | Yes | -1 |
| SYSTEMMONTH | id_Integer | Yes | -1 |
| SERVICEBATCH | id_String | Yes | 30 |
| VERIFIEDBY | id_String | Yes | 10 |
| VERIFIEDDATE | id_String | Yes | 30 |
| BATCHID | id_String | Yes | 16777216 |
| PROFILEID | id_String | Yes | 16777216 |
| PACKAGEID | id_Integer | Yes | -1 |
| REQUESTINGDATE | id_String | Yes | 30 |
| REQUESTEDDATE | id_String | Yes | 30 |
| RESPONSEBATCHID | id_String | Yes | 16777216 |
| TYPENAME | id_String | Yes | 25 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| REQUESTID | id_Integer | No | -1 |
| ACCTID | id_Integer | Yes | -1 |
| DEBTORID | id_Integer | Yes | -1 |
| CREATIONDATE | id_String | Yes | 30 |
| RETURNEDDATE | id_String | Yes | 30 |
| SERVICEID | id_Integer | Yes | -1 |
| REQUESTEDBY | id_String | Yes | 256 |
| REQUESTEDPROGRAM | id_String | Yes | 256 |
| PROCESSED | id_Integer | Yes | -1 |
| XMLINFOREQUESTED | id_String | Yes | 16777216 |
| XMLINFORETURNED | id_String | Yes | 16777216 |
| FILENAME | id_String | Yes | 2000 |
| COST | id_String | Yes | 30 |
| SYSTEMYEAR | id_Integer | Yes | -1 |
| SYSTEMMONTH | id_Integer | Yes | -1 |
| SERVICEBATCH | id_String | Yes | 30 |
| VERIFIEDBY | id_String | Yes | 10 |
| VERIFIEDDATE | id_String | Yes | 30 |
| BATCHID | id_String | Yes | 16777216 |
| PROFILEID | id_String | Yes | 16777216 |
| PACKAGEID | id_Integer | Yes | -1 |
| REQUESTINGDATE | id_String | Yes | 30 |
| REQUESTEDDATE | id_String | Yes | 30 |
| RESPONSEBATCHID | id_String | Yes | 16777216 |
| TYPENAME | id_String | Yes | 25 |
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
    tPrejob_1 -->|COMPONENT_OK| tJava_2
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tParallelize_1 -->|PARALLELIZE| tFileList_2
    tFileList_2 -->|SUBJOB_OK| tFileList_3
    tFileList_2 -->|ITERATE| tJava_3
    tJava_3 -->|ITERATE| tFileArchive_1
    tFileList_3 -->|ITERATE| tJava_4
    tJava_4 -->|ITERATE| tFileDelete_1
    tJava_2 -->|SUBJOB_OK| tSetKeystore_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
