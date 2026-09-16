# Talend Job: Hermes_Latitude_Recommendations

- **Project**: LATITUDE
- **Version**: 0.1
- **Job Type**: Standard

- **Author**: jmach@harriscollect.com
- **Created**: 2025-03-26T09:18:27.296-0700
- **Last Modified**: 2026-02-05T12:12:45.917-0800

## Components

| # | Component | Type | Key Parameters |
|---|-----------|------|----------------|
| 1 | tDBInput_1 | `tSnowflakeInput` | `CONNECTION_FORMAT`=row, `PROPERTIES`={"@id":4,"@type":"org.talend.components.snowflake. |
| 2 | tFileOutputDelimited_1 | `tFileOutputDelimited` | `USESTREAM`=false, `STREAMNAME`=outputStream, `FILENAME`=context.outputDir + "master_prediction_proposal_la, `ROWSEPARATOR`="\n", `OS_LINE_SEPARATOR_AS_ROW_SEPARATOR`=true |
| 3 | tSetKeystore_1 | `tSetKeystore` | `SET_TRUSTSTORE`=false, `SET_TRUSTSTORE_KEYSTORE`=false, `TRUSTSTORE_TYPE`=JKS, `SSL_TRUSTSERVER_TRUSTSTORE`="C:/clientTrustStore.trustStore", `KEYSTORE_TYPE`=PKCS12 |

## Schemas

### tDBInput_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| NUMBER | id_String | Yes | 50 |
| PROPOSED_CHANNEL | id_String | Yes | 16777216 |
| TEMPLATE | id_String | Yes | 134217728 |
| PHONE_NUMBER | id_String | Yes | 134217728 |
| SUBTEAM | id_String | Yes | 16777216 |
| TEXT_TYPE | id_String | Yes | 16777216 |
| SETTLEMENT_AMT | id_String | Yes | 16777216 |
| VOAPPS_TARGET_DATE | id_String | Yes | 134217728 |
| VOAPPS_CALLER_NUMBER | id_String | Yes | 134217728 |
| VOAPPS_MESSAGE_ID | id_String | Yes | 134217728 |
| VOAPPS_ZIP_CODE | id_String | Yes | 134217728 |
| VOAPPS_VOICE_APPEND | id_String | Yes | 134217728 |
| HERMES_REQUEST_ID | id_String | Yes | 16777216 |

### tFileOutputDelimited_1

| Column | Type | Nullable | Length |
|--------|------|----------|--------|
| NUMBER | id_String | Yes | 50 |
| PROPOSED_CHANNEL | id_String | Yes | 16777216 |
| TEMPLATE | id_String | Yes | 134217728 |
| PHONE_NUMBER | id_String | Yes | 134217728 |
| SUBTEAM | id_String | Yes | 16777216 |
| TEXT_TYPE | id_String | Yes | 16777216 |
| SETTLEMENT_AMT | id_String | Yes | 16777216 |
| VOAPPS_TARGET_DATE | id_String | Yes | 134217728 |
| VOAPPS_CALLER_NUMBER | id_String | Yes | 134217728 |
| VOAPPS_MESSAGE_ID | id_String | Yes | 134217728 |
| VOAPPS_ZIP_CODE | id_String | Yes | 134217728 |
| VOAPPS_VOICE_APPEND | id_String | Yes | 134217728 |
| HERMES_REQUEST_ID | id_String | Yes | 16777216 |

## Data Flow

```mermaid
graph LR
    tDBInput_1 -->|MAIN| tFileOutputDelimited_1
    tSetKeystore_1 -->|SUBJOB_OK| tDBInput_1
```
