# Talend Job: cmi_Dialer_SBT_History_Table_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2024-11-05T10:39:49.444-0800
- **Last Modified**: 2025-09-29T21:30:00.095-0700

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
| 9 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 10 | tJava_2 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 11 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 12 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 13 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 14 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 15 | tJava_3 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 16 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=false, `FOLDER`=false |
| 17 | tJava_4 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 18 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| ID | id_String | Yes | -1 |
| MobileNo | id_String | Yes | -1 |
| MessageId | id_String | Yes | -1 |
| DeliveryStatus | id_String | Yes | -1 |
| DeliveryStatusCode | id_String | Yes | -1 |
| Message | id_String | Yes | -1 |
| MessageCategory | id_String | Yes | -1 |
| Direction | id_String | Yes | -1 |
| ReferenceId | id_String | Yes | -1 |
| CommunicationCode | id_String | Yes | -1 |
| ReceivedAt | id_String | Yes | -1 |
| ReceivedTimeLocal | id_String | Yes | -1 |
| ReadAt | id_String | Yes | -1 |
| ReadTimeLocal | id_String | Yes | -1 |
| SentAt | id_String | Yes | -1 |
| SentTimeLocal | id_String | Yes | -1 |
| DeliveredAt | id_String | Yes | -1 |
| DeliveredTimeLocal | id_String | Yes | -1 |
| MessageTime | id_String | Yes | -1 |
| MessageTimeLocal | id_String | Yes | -1 |
| TotalMessageSegments | id_String | Yes | -1 |
| AccountID | id_String | Yes | -1 |
| DateLoaded | id_String | Yes | -1 |
| FullFileName | id_String | Yes | -1 |
| DebtorSeq | id_String | Yes | -1 |
| ID | id_String | Yes | -1 |
| MobileNo | id_String | Yes | -1 |
| MessageId | id_String | Yes | -1 |
| DeliveryStatus | id_String | Yes | -1 |
| DeliveryStatusCode | id_String | Yes | -1 |
| Message | id_String | Yes | -1 |
| MessageCategory | id_String | Yes | -1 |
| Direction | id_String | Yes | -1 |
| ReferenceId | id_String | Yes | -1 |
| CommunicationCode | id_String | Yes | -1 |
| ReceivedAt | id_String | Yes | -1 |
| ReceivedTimeLocal | id_String | Yes | -1 |
| ReadAt | id_String | Yes | -1 |
| ReadTimeLocal | id_String | Yes | -1 |
| SentAt | id_String | Yes | -1 |
| SentTimeLocal | id_String | Yes | -1 |
| DeliveredAt | id_String | Yes | -1 |
| DeliveredTimeLocal | id_String | Yes | -1 |
| MessageTime | id_String | Yes | -1 |
| MessageTimeLocal | id_String | Yes | -1 |
| TotalMessageSegments | id_String | Yes | -1 |
| AccountID | id_String | Yes | -1 |
| DateLoaded | id_String | Yes | -1 |
| FullFileName | id_String | Yes | -1 |
| DebtorSeq | id_String | Yes | -1 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_String | No | -1 |
| MOBILENO | id_String | Yes | 16777216 |
| MESSAGEID | id_String | Yes | 16777216 |
| DELIVERYSTATUS | id_String | Yes | 16777216 |
| DELIVERYSTATUSCODE | id_String | Yes | 16777216 |
| MESSAGE | id_String | Yes | 16777216 |
| MESSAGECATEGORY | id_String | Yes | 16777216 |
| DIRECTION | id_String | Yes | 16777216 |
| REFERENCEID | id_String | Yes | 16777216 |
| COMMUNICATIONCODE | id_String | Yes | 16777216 |
| RECEIVEDAT | id_String | Yes | 16777216 |
| RECEIVEDTIMELOCAL | id_String | Yes | 16777216 |
| READAT | id_String | Yes | 16777216 |
| READTIMELOCAL | id_String | Yes | 16777216 |
| SENTAT | id_String | Yes | 16777216 |
| SENTTIMELOCAL | id_String | Yes | 16777216 |
| DELIVEREDAT | id_String | Yes | 16777216 |
| DELIVEREDTIMELOCAL | id_String | Yes | 16777216 |
| MESSAGETIME | id_String | Yes | 16777216 |
| MESSAGETIMELOCAL | id_String | Yes | 16777216 |
| TOTALMESSAGESEGMENTS | id_String | Yes | 16777216 |
| ACCOUNTID | id_String | Yes | -1 |
| DATELOADED | id_String | Yes | 16777216 |
| FULLFILENAME | id_String | Yes | 16777216 |
| DEBTORSEQ | id_String | Yes | -1 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_String | No | -1 |
| MOBILENO | id_String | Yes | 16777216 |
| MESSAGEID | id_String | Yes | 16777216 |
| DELIVERYSTATUS | id_String | Yes | 16777216 |
| DELIVERYSTATUSCODE | id_String | Yes | 16777216 |
| MESSAGE | id_String | Yes | 16777216 |
| MESSAGECATEGORY | id_String | Yes | 16777216 |
| DIRECTION | id_String | Yes | 16777216 |
| REFERENCEID | id_String | Yes | 16777216 |
| COMMUNICATIONCODE | id_String | Yes | 16777216 |
| RECEIVEDAT | id_String | Yes | 16777216 |
| RECEIVEDTIMELOCAL | id_String | Yes | 16777216 |
| READAT | id_String | Yes | 16777216 |
| READTIMELOCAL | id_String | Yes | 16777216 |
| SENTAT | id_String | Yes | 16777216 |
| SENTTIMELOCAL | id_String | Yes | 16777216 |
| DELIVEREDAT | id_String | Yes | 16777216 |
| DELIVEREDTIMELOCAL | id_String | Yes | 16777216 |
| MESSAGETIME | id_String | Yes | 16777216 |
| MESSAGETIMELOCAL | id_String | Yes | 16777216 |
| TOTALMESSAGESEGMENTS | id_String | Yes | 16777216 |
| ACCOUNTID | id_String | Yes | -1 |
| DATELOADED | id_String | Yes | 16777216 |
| FULLFILENAME | id_String | Yes | 16777216 |
| DEBTORSEQ | id_String | Yes | -1 |
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
    tPrejob_1 -->|COMPONENT_OK| tJava_4
    tFileList_3 -->|ITERATE| tJava_3
    tJava_3 -->|ITERATE| tFileDelete_1
    tJava_4 -->|SUBJOB_OK| tSetKeystore_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
