# Talend Job: Calls_Load

## Overview

`Calls_Load` is one of twelve near-identical loader jobs in the FAMIGRATION project. It copies contact-centre call records from the `calls` table in the source SQL Server database into the `CALLS` table in the Snowflake data warehouse. In practice it holds who handled each call (agent), when it was placed, how long it spent in each phase (queue, talk, hold, wrap-up), the direction of the call, and outcome flags such as right-party-contact (RPC), promise-to-pay (P2P) and revenue (REV). The job reads the full table with a single SQL query (no filtering), passes every column straight through an intermediate mapping step, and writes it to Snowflake, where it becomes available to downstream reporting tools such as Qlik.

## Detail Table

| Field | Value |
|---|---|
| Job name | Calls_Load |
| Version | 0.1 |
| Project | FAMIGRATION |
| Author | jmach@harriscollect.com |
| Created | 2026-07-30T16:08:12.103-0500 |
| Last Modified | 2026-08-03T13:22:20.283-0500 |

## Step-by-Step Data Flow

1. **Startup** — `tPrejob_1` marks the start of the job, then `tSetKeystore_1` loads the SSL keystore file named in the `keystorePath` context variable, so the job can trust the certificate Snowflake presents. `tDBConnection_1` then opens a connection to Snowflake using that trust configuration (this connection component is defined in the job but, per the extracted metadata, the actual data-writing step below opens its own separate Snowflake connection rather than reusing it — see Issues Observed).
2. **Read** — `tDBInput_1` connects to SQL Server at `10.1.40.7:1433` and runs a `SELECT` against `dbo.calls` (37 columns), pulling every row and column with no filtering or joins.
3. **Map** — `tMap_1` receives those rows and maps every column straight across to the output with no renaming, filtering, or calculated fields — it also has "die on error" turned on, so a type-conversion problem here would stop the job rather than skip the row.
4. **Write** — `tDBOutput_1` writes the mapped rows into the `CALLS` table in the `EDWPRODHH.BIDATA` schema of the `xca26579.us-east-1` Snowflake account, using the `COMPUTE_WH` warehouse and the `DATALOADER` role. The existing target table is left untouched — new rows are simply added on top of whatever is already there.

```mermaid
graph LR
    subgraph Startup[Startup / secure connection]
        tPrejob_1[Pre-job] -->|OK| tSetKeystore_1[Load SSL keystore]
        tSetKeystore_1 -->|OK| tDBConnection_1[Open Snowflake connection]
    end
    subgraph DataFlow[Data movement]
        tDBInput_1["Read dbo.calls (SQL Server)"] -->|rows| tMap_1[Map columns 1:1]
        tMap_1 -->|rows| tDBOutput_1["Write CALLS (Snowflake)"]
    end
```

## Settings

### Source: SQL Server table `dbo.calls` (component `tDBInput_1`, type `tMSSqlInput`)

| Setting | Value | What it means |
|---|---|---|
| HOST | 10.1.40.7 | The network address of the SQL Server machine the source data is read from. |
| PORT | 1433 | The network port SQL Server listens on (1433 is the SQL Server default). |
| DB_SCHEMA | dbo | The schema inside the source database that owns the table (`dbo` is SQL Server's default schema). |
| DBNAME | snowflake | The name Talend was told to use for the source database connection. Despite the name, this is the SQL Server source, not Snowflake — see Issues Observed. |
| USER | svc_talend | The SQL Server login Talend authenticates as to read the source table. |
| TABLE | calls | The specific source table this job reads from. |
| PASS | ***REDACTED*** | The SQL Server password — captured by the extractor as redacted, never in plain text. |

### Target: Snowflake table `CALLS` (component `tDBOutput_1`, type `SnowflakeOutput`)

| Setting | Value | What it means |
|---|---|---|
| configuration.dataSet.dataStore.account | xca26579.us-east-1 | The Snowflake account identifier (region-qualified) the job connects to. |
| configuration.dataSet.dataStore.warehouse | COMPUTE_WH | The Snowflake virtual warehouse (compute cluster) used to run the load. |
| configuration.dataSet.dataStore.database | EDWPRODHH | The Snowflake database the target table lives in. |
| configuration.dataSet.dataStore.dbSchema | BIDATA | The schema inside that Snowflake database the target table lives in. |
| configuration.dataSet.dataStore.role | DATALOADER | The Snowflake role the job's service account assumes for this load. |
| configuration.dataSet.tableName | CALLS | The Snowflake table this job writes to. |
| configuration.snowflakeOutputCommonConfig.tableAction | NONE | What happens to the target table before loading: create it if missing, empty it first, or leave it as-is. |
| configuration.snowflakeOutputCommonConfig.dataAction | INSERT | How rows are written: a straight insert, versus an update-or-insert (upsert) keyed on a column. |
| configuration.snowflakeOutputCommonConfig.upsertKeyColumn | CALLIDKEY | The column that would be used to match existing rows if the load were doing an upsert. |
| configuration.dieOnError | false | Whether the whole job aborts the moment a single row fails to load. |
| configuration.dataSet.dataStore.shareConnection | false | Whether this component reuses another open Snowflake connection in the job instead of opening its own. |

## Dependencies & Configuration

**Other jobs**: none observed. The extracted metadata shows no `tRunJob` component and no cross-job triggers for `Calls_Load` — it runs standalone, on its own trigger/schedule (not visible in the Talend Studio metadata extracted here; verify with the team or Talend Cloud Management Console if this job is deployed as a scheduled Task).

**Context variables**: `keystorePath` (from the `Common_0.1` context group) points to the SSL certificate keystore file (`.p12`) that `tSetKeystore_1` loads before the job opens its Snowflake connection. It lets the job's Snowflake JDBC connection trust the certificate chain it's presented, which is why every job in this project depends on it even though none of them talk to each other.

## Glossary

| Component type | What it does |
|---|---|
| tMSSqlInput | Reads rows out of a Microsoft SQL Server table using a SQL query. |
| tMap | A transformation step that maps columns from the input to the output — here it passes the same columns straight through without changing values. |
| SnowflakeOutput | Writes rows into a table in Snowflake, the cloud data warehouse. |
| SnowflakeConnection | Opens a connection to the Snowflake cloud data warehouse that later steps can use. |
| tSetKeystore | Configures the SSL/TLS certificate store the job uses to make encrypted connections trustworthy. |
| tPrejob | A marker that runs before anything else in the job — used to sequence startup steps. |

## Issues Observed

- **Hardcoded connection details.** The source host (`10.1.40.7`), port (`1433`), and SQL Server login (`svc_talend`) are typed directly into this job's component settings rather than coming from a context variable — the same is true in all 12 jobs in this project. If the source server ever moves, every job has to be edited individually.
- **Misleading connection name.** The source SQL Server connection's `DBNAME` setting is literally `"snowflake"`, even though this component (`tMSSqlInput`) reads from SQL Server, not Snowflake. This is confusing for anyone reading the job cold and worth renaming.
- **No truncate before load, but not an upsert either.** `tableAction` is `NONE` and `dataAction` is `INSERT` — the target table is not emptied before this job runs, and rows are inserted rather than merged. Running this job more than once without truncating `CALLS` first (e.g. manually or via another process) will duplicate every row from the previous run.
- **Unused upsert setting.** An `upsertKeyColumn` (`CALLIDKEY`) is configured, but `dataAction` is set to `INSERT`, not `UPSERT` — so this key is currently inert. It's either a leftover from an earlier design or a sign the load mode should be revisited.
- **Separate Snowflake connection per component.** `shareConnection` is `false`, and the job also defines a standalone `tDBConnection_1` (Snowflake) component that isn't wired into the actual read/write flow shown in the extracted connections — the data-writing step opens its own connection instead. `tDBConnection_1` appears to only gate the SSL keystore setup step; verify with the team whether it's still needed.
