# Talend Job: Desk_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2025-07-17T21:38:26.788-0700
- **Last Modified**: 2025-09-30T19:32:28.776-0700

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tDBConnection_1 | `tSnowflakeConnection` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":2,"@type":"org.talend.components.snowflake. |
| 2 | tPrejob_1 | `tPrejob` | `CONNECTION_FORMAT`=row |
| 3 | tJava_1 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 4 | tDBRow_1 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 5 | tFileList_1 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 6 | tJava_2 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 7 | tFileInputDelimited_1 | `tFileInputDelimited` | `USE_EXISTING_DYNAMIC`=false, `FILENAMETEXT`="When the input source is a stream or a zip file,f, `FILENAME`=context.filePath, `CSV_OPTION`=false, `ROWSEPARATOR`="|$|" |
| 8 | tFileProperties_1 | `tFileProperties` | `FILENAME`=context.filePath, `MD5`=false, `CONNECTION_FORMAT`=row |
| 9 | tJavaRow_1 | `tJavaRow` | `CODE`=//Code generated according to input schema and out, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 10 | tMap_1 | `tMap` | `LINK_STYLE`=AUTO, `DIE_ON_ERROR`=true, `LKUP_PARALLELIZE`=false, `LEVENSHTEIN`=0, `JACCARD`=0 |
| 11 | tFlowMeter_1 | `tFlowMeter` | `USEROWLABEL`=true, `METTERLABEL`="MyLabel", `ABSOLUTE`=Absolute, `CONNECTION_FORMAT`=row |
| 12 | tDBOutput_1 | `tSnowflakeOutput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 13 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 14 | tJava_3 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 15 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 16 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 17 | tDBRow_2 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 18 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 19 | tJava_4 | `tJava` | `CODE`=context.filePath=((String)globalMap.get("tFileList, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 20 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=true, `FOLDER`=false |
| 21 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tDBRow_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| CODE | id_String | No | 10 |
| CTL | id_String | Yes | 3 |
| PRIV | id_String | Yes | 100 |
| NAME | id_String | Yes | 30 |
| DESKTYPE | id_String | Yes | 15 |
| PASSWORD | id_String | Yes | 8 |
| FEES | id_String | Yes | 20 |
| COLLECTIONS | id_String | Yes | 20 |
| MTDPDCFEES | id_String | Yes | 20 |
| MTDPDCCOLLECTIONS | id_String | Yes | 20 |
| MTDFEES | id_String | Yes | 20 |
| MTDCOLLECTIONS | id_String | Yes | 20 |
| YTDFEES | id_String | Yes | 20 |
| YTDCOLLECTIONS | id_String | Yes | 20 |
| BRANCH | id_String | Yes | 5 |
| QUEUERPTDAYS | id_Integer | Yes | 38 |
| QUEUERPT | id_String | Yes | 1 |
| WAITDAYS | id_Integer | Yes | 38 |
| MONTHLYGOAL | id_String | Yes | 20 |
| MONTHLYCBRREQUESTS | id_Integer | No | 38 |
| CBRREQUESTS | id_Integer | No | 38 |
| CASELIMIT | id_Integer | Yes | 38 |
| ENFORCELIMIT | id_Integer | Yes | 38 |
| DAILYLIMIT | id_Integer | Yes | 38 |
| NEWBIZDAYS | id_Integer | Yes | 38 |
| MAXFOLLOWUP | id_Integer | Yes | 38 |
| CALIAS | id_String | Yes | 30 |
| PHONE | id_String | Yes | 12 |
| EXTENSION | id_String | Yes | 6 |
| EMAIL | id_String | Yes | 50 |
| MONTHLYGOAL2 | id_String | Yes | 20 |
| SPECIAL1 | id_String | Yes | 20 |
| SPECIAL2 | id_String | Yes | 20 |
| SPECIAL3 | id_String | Yes | 20 |
| VPASSWORD | id_String | Yes | 10 |
| TEAMID | id_Integer | Yes | 38 |
| PREVENTLINKING | id_Integer | No | 38 |
| CODE | id_String | No | 10 |
| CTL | id_String | Yes | 3 |
| PRIV | id_String | Yes | 100 |
| NAME | id_String | Yes | 30 |
| DESKTYPE | id_String | Yes | 15 |
| PASSWORD | id_String | Yes | 8 |
| FEES | id_String | Yes | 20 |
| COLLECTIONS | id_String | Yes | 20 |
| MTDPDCFEES | id_String | Yes | 20 |
| MTDPDCCOLLECTIONS | id_String | Yes | 20 |
| MTDFEES | id_String | Yes | 20 |
| MTDCOLLECTIONS | id_String | Yes | 20 |
| YTDFEES | id_String | Yes | 20 |
| YTDCOLLECTIONS | id_String | Yes | 20 |
| BRANCH | id_String | Yes | 5 |
| QUEUERPTDAYS | id_Integer | Yes | 38 |
| QUEUERPT | id_String | Yes | 1 |
| WAITDAYS | id_Integer | Yes | 38 |
| MONTHLYGOAL | id_String | Yes | 20 |
| MONTHLYCBRREQUESTS | id_Integer | No | 38 |
| CBRREQUESTS | id_Integer | No | 38 |
| CASELIMIT | id_Integer | Yes | 38 |
| ENFORCELIMIT | id_Integer | Yes | 38 |
| DAILYLIMIT | id_Integer | Yes | 38 |
| NEWBIZDAYS | id_Integer | Yes | 38 |
| MAXFOLLOWUP | id_Integer | Yes | 38 |
| CALIAS | id_String | Yes | 30 |
| PHONE | id_String | Yes | 12 |
| EXTENSION | id_String | Yes | 6 |
| EMAIL | id_String | Yes | 50 |
| MONTHLYGOAL2 | id_String | Yes | 20 |
| SPECIAL1 | id_String | Yes | 20 |
| SPECIAL2 | id_String | Yes | 20 |
| SPECIAL3 | id_String | Yes | 20 |
| VPASSWORD | id_String | Yes | 10 |
| TEAMID | id_Integer | Yes | 38 |
| PREVENTLINKING | id_Integer | No | 38 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tFileProperties_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| abs_path | id_String | Yes | 255 |
| dirname | id_String | Yes | 255 |
| basename | id_String | Yes | 255 |
| mode_string | id_String | Yes | 10 |
| size | id_Long | Yes | 20 |
| mtime | id_Long | Yes | 20 |
| mtime_string | id_String | Yes | 20 |

### tJavaRow_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| abs_path | id_String | Yes | 255 |
| dirname | id_String | Yes | 255 |
| basename | id_String | Yes | 255 |
| mode_string | id_String | Yes | 10 |
| size | id_Long | Yes | 20 |
| mtime | id_Long | Yes | 20 |
| mtime_string | id_String | Yes | 20 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| LASTMODIFIED | id_BigDecimal | Yes | -1 |
| CODE | id_String | No | 10 |
| CTL | id_String | Yes | 3 |
| PRIV | id_String | Yes | 100 |
| NAME | id_String | Yes | 30 |
| DESKTYPE | id_String | Yes | 15 |
| PASSWORD | id_String | Yes | 8 |
| FEES | id_String | Yes | 20 |
| COLLECTIONS | id_String | Yes | 20 |
| MTDPDCFEES | id_String | Yes | 20 |
| MTDPDCCOLLECTIONS | id_String | Yes | 20 |
| MTDFEES | id_String | Yes | 20 |
| MTDCOLLECTIONS | id_String | Yes | 20 |
| YTDFEES | id_String | Yes | 20 |
| YTDCOLLECTIONS | id_String | Yes | 20 |
| BRANCH | id_String | Yes | 5 |
| QUEUERPTDAYS | id_Integer | Yes | 38 |
| QUEUERPT | id_String | Yes | 1 |
| WAITDAYS | id_Integer | Yes | 38 |
| MONTHLYGOAL | id_String | Yes | 20 |
| MONTHLYCBRREQUESTS | id_Integer | No | 38 |
| CBRREQUESTS | id_Integer | No | 38 |
| CASELIMIT | id_Integer | Yes | 38 |
| ENFORCELIMIT | id_Integer | Yes | 38 |
| DAILYLIMIT | id_Integer | Yes | 38 |
| NEWBIZDAYS | id_Integer | Yes | 38 |
| MAXFOLLOWUP | id_Integer | Yes | 38 |
| CALIAS | id_String | Yes | 30 |
| PHONE | id_String | Yes | 12 |
| EXTENSION | id_String | Yes | 6 |
| EMAIL | id_String | Yes | 50 |
| MONTHLYGOAL2 | id_String | Yes | 20 |
| SPECIAL1 | id_String | Yes | 20 |
| SPECIAL2 | id_String | Yes | 20 |
| SPECIAL3 | id_String | Yes | 20 |
| VPASSWORD | id_String | Yes | 10 |
| TEAMID | id_Integer | Yes | 38 |
| PREVENTLINKING | id_Integer | No | 38 |

### tFlowMeter_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| LASTMODIFIED | id_BigDecimal | Yes | -1 |
| CODE | id_String | No | 10 |
| CTL | id_String | Yes | 3 |
| PRIV | id_String | Yes | 100 |
| NAME | id_String | Yes | 30 |
| DESKTYPE | id_String | Yes | 15 |
| PASSWORD | id_String | Yes | 8 |
| FEES | id_String | Yes | 20 |
| COLLECTIONS | id_String | Yes | 20 |
| MTDPDCFEES | id_String | Yes | 20 |
| MTDPDCCOLLECTIONS | id_String | Yes | 20 |
| MTDFEES | id_String | Yes | 20 |
| MTDCOLLECTIONS | id_String | Yes | 20 |
| YTDFEES | id_String | Yes | 20 |
| YTDCOLLECTIONS | id_String | Yes | 20 |
| BRANCH | id_String | Yes | 5 |
| QUEUERPTDAYS | id_Integer | Yes | 38 |
| QUEUERPT | id_String | Yes | 1 |
| WAITDAYS | id_Integer | Yes | 38 |
| MONTHLYGOAL | id_String | Yes | 20 |
| MONTHLYCBRREQUESTS | id_Integer | No | 38 |
| CBRREQUESTS | id_Integer | No | 38 |
| CASELIMIT | id_Integer | Yes | 38 |
| ENFORCELIMIT | id_Integer | Yes | 38 |
| DAILYLIMIT | id_Integer | Yes | 38 |
| NEWBIZDAYS | id_Integer | Yes | 38 |
| MAXFOLLOWUP | id_Integer | Yes | 38 |
| CALIAS | id_String | Yes | 30 |
| PHONE | id_String | Yes | 12 |
| EXTENSION | id_String | Yes | 6 |
| EMAIL | id_String | Yes | 50 |
| MONTHLYGOAL2 | id_String | Yes | 20 |
| SPECIAL1 | id_String | Yes | 20 |
| SPECIAL2 | id_String | Yes | 20 |
| SPECIAL3 | id_String | Yes | 20 |
| VPASSWORD | id_String | Yes | 10 |
| TEAMID | id_Integer | Yes | 38 |
| PREVENTLINKING | id_Integer | No | 38 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| LASTMODIFIED | id_BigDecimal | Yes | -1 |
| CODE | id_String | No | 10 |
| CTL | id_String | Yes | 3 |
| PRIV | id_String | Yes | 100 |
| NAME | id_String | Yes | 30 |
| DESKTYPE | id_String | Yes | 15 |
| PASSWORD | id_String | Yes | 8 |
| FEES | id_String | Yes | 20 |
| COLLECTIONS | id_String | Yes | 20 |
| MTDPDCFEES | id_String | Yes | 20 |
| MTDPDCCOLLECTIONS | id_String | Yes | 20 |
| MTDFEES | id_String | Yes | 20 |
| MTDCOLLECTIONS | id_String | Yes | 20 |
| YTDFEES | id_String | Yes | 20 |
| YTDCOLLECTIONS | id_String | Yes | 20 |
| BRANCH | id_String | Yes | 5 |
| QUEUERPTDAYS | id_Integer | Yes | 38 |
| QUEUERPT | id_String | Yes | 1 |
| WAITDAYS | id_Integer | Yes | 38 |
| MONTHLYGOAL | id_String | Yes | 20 |
| MONTHLYCBRREQUESTS | id_Integer | No | 38 |
| CBRREQUESTS | id_Integer | No | 38 |
| CASELIMIT | id_Integer | Yes | 38 |
| ENFORCELIMIT | id_Integer | Yes | 38 |
| DAILYLIMIT | id_Integer | Yes | 38 |
| NEWBIZDAYS | id_Integer | Yes | 38 |
| MAXFOLLOWUP | id_Integer | Yes | 38 |
| CALIAS | id_String | Yes | 30 |
| PHONE | id_String | Yes | 12 |
| EXTENSION | id_String | Yes | 6 |
| EMAIL | id_String | Yes | 50 |
| MONTHLYGOAL2 | id_String | Yes | 20 |
| SPECIAL1 | id_String | Yes | 20 |
| SPECIAL2 | id_String | Yes | 20 |
| SPECIAL3 | id_String | Yes | 20 |
| VPASSWORD | id_String | Yes | 10 |
| TEAMID | id_Integer | Yes | 38 |
| PREVENTLINKING | id_Integer | No | 38 |
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
    tDBRow_1 -->|SUBJOB_OK| tFileList_1
    tFileList_1 -->|ITERATE| tJava_2
    tFileList_1 -->|SUBJOB_OK| tParallelize_1
    tJava_2 -->|ITERATE| tFileInputDelimited_1
    tFileInputDelimited_1 -->|FLOW| tMap_1
    tFileInputDelimited_1 -->|ITERATE| tFileProperties_1
    tFileProperties_1 -->|FLOW| tJavaRow_1
    tMap_1 -->|FLOW| tFlowMeter_1
    tFlowMeter_1 -->|FLOW| tDBOutput_1
    tFileList_2 -->|ITERATE| tJava_3
    tFileList_2 -->|SUBJOB_OK| tFileList_3
    tJava_3 -->|ITERATE| tFileArchive_1
    tParallelize_1 -->|PARALLELIZE| tFileList_2
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tFileList_3 -->|ITERATE| tJava_4
    tJava_4 -->|ITERATE| tFileDelete_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
