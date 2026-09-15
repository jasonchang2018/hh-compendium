# Talend Job: ScheduledPayment_Text_Load

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2025-07-01T10:41:45.613-0700
- **Last Modified**: 2025-10-02T10:50:11.984-0700

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
| 8 | tMap_1 | `tMap` | `LINK_STYLE`=AUTO, `DIE_ON_ERROR`=true, `LKUP_PARALLELIZE`=false, `LEVENSHTEIN`=0, `JACCARD`=0 |
| 9 | tFlowMeter_2 | `tFlowMeter` | `USEROWLABEL`=true, `METTERLABEL`="MyLabel", `ABSOLUTE`=Absolute, `CONNECTION_FORMAT`=row |
| 10 | tDBOutput_1 | `tSnowflakeOutput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 11 | tParallelize_1 | `tParallelize` | `WAIT_FOR`=All, `SLEEPTIME`=100, `DIE_ON_ERROR`=false, `CONNECTION_FORMAT`=row |
| 12 | tDBRow_2 | `tSnowflakeRow` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":3,"@type":"org.talend.components.snowflake. |
| 13 | tFileList_2 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 14 | tJava_3 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 15 | tFileArchive_1 | `tFileArchive` | `SOURCE`=context.sourceDir, `SOURCE_FILE`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s, `SUB_DIRECTROY`=false, `TARGET`=context.archiveDir + context.fileName+".zip", `MKDIR`=true |
| 16 | tFileList_3 | `tFileList` | `DIRECTORY`=context.sourceDir, `LIST_MODE`=FILES, `INCLUDSUBDIR`=false, `CASE_SENSITIVE`=YES, `ERROR`=false |
| 17 | tJava_4 | `tJava` | `CODE`=context.filePath = ((String)globalMap.get("tFileLi, `IMPORT`=//import java.util.List;, `CONNECTION_FORMAT`=row |
| 18 | tSleep_1 | `tSleep` | `PAUSE`=5, `CONNECTION_FORMAT`=row |
| 19 | tFileDelete_1 | `tFileDelete` | `FILENAME`=context.filePath, `DIRECTORY`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `PATH`="C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d, `FAILON`=false, `FOLDER`=false |
| 20 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tDBRow_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| errorCode | id_String | No | 255 |
| errorMessage | id_String | No | 255 |

### tFileInputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| ID | id_Integer | No | 38 |
| ACCOUNTID | id_Integer | No | 38 |
| DEBTORID | id_Integer | No | 38 |
| TYPE | id_String | No | 14 |
| PAYMENTVENDORTOKENID | id_Integer | Yes | 38 |
| WALLETID | id_Integer | Yes | 38 |
| ARRANGEMENTID | id_Integer | Yes | 38 |
| ISEXTERNALLYMANAGED | id_Integer | No | 38 |
| PAYMENTLINKUID | id_Integer | Yes | 38 |
| STATUS | id_String | No | 14 |
| TRANSACTIONSTATUS | id_String | Yes | 14 |
| TRANSACTIONLOCK | id_String | Yes | 72 |
| TRANSACTIONSTART | id_String | Yes | 30 |
| AMOUNT | id_String | No | 30 |
| SURCHARGE | id_String | No | 30 |
| WHEN | id_String | No | 30 |
| COLLECTORFEE | id_String | Yes | 30 |
| PROJECTEDFEE | id_String | Yes | 30 |
| USEPROJECTEDFEE | id_Integer | No | 38 |
| DEPOSITTOGENERALTRUST | id_Integer | No | 38 |
| DEPOSITSURCHARGETOOPERATINGTRUST | id_Integer | No | 38 |
| ENTEREDWHEN | id_String | No | 30 |
| ENTEREDBY | id_String | No | 20 |
| UPDATEDWHEN | id_String | No | 30 |
| UPDATEDBY | id_String | No | 20 |
| EXECUTEDWHEN | id_String | Yes | 30 |
| EXECUTEDBY | id_String | Yes | 20 |
| ONHOLDWHEN | id_String | Yes | 30 |
| ONHOLDBY | id_String | Yes | 20 |
| APPROVEDWHEN | id_String | Yes | 30 |
| APPROVEDBY | id_String | Yes | 20 |
| BATCHED | id_String | Yes | 30 |
| BOUNCED | id_String | Yes | 30 |
| BOUNCECOUNT | id_Integer | No | 38 |
| EXECUTERESULTDETAIL | id_String | Yes | 250 |
| BOUNCERESULTDETAIL | id_String | Yes | 250 |
| PAYMENTMETHODID | id_Integer | No | 38 |
| NITDSENDDATE | id_String | Yes | 30 |
| SENDRM | id_Integer | No | 38 |
| LETTERCODE | id_String | Yes | 5 |
| RMSENTDATE | id_String | Yes | 30 |
| CUSTOMER | id_String | No | 7 |
| ID | id_Integer | No | 38 |
| ACCOUNTID | id_Integer | No | 38 |
| DEBTORID | id_Integer | No | 38 |
| TYPE | id_String | No | 14 |
| PAYMENTVENDORTOKENID | id_Integer | Yes | 38 |
| WALLETID | id_Integer | Yes | 38 |
| ARRANGEMENTID | id_Integer | Yes | 38 |
| ISEXTERNALLYMANAGED | id_Integer | No | 38 |
| PAYMENTLINKUID | id_Integer | Yes | 38 |
| STATUS | id_String | No | 14 |
| TRANSACTIONSTATUS | id_String | Yes | 14 |
| TRANSACTIONLOCK | id_String | Yes | 72 |
| TRANSACTIONSTART | id_String | Yes | 30 |
| AMOUNT | id_String | No | 30 |
| SURCHARGE | id_String | No | 30 |
| WHEN | id_String | No | 30 |
| COLLECTORFEE | id_String | Yes | 30 |
| PROJECTEDFEE | id_String | Yes | 30 |
| USEPROJECTEDFEE | id_Integer | No | 38 |
| DEPOSITTOGENERALTRUST | id_Integer | No | 38 |
| DEPOSITSURCHARGETOOPERATINGTRUST | id_Integer | No | 38 |
| ENTEREDWHEN | id_String | No | 30 |
| ENTEREDBY | id_String | No | 20 |
| UPDATEDWHEN | id_String | No | 30 |
| UPDATEDBY | id_String | No | 20 |
| EXECUTEDWHEN | id_String | Yes | 30 |
| EXECUTEDBY | id_String | Yes | 20 |
| ONHOLDWHEN | id_String | Yes | 30 |
| ONHOLDBY | id_String | Yes | 20 |
| APPROVEDWHEN | id_String | Yes | 30 |
| APPROVEDBY | id_String | Yes | 20 |
| BATCHED | id_String | Yes | 30 |
| BOUNCED | id_String | Yes | 30 |
| BOUNCECOUNT | id_Integer | No | 38 |
| EXECUTERESULTDETAIL | id_String | Yes | 250 |
| BOUNCERESULTDETAIL | id_String | Yes | 250 |
| PAYMENTMETHODID | id_Integer | No | 38 |
| NITDSENDDATE | id_String | Yes | 30 |
| SENDRM | id_Integer | No | 38 |
| LETTERCODE | id_String | Yes | 5 |
| RMSENTDATE | id_String | Yes | 30 |
| CUSTOMER | id_String | No | 7 |
| errorCode | id_String | Yes | 255 |
| errorMessage | id_String | Yes | 255 |

### tMap_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_Integer | No | 38 |
| ACCOUNTID | id_Integer | No | 38 |
| DEBTORID | id_Integer | No | 38 |
| TYPE | id_String | No | 14 |
| PAYMENTVENDORTOKENID | id_Integer | Yes | 38 |
| WALLETID | id_Integer | Yes | 38 |
| ARRANGEMENTID | id_Integer | Yes | 38 |
| ISEXTERNALLYMANAGED | id_Integer | No | 38 |
| PAYMENTLINKUID | id_Integer | Yes | 38 |
| STATUS | id_String | No | 14 |
| TRANSACTIONSTATUS | id_String | Yes | 14 |
| TRANSACTIONLOCK | id_String | Yes | 72 |
| TRANSACTIONSTART | id_String | Yes | 30 |
| AMOUNT | id_String | No | 30 |
| SURCHARGE | id_String | No | 30 |
| WHEN | id_String | No | 30 |
| COLLECTORFEE | id_String | Yes | 30 |
| PROJECTEDFEE | id_String | Yes | 30 |
| USEPROJECTEDFEE | id_Integer | No | 38 |
| DEPOSITTOGENERALTRUST | id_Integer | No | 38 |
| DEPOSITSURCHARGETOOPERATINGTRUST | id_Integer | No | 38 |
| ENTEREDWHEN | id_String | No | 30 |
| ENTEREDBY | id_String | No | 20 |
| UPDATEDWHEN | id_String | No | 30 |
| UPDATEDBY | id_String | No | 20 |
| EXECUTEDWHEN | id_String | Yes | 30 |
| EXECUTEDBY | id_String | Yes | 20 |
| ONHOLDWHEN | id_String | Yes | 30 |
| ONHOLDBY | id_String | Yes | 20 |
| APPROVEDWHEN | id_String | Yes | 30 |
| APPROVEDBY | id_String | Yes | 20 |
| BATCHED | id_String | Yes | 30 |
| BOUNCED | id_String | Yes | 30 |
| BOUNCECOUNT | id_Integer | No | 38 |
| EXECUTERESULTDETAIL | id_String | Yes | 250 |
| BOUNCERESULTDETAIL | id_String | Yes | 250 |
| PAYMENTMETHODID | id_Integer | No | 38 |
| NITDSENDDATE | id_String | Yes | 30 |
| SENDRM | id_Integer | No | 38 |
| LETTERCODE | id_String | Yes | 5 |
| RMSENTDATE | id_String | Yes | 30 |
| CUSTOMER | id_String | No | 7 |

### tFlowMeter_2

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_Integer | No | 38 |
| ACCOUNTID | id_Integer | No | 38 |
| DEBTORID | id_Integer | No | 38 |
| TYPE | id_String | No | 14 |
| PAYMENTVENDORTOKENID | id_Integer | Yes | 38 |
| WALLETID | id_Integer | Yes | 38 |
| ARRANGEMENTID | id_Integer | Yes | 38 |
| ISEXTERNALLYMANAGED | id_Integer | No | 38 |
| PAYMENTLINKUID | id_Integer | Yes | 38 |
| STATUS | id_String | No | 14 |
| TRANSACTIONSTATUS | id_String | Yes | 14 |
| TRANSACTIONLOCK | id_String | Yes | 72 |
| TRANSACTIONSTART | id_String | Yes | 30 |
| AMOUNT | id_String | No | 30 |
| SURCHARGE | id_String | No | 30 |
| WHEN | id_String | No | 30 |
| COLLECTORFEE | id_String | Yes | 30 |
| PROJECTEDFEE | id_String | Yes | 30 |
| USEPROJECTEDFEE | id_Integer | No | 38 |
| DEPOSITTOGENERALTRUST | id_Integer | No | 38 |
| DEPOSITSURCHARGETOOPERATINGTRUST | id_Integer | No | 38 |
| ENTEREDWHEN | id_String | No | 30 |
| ENTEREDBY | id_String | No | 20 |
| UPDATEDWHEN | id_String | No | 30 |
| UPDATEDBY | id_String | No | 20 |
| EXECUTEDWHEN | id_String | Yes | 30 |
| EXECUTEDBY | id_String | Yes | 20 |
| ONHOLDWHEN | id_String | Yes | 30 |
| ONHOLDBY | id_String | Yes | 20 |
| APPROVEDWHEN | id_String | Yes | 30 |
| APPROVEDBY | id_String | Yes | 20 |
| BATCHED | id_String | Yes | 30 |
| BOUNCED | id_String | Yes | 30 |
| BOUNCECOUNT | id_Integer | No | 38 |
| EXECUTERESULTDETAIL | id_String | Yes | 250 |
| BOUNCERESULTDETAIL | id_String | Yes | 250 |
| PAYMENTMETHODID | id_Integer | No | 38 |
| NITDSENDDATE | id_String | Yes | 30 |
| SENDRM | id_Integer | No | 38 |
| LETTERCODE | id_String | Yes | 5 |
| RMSENTDATE | id_String | Yes | 30 |
| CUSTOMER | id_String | No | 7 |

### tDBOutput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| LOAD_DT | id_Date | Yes | -1 |
| ID | id_Integer | No | 38 |
| ACCOUNTID | id_Integer | No | 38 |
| DEBTORID | id_Integer | No | 38 |
| TYPE | id_String | No | 14 |
| PAYMENTVENDORTOKENID | id_Integer | Yes | 38 |
| WALLETID | id_Integer | Yes | 38 |
| ARRANGEMENTID | id_Integer | Yes | 38 |
| ISEXTERNALLYMANAGED | id_Integer | No | 38 |
| PAYMENTLINKUID | id_Integer | Yes | 38 |
| STATUS | id_String | No | 14 |
| TRANSACTIONSTATUS | id_String | Yes | 14 |
| TRANSACTIONLOCK | id_String | Yes | 72 |
| TRANSACTIONSTART | id_String | Yes | 30 |
| AMOUNT | id_String | No | 30 |
| SURCHARGE | id_String | No | 30 |
| WHEN | id_String | No | 30 |
| COLLECTORFEE | id_String | Yes | 30 |
| PROJECTEDFEE | id_String | Yes | 30 |
| USEPROJECTEDFEE | id_Integer | No | 38 |
| DEPOSITTOGENERALTRUST | id_Integer | No | 38 |
| DEPOSITSURCHARGETOOPERATINGTRUST | id_Integer | No | 38 |
| ENTEREDWHEN | id_String | No | 30 |
| ENTEREDBY | id_String | No | 20 |
| UPDATEDWHEN | id_String | No | 30 |
| UPDATEDBY | id_String | No | 20 |
| EXECUTEDWHEN | id_String | Yes | 30 |
| EXECUTEDBY | id_String | Yes | 20 |
| ONHOLDWHEN | id_String | Yes | 30 |
| ONHOLDBY | id_String | Yes | 20 |
| APPROVEDWHEN | id_String | Yes | 30 |
| APPROVEDBY | id_String | Yes | 20 |
| BATCHED | id_String | Yes | 30 |
| BOUNCED | id_String | Yes | 30 |
| BOUNCECOUNT | id_Integer | No | 38 |
| EXECUTERESULTDETAIL | id_String | Yes | 250 |
| BOUNCERESULTDETAIL | id_String | Yes | 250 |
| PAYMENTMETHODID | id_Integer | No | 38 |
| NITDSENDDATE | id_String | Yes | 30 |
| SENDRM | id_Integer | No | 38 |
| LETTERCODE | id_String | Yes | 5 |
| RMSENTDATE | id_String | Yes | 30 |
| CUSTOMER | id_String | No | 7 |
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
    tMap_1 -->|FLOW| tFlowMeter_2
    tFlowMeter_2 -->|FLOW| tDBOutput_1
    tParallelize_1 -->|PARALLELIZE| tFileList_2
    tParallelize_1 -->|PARALLELIZE| tDBRow_2
    tFileList_2 -->|ITERATE| tJava_3
    tFileList_2 -->|SUBJOB_OK| tFileList_3
    tJava_3 -->|ITERATE| tFileArchive_1
    tFileList_3 -->|ITERATE| tJava_4
    tJava_4 -->|ITERATE| tSleep_1
    tSleep_1 -->|ITERATE| tFileDelete_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBConnection_1
```
