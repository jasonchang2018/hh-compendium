# Talend Job: Extract_DC_Hermes_Decile

## Overview

Extracts the DC-site "Hermes"/Equabli prediction decile assignment (logon, packet, debtor number, local/global score, treatment group, dialer group) from a Snowflake transformation table scoped to DC, and writes it to a dated CSV file. Part of the same per-site decile extract family as `Extract_CHI_Hermes_Decile`, `Extract_CO_Hermes_Decile`, and `Extract_HH_Hermes_Decile` — this one is internally consistent: its query, table name, and output filename all correctly reference `DC`.

## Detail table

| Field | Value |
|---|---|
| Job name | Extract_DC_Hermes_Decile |
| Version | 0.1 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2023-08-13T21:08:21.736-0700 |
| Last Modified | 2025-11-05T08:59:52.429-0800 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` → `tJava_1` opens a per-run log file → `tSetKeystore_1` configures SSL trust/keystore from `context.keystorePath` (passwords redacted) → `tDBConnection_1` opens the Snowflake connection.

**Main subjob:**

1. `tDBInput_1` runs `SELECT LOGON, PACKET, DEBTORNUMBER, PL_GROUP, "LOCAL", "GLOBAL", EQUABLI_TREATMENT_GROUP, DIALERGRP FROM MASTER_PREDICTION_SCORES_TRANSFORMATION_CUBS_DEBTOR_DC;` — a fixed, unfiltered read of the entire DC-scoped transformation table.
2. `tFileOutputDelimited_1` writes the result to `context.outputDir + "DC_HERMES_DECILE_" + <CCYYMMDD> + ".csv"` (comma-delimited, header included).

**Teardown subjob:** `tPostjob_1` → `tDBClose_1` closes the Snowflake connection.

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> OpenLog["tJava_1<br/>Open log file"] -->|OnSubjobOk| Keystore["tSetKeystore_1<br/>Configure SSL"] -->|OnSubjobOk| Connect["tDBConnection_1<br/>Open Snowflake connection"]

    Read["tDBInput_1<br/>SELECT ... FROM<br/>MASTER_PREDICTION_SCORES_TRANSFORMATION_CUBS_DEBTOR_DC"] -->|MAIN| Write["tFileOutputDelimited_1<br/>Write DC_HERMES_DECILE_&lt;date&gt;.csv"]

    Postjob["tPostjob_1"] --> Close["tDBClose_1<br/>Close Snowflake connection"]
```

## Settings tables

### Source: `tDBInput_1` (`tSnowflakeInput`)

| Setting | Value | What it means |
|---|---|---|
| Query | `SELECT LOGON, PACKET, DEBTORNUMBER, PL_GROUP, "LOCAL", "GLOBAL", EQUABLI_TREATMENT_GROUP, DIALERGRP FROM MASTER_PREDICTION_SCORES_TRANSFORMATION_CUBS_DEBTOR_DC;` | No `WHERE` clause — the source table is already scoped to DC by name; the entire table is exported every run. |

### Target: `tFileOutputDelimited_1`

| Setting | Value | What it means |
|---|---|---|
| FILENAME | `context.outputDir+"DC_HERMES_DECILE_"+TalendDate.getDate("CCYYMMDD")+".csv"` | Correctly labeled `DC_` — consistent with both the job name and the source table. |
| INCLUDEHEADER | `true` | CSV includes a header row. |

### SSL setup: `tSetKeystore_1`

| Setting | Value | What it means |
|---|---|---|
| SSL_TRUSTSERVER_TRUSTSTORE | `"C:/clientTrustStore.trustStore"` | Hardcoded local path, not `context`-driven — see Issues observed. |
| SSL_KEYSTORE | `context.keystorePath` | Client keystore path is context-driven, unlike the trust store above. |
| SSL_TRUSTSERVER_PASSWORD / SSL_KEYSTORE_PASSWORD / NEED_CLIENT_AUTH | `***REDACTED***` | Preserved as redacted. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none — no `tRunJob` links found.
- **Context variables used:** `keystorePath`, `logDir`, `outputDir`.
- **1 hardcoded path finding:** `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE` = `"C:/clientTrustStore.trustStore"` — identical across the whole `*_Hermes_Decile` family.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tSetKeystore` | Configures SSL/TLS trust and client keystore settings for secure connections made later in the job. |
| `tSnowflakeConnection` / `tSnowflakeClose` | Open/close the Snowflake connection shared by other components. |
| `tSnowflakeInput` | Runs a query against Snowflake and returns its result rows. |
| `tFileOutputDelimited` | Writes rows to a delimited (CSV-style) text file. |

## Issues observed

- **This job is one of a near-identical family** (`Extract_CHI_Hermes_Decile`, `Extract_CO_Hermes_Decile`, `Extract_DC_Hermes_Decile`, `Extract_HH_Hermes_Decile`), sharing the same component structure, SSL setup, and query shape, differing only in the site-code suffix on the source table and the output filename prefix. **This one is internally consistent** — job name, query table (`..._DC`), and output filename (`DC_HERMES_DECILE_...`) all agree. This is notably different from the `Extract_No_Dialer_Test_*` family, where the CHI- and DC-named jobs have their site codes swapped internally (see those jobs' docs) — the "Decile" family does not have that bug.
- **The query has no `WHERE` clause and no incremental filter** — every run exports the entire `MASTER_PREDICTION_SCORES_TRANSFORMATION_CUBS_DEBTOR_DC` table. Presumably a full daily snapshot by design.
- **`SSL_TRUSTSERVER_TRUSTSTORE` is a hardcoded local path** rather than `context`-driven like the paired `SSL_KEYSTORE` — inconsistent within the same component, and a minor portability risk.
- **No error/row-count logging or reject handling** — no `tWarn`/`tDie`/`tSendMail`; a failed extract would only surface as a generic Talend execution error.
