# Talend Job: LW_Lurie_Focus_Attributes_Granular

## Overview

This job extracts a narrow, long-format (name/value pair) view of Lurie focus-attribute scores from a Snowflake view (`PUB_LWASHINGTON.LURIE_FOCUS_ATTRIBUTES_GRANULAR`) and writes them to `Lurie_Focus_Attributes_Granular_View.csv`. It is the Lurie counterpart to `LW_Delaware_Focus_Attributes_Granular` and `LW_HPS_Focus_Attributes_Granular`, structurally identical apart from the source view name and output filename.

## Detail table

| Field | Value |
|---|---|
| Job name | LW_Lurie_Focus_Attributes_Granular |
| Version | 0.1 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2024-07-09T11:46:25.132-0700 |
| Last Modified | 2025-11-16T20:12:45.323-0800 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` → `tJava_1` opens a per-run log file → on subjob-ok, `tSetKeystore_1` configures SSL → on subjob-ok, `tDBConnection_1` opens the Snowflake connection.

**Main flow (no explicit trigger link into it):** `tDBInput_1` runs `SELECT SCORE_NAME, SCORE_VALUE FROM PUB_LWASHINGTON.LURIE_FOCUS_ATTRIBUTES_GRANULAR;` → `tFlowMeter_1` counts rows → `tFileOutputDelimited_1` writes the result (with header, file recreated each run) to `context.outputDir+"Lurie_Focus_Attributes_Granular_View.csv"`.

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> OpenLog["tJava_1<br/>Open log file"] -->|OnSubjobOk| Keystore["tSetKeystore_1<br/>Configure SSL"] -->|OnSubjobOk| Connect["tDBConnection_1<br/>Open Snowflake connection"]

    Query["tDBInput_1<br/>SELECT SCORE_NAME, SCORE_VALUE<br/>FROM LURIE_FOCUS_ATTRIBUTES_GRANULAR"] --> FlowMeter["tFlowMeter_1<br/>Count rows"] --> Write["tFileOutputDelimited_1<br/>Write Lurie_Focus_Attributes_Granular_View.csv"]
```

## Settings tables

### Source: `tDBInput_1` (`tSnowflakeInput`)

| Setting | Value | What it means |
|---|---|---|
| Query | `SELECT SCORE_NAME, SCORE_VALUE FROM PUB_LWASHINGTON.LURIE_FOCUS_ATTRIBUTES_GRANULAR;` | Same 2-column long-format shape as the Delaware/HPS siblings. |

### Target: `tFileOutputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.outputDir+"Lurie_Focus_Attributes_Granular_View.csv"` | |
| APPEND / INCLUDEHEADER | `false` / `true` | |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none.
- **Context variables used:** `keystorePath`, `logDir`, `outputDir`.
- **Hardcoded paths:** `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE`.
- **Sibling comparison:** Identical structure to `LW_Delaware_Focus_Attributes_Granular` and `LW_HPS_Focus_Attributes_Granular`. This is the granular counterpart to `LW_Lurie_Focus_Attributes` and `LW_Lurie_Audit_Scorecard`.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tSnowflakeConnection` / `tSnowflakeInput` | Open a Snowflake connection and run a query against it. |
| `tFlowMeter` | Counts rows passing a point in the flow. |
| `tFileOutputDelimited` | Writes rows to a CSV file. |
| `tSetKeystore` | Configures SSL trust store/keystore for the Snowflake JDBC connection. |

## Issues observed

- **Same missing explicit trigger link** between the connection-setup subjob and the query subjob as the other Granular jobs in this batch.
- **No client/debtor/audit identifying columns**, same limitation as the Delaware and HPS siblings — see `LW_HPS_Focus_Attributes_Granular`'s doc for the cross-sibling source-view naming inconsistency this job is part of (`LURIE_FOCUS_ATTRIBUTES_GRANULAR`, no `_VIEW` suffix, unlike HPS's `..._GRANULAR_VIEW`).
