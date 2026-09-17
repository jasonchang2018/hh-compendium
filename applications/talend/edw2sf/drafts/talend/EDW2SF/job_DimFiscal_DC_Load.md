# Talend Job: DimFiscal_DC_Load

## Overview

A merge-only orchestrator for the "DC" site's fiscal/patient-billing dimension: it runs three Snowflake stored-procedure merges (`DIMFISCAL_DC_A`, `_B`, `_C`) in parallel to fold previously-staged DC fiscal data into its final tables. Functionally identical to `DimFiscal_CO_Load` and `DimFiscal_TOL_Load` (same three merge sub-tables), differing only in the site-specific procedure names and a cosmetic difference in wiring order (see Issues observed).

## Detail table

| Field | Value |
|---|---|
| Job name | DimFiscal_DC_Load |
| Version | 0.1 |
| Project | EDW2SF |
| Author | jmach@harriscollect.com |
| Created | 2022-08-02T09:27:21.839-0700 |
| Last Modified | 2025-11-04T11:08:09.761-0800 |

## Step-by-step data flow

**Setup subjob:** `tPrejob_1` → `tJava_1` opens a per-run log file → on subjob success, `tSetKeystore_1` configures SSL trust/keystore → on subjob success, `tDBConnection_1` opens the Snowflake connection.

**Main subjob:** `tParallelize_1` runs three branches at the same time (in this job, wired as `tDBRow_2` first, then `tDBRow_1`, then `tDBRow_3` — order has no practical effect since all three run in parallel regardless):
1. `tDBRow_2` runs `CALL STAGING.MERGE_INTO_DIMFISCAL_DC_A();`
2. `tDBRow_1` runs `CALL STAGING.MERGE_INTO_DIMFISCAL_DC_B();`
3. `tDBRow_3` runs `CALL STAGING.MERGE_INTO_DIMFISCAL_DC_C();`

No result-code checking is wired on any of the three merges.

**Teardown subjob:** `tPostjob_1` → `tDBClose_1` (Snowflake).

```mermaid
flowchart TD
    Prejob["tPrejob_1"] --> OpenLog["tJava_1<br/>Open per-run log file"] -->|OnSubjobOk| Keystore["tSetKeystore_1<br/>Configure SSL"] -->|OnSubjobOk| Connect["tDBConnection_1<br/>Open Snowflake connection"]

    Parallel["tParallelize_1"] --> MergeA["tDBRow_2<br/>CALL STAGING.MERGE_INTO_DIMFISCAL_DC_A()"]
    Parallel --> MergeB["tDBRow_1<br/>CALL STAGING.MERGE_INTO_DIMFISCAL_DC_B()"]
    Parallel --> MergeC["tDBRow_3<br/>CALL STAGING.MERGE_INTO_DIMFISCAL_DC_C()"]

    Postjob["tPostjob_1"] --> Close["tDBClose_1<br/>Close Snowflake connection"]
```

## Settings tables

### SSL setup: `tSetKeystore_1`

| Setting | Value | What it means |
|---|---|---|
| SSL_TRUSTSERVER_TRUSTSTORE | `"C:/clientTrustStore.trustStore"` (hardcoded) | Same hardcoded truststore path used across all six `DimFiscal_<SITE>_Load` siblings. |
| SSL_KEYSTORE | `context.keystorePath` | Context-driven. |

### Merges: `tDBRow_1` / `tDBRow_2` / `tDBRow_3`

| Setting | Value | What it means |
|---|---|---|
| Query (`tDBRow_1`) | `CALL STAGING.MERGE_INTO_DIMFISCAL_DC_B();` | Merges the "B" fiscal sub-table for DC. |
| Query (`tDBRow_2`) | `CALL STAGING.MERGE_INTO_DIMFISCAL_DC_A();` | Merges the "A" fiscal sub-table for DC. |
| Query (`tDBRow_3`) | `CALL STAGING.MERGE_INTO_DIMFISCAL_DC_C();` | Merges the "C" fiscal sub-table for DC. |
| Result handling | None captured | No `tJavaRow`/`tWarn`/`tDie` downstream of any of the three. |

## Dependencies & configuration

- **Triggers/depends on other jobs:** none — no `tRunJob` links found, and no orchestrator in this project's captured metadata calls `DimFiscal_DC_Load` (only the CO sibling has a confirmed caller — see `06_dependency_matrix.md`). How/when the DC pipeline (including this job) is triggered is not visible in this metadata.
- **Context variables used:** `keystorePath`, `logDir`.
- **1 hardcoded path finding:** `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE = "C:/clientTrustStore.trustStore"`.

## Glossary

| Component type | Plain-English meaning |
|---|---|
| `tJava` | Runs custom Java code once — here, to redirect console output to a per-run log file. |
| `tSetKeystore` | Configures the SSL trust/keystore used for secure connections made later in the job. |
| `tSnowflakeConnection` / `tSnowflakeClose` / `tSnowflakeRow` | Open/close a Snowflake connection, or run an arbitrary SQL statement/procedure call against it. |
| `tParallelize` | Runs its downstream branches at the same time rather than one after another. |

## Issues observed

- **No result-code checking on any of the three merge calls** — same gap as the CHI/CO siblings.
- **Family comparison — DimFiscal_DC_Load has 3 merge sub-tables (A, B, C)**, matching CO and TOL exactly; CHI has only 2, HH has 5, and PRE nominally has 3 but one is disabled. Unlike `DimFiscal_CO_Load` (called by `CO_Master_Load`), this job has **no confirmed caller** in the project's captured `tRunJob` orchestration — consistent with `05_operational_runbook.md`'s note that only the CO site has a documented `_Master_Load` orchestrator; if DC has an equivalent pipeline trigger, it's not visible in this metadata.
- **Component wiring order in the PARALLELIZE connections is `A, B, C`** (by `tDBRow_2`, `tDBRow_1`, `tDBRow_3` unique names) rather than the `B, A, C` numbering seen in the CO/CHI siblings — purely a cosmetic difference in how the components were numbered/wired during development, with no functional effect since `tParallelize` runs all branches concurrently regardless of listed order.
- Same hardcoded truststore path issue documented across the whole `DimFiscal_<SITE>_Load` family applies here.
