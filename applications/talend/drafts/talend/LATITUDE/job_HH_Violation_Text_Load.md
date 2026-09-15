# Talend Job: HH_Violation_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2025-09-26T10:02:04.422-0700
- **Last Modified**: 2026-07-29T09:26:05.042-0700

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
| 22 | tFileCopy_1 | `tFileCopy` | `FILENAME`=context.filePath, `ENABLE_COPY_DIRECTORY`=false, `SOURCE_DERECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace", `DESTINATION`=context.badFileDir, `RENAME`=false |
| 23 | tDie_2 | `tDie` | `MESSAGE`="File parsing error: " + ((String)globalMap.get("t, `CODE`=4, `PRIORITY`=5, `EXIT_JVM`=false, `CONNECTION_FORMAT`=row |

## Schemas

### tDBRow_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| VIOLATIONID | id_BigDecimal | No | 38 |
| ACCOUNTID | id_BigDecimal | No | 38 |
| VIOLATIONDATETIME | id_String | Yes | 30 |
| TOLLWAY | id_String | Yes | 20 |
| ENTRYLANE | id_String | Yes | 20 |
| TURNPIKE | id_String | Yes | 20 |
| PLAZA | id_String | Yes | 20 |
| LANE | id_String | Yes | 20 |
| _CLASS | id_String | Yes | 50 |
| LOCATIONDESC | id_String | Yes | 50 |
| POSTEDSPEED | id_String | Yes | 4 |
| RECORDEDSPEED | id_String | Yes | 4 |
| VIOLATIONDESC | id_String | Yes | 50 |
| VIOLATIONREF | id_String | Yes | 50 |
| VIOLATIONTYPE | id_String | Yes | 50 |
| VIOLATIONNUMBER | id_String | Yes | 25 |
| STATEMENTID | id_String | Yes | 25 |
| PLATENUMBER | id_String | Yes | 10 |
| PLATESTATE | id_String | Yes | 4 |
| PLATECITY | id_String | Yes | 25 |
| VEHICLEYEAR | id_String | Yes | 4 |
| VEHICLEMAKE | id_String | Yes | 20 |
| VEHICLEVIN | id_String | Yes | 20 |
| VEHICLEMODEL | id_String | Yes | 50 |
| VIOLATIONID | id_BigDecimal | No | 38 |
| ACCOUNTID | id_BigDecimal | No | 38 |
| VIOLATIONDATETIME | id_String | Yes | 30 |
| TOLLWAY | id_String | Yes | 20 |
| ENTRYLANE | id_String | Yes | 20 |
| TURNPIKE | id_String | Yes | 20 |
| PLAZA | id_String | Yes | 20 |
| LANE | id_String | Yes | 20 |
| _CLASS | id_String | Yes | 50 |
| LOCATIONDESC | id_String | Yes | 50 |
| POSTEDSPEED | id_String | Yes | 4 |
| RECORDEDSPEED | id_String | Yes | 4 |
| VIOLATIONDESC | id_String | Yes | 50 |
| VIOLATIONREF | id_String | Yes | 50 |
| VIOLATIONTYPE | id_String | Yes | 50 |
| VIOLATIONNUMBER | id_String | Yes | 25 |
| STATEMENTID | id_String | Yes | 25 |
| PLATENUMBER | id_String | Yes | 10 |
| PLATESTATE | id_String | Yes | 4 |
| PLATECITY | id_String | Yes | 25 |
| VEHICLEYEAR | id_String | Yes | 4 |
| VEHICLEMAKE | id_String | Yes | 20 |
| VEHICLEVIN | id_String | Yes | 20 |
| VEHICLEMODEL | id_String | Yes | 50 |
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
| LASTMODIFIED | id_BigDecimal | Yes | 38 |
| VIOLATIONID | id_BigDecimal | No | 38 |
| ACCOUNTID | id_BigDecimal | No | 38 |
| VIOLATIONDATETIME | id_String | Yes | 30 |
| TOLLWAY | id_String | Yes | 20 |
| ENTRYLANE | id_String | Yes | 20 |
| TURNPIKE | id_String | Yes | 20 |
| PLAZA | id_String | Yes | 20 |
| LANE | id_String | Yes | 20 |
| _CLASS | id_String | Yes | 50 |
| LOCATIONDESC | id_String | Yes | 50 |
| POSTEDSPEED | id_String | Yes | 4 |
| RECORDEDSPEED | id_String | Yes | 4 |
| VIOLATIONDESC | id_String | Yes | 50 |
| VIOLATIONREF | id_String | Yes | 50 |
| VIOLATIONTYPE | id_String | Yes | 50 |
| VIOLATIONNUMBER | id_String | Yes | 25 |
| STATEMENTID | id_String | Yes | 25 |
| PLATENUMBER | id_String | Yes | 10 |
| PLATESTATE | id_String | Yes | 4 |
| PLATECITY | id_String | Yes | 25 |
| VEHICLEYEAR | id_String | Yes | 4 |
| VEHICLEMAKE | id_String | Yes | 20 |
| VEHICLEVIN | id_String | Yes | 20 |
| VEHICLEMODEL | id_String | Yes | 50 |

### tFlowMeter_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| LASTMODIFIED | id_BigDecimal | Yes | 38 |
| VIOLATIONID | id_BigDecimal | No | 38 |
| ACCOUNTID | id_BigDecimal | No | 38 |
| VIOLATIONDATETIME | id_String | Yes | 30 |
| TOLLWAY | id_String | Yes | 20 |
| ENTRYLANE | id_String | Yes | 20 |
| TURNPIKE | id_String | Yes | 20 |
| PLAZA | id_String | Yes | 20 |
| LANE | id_String | Yes | 20 |
| _CLASS | id_String | Yes | 50 |
| LOCATIONDESC | id_String | Yes | 50 |
| POSTEDSPEED | id_String | Yes | 4 |
| RECORDEDSPEED | id_String | Yes | 4 |
| VIOLATIONDESC | id_String | Yes | 50 |
| VIOLATIONREF | id_String | Yes | 50 |
| VIOLATIONTYPE | id_String | Yes | 50 |
| VIOLATIONNUMBER | id_String | Yes | 25 |
| STATEMENTID | id_String | Yes | 25 |
| PLATENUMBER | id_String | Yes | 10 |
| PLATESTATE | id_String | Yes | 4 |
| PLATECITY | id_String | Yes | 25 |
| VEHICLEYEAR | id_String | Yes | 4 |
| VEHICLEMAKE | id_String | Yes | 20 |
| VEHICLEVIN | id_String | Yes | 20 |
| VEHICLEMODEL | id_String | Yes | 50 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| LASTMODIFIED | id_BigDecimal | Yes | 38 |
| VIOLATIONID | id_BigDecimal | No | 38 |
| ACCOUNTID | id_BigDecimal | No | 38 |
| VIOLATIONDATETIME | id_String | Yes | 30 |
| TOLLWAY | id_String | Yes | 20 |
| ENTRYLANE | id_String | Yes | 20 |
| TURNPIKE | id_String | Yes | 20 |
| PLAZA | id_String | Yes | 20 |
| LANE | id_String | Yes | 20 |
| _CLASS | id_String | Yes | 50 |
| LOCATIONDESC | id_String | Yes | 50 |
| POSTEDSPEED | id_String | Yes | 4 |
| RECORDEDSPEED | id_String | Yes | 4 |
| VIOLATIONDESC | id_String | Yes | 50 |
| VIOLATIONREF | id_String | Yes | 50 |
| VIOLATIONTYPE | id_String | Yes | 50 |
| VIOLATIONNUMBER | id_String | Yes | 25 |
| STATEMENTID | id_String | Yes | 25 |
| PLATENUMBER | id_String | Yes | 10 |
| PLATESTATE | id_String | Yes | 4 |
| PLATECITY | id_String | Yes | 25 |
| VEHICLEYEAR | id_String | Yes | 4 |
| VEHICLEMAKE | id_String | Yes | 20 |
| VEHICLEVIN | id_String | Yes | 20 |
| VEHICLEMODEL | id_String | Yes | 50 |
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
    tDBConnection_1 -->|SUBJOB_OK| tJava_1
    tPrejob_1 -->|COMPONENT_OK| tSetKeystore_1
    tDBRow_1 -->|SUBJOB_OK| tFileList_1
    tFileList_1 -->|ITERATE| tJava_2
    tFileList_1 -->|SUBJOB_OK| tParallelize_1
    tJava_2 -->|ITERATE| tFileInputDelimited_1
    tFileInputDelimited_1 -->|FLOW| tMap_1
    tFileInputDelimited_1 -->|ITERATE| tFileProperties_1
    tFileInputDelimited_1 -->|COMPONENT_ERROR| tFileCopy_1
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
    tFileCopy_1 -->|SUBJOB_OK| tDie_2
```
