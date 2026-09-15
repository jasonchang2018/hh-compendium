# Talend Job: cmi_renkim_ReturnHistory_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2024-11-06T10:21:21.321-0800
- **Last Modified**: 2025-09-29T21:40:53.679-0700

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
| 10 | tJava_2 | `tJava` | `CODE`=context.archiveDir = context.archiveDir + TalendDa, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 11 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 12 | tJava_3 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 13 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 14 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 15 | tJava_4 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 16 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=true, `FOLDER`=false |
| 17 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 18 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| RecordID | id_Integer | Yes | -1 |
| DateCreated | id_String | Yes | -1 |
| ReturnSource | id_String | Yes | -1 |
| UpdateCode | id_String | Yes | -1 |
| DebtorID | id_String | Yes | -1 |
| ID1 | id_String | Yes | -1 |
| LetterCode | id_String | Yes | -1 |
| OriginalName | id_String | Yes | -1 |
| OriginalAddress1 | id_String | Yes | -1 |
| OriginalAddress2 | id_String | Yes | -1 |
| OriginalCity | id_String | Yes | -1 |
| OriginalState | id_String | Yes | -1 |
| OriginalZip | id_String | Yes | -1 |
| MoveType | id_String | Yes | -1 |
| MoveFlag | id_String | Yes | -1 |
| EffectiveDate | id_String | Yes | -1 |
| NCOAAddress1 | id_String | Yes | -1 |
| NCOAAddress2 | id_String | Yes | -1 |
| NCOACity | id_String | Yes | -1 |
| NCOAState | id_String | Yes | -1 |
| NCOAZip | id_String | Yes | -1 |
| LetterAddress1 | id_String | Yes | -1 |
| LetterAddress2 | id_String | Yes | -1 |
| LetterCity | id_String | Yes | -1 |
| LetterState | id_String | Yes | -1 |
| LetterZip | id_String | Yes | -1 |
| eNoticeEmailAddress | id_String | Yes | -1 |
| eNoticeSecurityCode | id_String | Yes | -1 |
| eNoticeResponse | id_String | Yes | -1 |
| ReturnReason | id_String | Yes | -1 |
| DateProcessed | id_String | Yes | -1 |
| ProcessResult | id_String | Yes | -1 |
| PDF_URL | id_String | Yes | -1 |
| RecordID | id_Integer | Yes | -1 |
| DateCreated | id_String | Yes | -1 |
| ReturnSource | id_String | Yes | -1 |
| UpdateCode | id_String | Yes | -1 |
| DebtorID | id_String | Yes | -1 |
| ID1 | id_String | Yes | -1 |
| LetterCode | id_String | Yes | -1 |
| OriginalName | id_String | Yes | -1 |
| OriginalAddress1 | id_String | Yes | -1 |
| OriginalAddress2 | id_String | Yes | -1 |
| OriginalCity | id_String | Yes | -1 |
| OriginalState | id_String | Yes | -1 |
| OriginalZip | id_String | Yes | -1 |
| MoveType | id_String | Yes | -1 |
| MoveFlag | id_String | Yes | -1 |
| EffectiveDate | id_String | Yes | -1 |
| NCOAAddress1 | id_String | Yes | -1 |
| NCOAAddress2 | id_String | Yes | -1 |
| NCOACity | id_String | Yes | -1 |
| NCOAState | id_String | Yes | -1 |
| NCOAZip | id_String | Yes | -1 |
| LetterAddress1 | id_String | Yes | -1 |
| LetterAddress2 | id_String | Yes | -1 |
| LetterCity | id_String | Yes | -1 |
| LetterState | id_String | Yes | -1 |
| LetterZip | id_String | Yes | -1 |
| eNoticeEmailAddress | id_String | Yes | -1 |
| eNoticeSecurityCode | id_String | Yes | -1 |
| eNoticeResponse | id_String | Yes | -1 |
| ReturnReason | id_String | Yes | -1 |
| DateProcessed | id_String | Yes | -1 |
| ProcessResult | id_String | Yes | -1 |
| PDF_URL | id_String | Yes | -1 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| RECORDID | id_Integer | Yes | 38 |
| DATECREATED | id_String | Yes | 16777216 |
| RETURNSOURCE | id_String | Yes | 16777216 |
| UPDATECODE | id_String | Yes | 16777216 |
| DEBTORID | id_String | Yes | 16777216 |
| ID1 | id_String | Yes | 16777216 |
| LETTERCODE | id_String | Yes | 16777216 |
| ORIGINALNAME | id_String | Yes | 16777216 |
| ORIGINALADDRESS1 | id_String | Yes | 16777216 |
| ORIGINALADDRESS2 | id_String | Yes | 16777216 |
| ORIGINALCITY | id_String | Yes | 16777216 |
| ORIGINALSTATE | id_String | Yes | 16777216 |
| ORIGINALZIP | id_String | Yes | 16777216 |
| MOVETYPE | id_String | Yes | 16777216 |
| MOVEFLAG | id_String | Yes | 16777216 |
| EFFECTIVEDATE | id_String | Yes | 16777216 |
| NCOAADDRESS1 | id_String | Yes | 16777216 |
| NCOAADDRESS2 | id_String | Yes | 16777216 |
| NCOACITY | id_String | Yes | 16777216 |
| NCOASTATE | id_String | Yes | 16777216 |
| NCOAZIP | id_String | Yes | 16777216 |
| LETTERADDRESS1 | id_String | Yes | 16777216 |
| LETTERADDRESS2 | id_String | Yes | 16777216 |
| LETTERCITY | id_String | Yes | 16777216 |
| LETTERSTATE | id_String | Yes | 16777216 |
| LETTERZIP | id_String | Yes | 16777216 |
| ENOTICEEMAILADDRESS | id_String | Yes | 16777216 |
| ENOTICESECURITYCODE | id_String | Yes | 16777216 |
| ENOTICERESPONSE | id_String | Yes | 16777216 |
| RETURNREASON | id_String | Yes | 16777216 |
| DATEPROCESSED | id_String | Yes | 16777216 |
| PROCESSRESULT | id_String | Yes | 16777216 |
| PDF_URL | id_String | Yes | 16777216 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| RECORDID | id_Integer | Yes | 38 |
| DATECREATED | id_String | Yes | 16777216 |
| RETURNSOURCE | id_String | Yes | 16777216 |
| UPDATECODE | id_String | Yes | 16777216 |
| DEBTORID | id_String | Yes | 16777216 |
| ID1 | id_String | Yes | 16777216 |
| LETTERCODE | id_String | Yes | 16777216 |
| ORIGINALNAME | id_String | Yes | 16777216 |
| ORIGINALADDRESS1 | id_String | Yes | 16777216 |
| ORIGINALADDRESS2 | id_String | Yes | 16777216 |
| ORIGINALCITY | id_String | Yes | 16777216 |
| ORIGINALSTATE | id_String | Yes | 16777216 |
| ORIGINALZIP | id_String | Yes | 16777216 |
| MOVETYPE | id_String | Yes | 16777216 |
| MOVEFLAG | id_String | Yes | 16777216 |
| EFFECTIVEDATE | id_String | Yes | 16777216 |
| NCOAADDRESS1 | id_String | Yes | 16777216 |
| NCOAADDRESS2 | id_String | Yes | 16777216 |
| NCOACITY | id_String | Yes | 16777216 |
| NCOASTATE | id_String | Yes | 16777216 |
| NCOAZIP | id_String | Yes | 16777216 |
| LETTERADDRESS1 | id_String | Yes | 16777216 |
| LETTERADDRESS2 | id_String | Yes | 16777216 |
| LETTERCITY | id_String | Yes | 16777216 |
| LETTERSTATE | id_String | Yes | 16777216 |
| LETTERZIP | id_String | Yes | 16777216 |
| ENOTICEEMAILADDRESS | id_String | Yes | 16777216 |
| ENOTICESECURITYCODE | id_String | Yes | 16777216 |
| ENOTICERESPONSE | id_String | Yes | 16777216 |
| RETURNREASON | id_String | Yes | 16777216 |
| DATEPROCESSED | id_String | Yes | 16777216 |
| PROCESSRESULT | id_String | Yes | 16777216 |
| PDF_URL | id_String | Yes | 16777216 |
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
    tJava_2 -->|SUBJOB_OK| tSetKeystore_1
    tFileList_2 -->|ITERATE| tJava_3
    tFileList_2 -->|SUBJOB_OK| tFileList_3
    tJava_3 -->|ITERATE| tFileArchive_1
    tFileList_3 -->|ITERATE| tJava_4
    tJava_4 -->|ITERATE| tFileDelete_1
    tParallelize_1 -->|PARALLELIZE| tFileList_2
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
