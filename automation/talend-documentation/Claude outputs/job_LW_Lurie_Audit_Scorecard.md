# Talend Job: LW_Lurie_Audit_Scorecard

## Overview

This job extracts a per-call audit scorecard for the Lurie client relationship — collector name, call/audit dates, overall score, 7 category percentage scores, the 32 underlying pass/fail attribute flags, and free-text summary columns — from a Snowflake view (`PUB_LWASHINGTON.LURIE_AUDIT_SCORECARD_REPORT`) and writes the full result to `Lurie_Audit_Scorecard_Report.csv`. It is structurally and column-for-column identical to `LW_Deleware_Audit_Scorecard` and `LW_HPS_Audit_Scorecard`, differing only in source view and output filename.

## Detail table

| Field | Value |
|---|---|
| Job name | LW_Lurie_Audit_Scorecard |
| Version | 0.1 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2024-07-09T11:17:34.434-0700 |
| Last Modified | 2025-11-16T20:12:02.820-0800 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` → `tJava_1` opens a per-run log file → on subjob-ok, `tSetKeystore_1` configures SSL → on subjob-ok, `tDBConnection_1` opens the Snowflake connection.

**Main flow (no explicit trigger link into it):** `tDBInput_1` runs the 46-column query below → `tFlowMeter_1` counts rows → `tFileOutputDelimited_1` writes the result (with header, file recreated each run) to `context.outputDir+"Lurie_Audit_Scorecard_Report.csv"`.

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> OpenLog["tJava_1<br/>Open log file"] -->|OnSubjobOk| Keystore["tSetKeystore_1<br/>Configure SSL"] -->|OnSubjobOk| Connect["tDBConnection_1<br/>Open Snowflake connection"]

    Query["tDBInput_1<br/>SELECT scorecard columns<br/>FROM LURIE_AUDIT_SCORECARD_REPORT"] --> FlowMeter["tFlowMeter_1<br/>Count rows"] --> Write["tFileOutputDelimited_1<br/>Write Lurie_Audit_Scorecard_Report.csv"]
```

## Settings tables

### Source: `tDBInput_1` (`tSnowflakeInput`)

| Setting | Value | What it means |
|---|---|---|
| Query | `SELECT COLLECTOR_NAME, "CALL DATE", "AUDIT DATE", "OVERALL SCORE", OPENING_SCORE_PCT, ... ACTION_CODE, ACC_DOCUMENTATION, "AREA OF OPPORTUNITY", COMPLIANCE_STATUS FROM PUB_LWASHINGTON.LURIE_AUDIT_SCORECARD_REPORT;` (same 46-column list as the Delaware/HPS siblings) | Identical shape; only `LURIE_AUDIT_SCORECARD_REPORT` differs as the source view. Note the source view name here already includes "SCORECARD" in it, unlike Delaware's `DELAWARE_AUDIT_REPORT` and HPS's `HPS_AUDIT_REPORT` — a minor naming-convention difference across the three, though not a functional one. |

### Target: `tFileOutputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.outputDir+"Lurie_Audit_Scorecard_Report.csv"` | |
| APPEND / INCLUDEHEADER | `false` / `true` | |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none.
- **Context variables used:** `keystorePath`, `logDir`, `outputDir`.
- **Hardcoded paths:** `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE`.
- **Sibling comparison:** Identical structure to `LW_Deleware_Audit_Scorecard` and `LW_HPS_Audit_Scorecard`. This is the per-call detail counterpart to `LW_Lurie_Focus_Attributes` and `LW_Lurie_Focus_Attributes_Granular`.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tSnowflakeConnection` / `tSnowflakeInput` | Open a Snowflake connection and run a query against it. |
| `tFlowMeter` | Counts rows passing a point in the flow. |
| `tFileOutputDelimited` | Writes rows to a CSV file. |
| `tSetKeystore` | Configures SSL trust store/keystore for the Snowflake JDBC connection. |

## Issues observed

- **Same missing explicit trigger link** between the connection-setup subjob and the query subjob as the rest of this batch.
- **No email/notification and no debtor/account identifier**, same as the Delaware and HPS siblings.
- **Source view naming already embeds "SCORECARD"** (`LURIE_AUDIT_SCORECARD_REPORT`), unlike Delaware's `DELAWARE_AUDIT_REPORT` and HPS's `HPS_AUDIT_REPORT` — worth noting for anyone reconciling view names against job names across the three sibling jobs, though it has no functional effect.
