# Talend Job: `Address_Text_Load`

## Overview

This job loads debtor address records that arrive as delimited text files into a
Snowflake table, then cleans up after itself. It opens a Snowflake session, runs a
preparatory SQL statement, walks every file in a source directory, parses each one,
adds two extra columns to every row, counts the rows as they pass, and inserts them
into Snowflake. Once the load finishes it runs two activities in parallel: a second
Snowflake SQL statement, and a housekeeping branch that zips each processed file into
an archive directory and then deletes the original. Everything the job touches on disk
is driven by context (environment) variables, so the same job is intended to run
against different directories in different environments.

## Detail table

| Field | Value |
|---|---|
| Job name | `Address_Text_Load` |
| Version | 0.1 |
| Project | LATITUDE |
| Job type | Standard |
| Author | jmach@harriscollect.com |
| Created | 2025-08-04T10:40:42.490-0700 |
| Last modified | 2026-07-12T13:49:17.054-0700 |

> The version has never been incremented past 0.1 despite roughly eleven months
> between creation and the last edit. Treat the version number as unreliable for
> change tracking.

## Step-by-step data flow

**Stage 1 — Prepare the run (pre-job).**
`tPrejob_1` fires before the main work begins and triggers `tJava_1`. That Java snippet
rewrites the archive directory variable in place: `context.archiveDir = context.archiveDir + TalendDa…`
(the extract truncates the line, but it concatenates a Talend date value onto the
configured archive path). The practical effect is that the archive folder is
date-stamped at runtime rather than being a fixed path.

**Stage 2 — Set up TLS, then connect to Snowflake.**
On success, control passes to `tSetKeystore_1`, which configures the Java keystore /
truststore used for SSL, and then to `tDBConnection_1` (`tSnowflakeConnection`), which
opens the Snowflake session that the rest of the job shares.

**Stage 3 — Run a preparatory SQL statement.**
`tDBRow_1` (`tSnowflakeRow`) executes a SQL statement against Snowflake. The statement
text is not present in the extracted metadata (the component's `PROPERTIES` value is
truncated), so **what this SQL does is unable to be determined from metadata — verify
with team.** Typical uses are truncating a staging table or setting a session
parameter. Note that **nothing in the extracted flow connects `tDBConnection_1` to
`tDBRow_1`** — see *Issues observed*.

**Stage 4 — Find the input files.**
`tDBRow_1` hands off to `tFileList_1`, which lists every file directly inside
`context.sourceDir` (subdirectories excluded) and iterates over them one at a time.

**Stage 5 — Remember which file is current.**
For each file, `tJava_2` copies the current filename out of Talend's runtime map into
`context.filePath` (`context.filePath=((String)globalMap.get("tFileList…`). Downstream
components read that variable rather than the iterator directly.

**Stage 6 — Parse the file.**
`tFileInputDelimited_1` reads `context.filePath` as a delimited text file using the
custom row separator `"|$|"` and produces a 29-column record layout (`ADDRESSID`,
`DEBTORASSOCIATIONID`, `DEBTORID`, type/status codes, flags, the street/city/county/
country/postal fields, and the created/modified audit columns).

**Stage 7 — Collect file properties (side branch).**
The same component also iterates into `tFileProperties_1`, which reads operating-system
facts about `context.filePath` — absolute path, directory, base name, permissions
string, size, and modified time — and passes them to `tJavaRow_1`. `tJavaRow_1` has no
outgoing link in the extracted flow, so where these values end up is not visible in the
metadata.

**Stage 8 — Add the two derived columns.**
`tMap_1` takes the 29 parsed columns and emits 31: it prepends `LOAD_DT` (a date,
non-nullable) and `LASTMODIFIED` (a decimal, nullable). The mapping expressions are not
present in the extract, so the exact sources of those two values are **unable to be
determined from metadata — verify with team.** `LASTMODIFIED` is plausibly the `mtime`
captured in Stage 7, but that link is not evidenced. `tMap_1` is set to `DIE_ON_ERROR=true`,
so a mapping failure aborts the job rather than skipping the row.

**Stage 9 — Count the rows.**
`tFlowMeter_1` passes rows through unchanged while recording a row count for
monitoring, in absolute (not relative) mode.

**Stage 10 — Write to Snowflake.**
`tDBOutput_1` (`tSnowflakeOutput`) inserts the 31 columns into a Snowflake table. The
target table name, schema, and write action (insert vs. upsert) are not present in the
extracted metadata — **unable to determine from metadata — verify with team.** The
component also carries nine reject columns (`columnName`, `rowNumber`, `category`,
`character`, `errorMessage`, `byteOffset`, `line`, `sqlState`, `code`), which is the
standard layout for rows Snowflake refuses.

**Stage 11 — Fan out to post-load work.**
Once the file loop completes, `tFileList_1` triggers `tParallelize_1`, which starts two
branches at the same time and waits for all of them:

- *Branch A — housekeeping.* `tFileList_2` lists `context.sourceDir` again; `tJava_3`
  sets `context.filePath` for each entry; `tFileArchive_1` zips the file into
  `context.archiveDir + context.fileName + ".zip"`, creating the directory if needed.
  When that sub-job completes, `tFileList_3` lists the same directory a third time,
  `tJava_4` again sets `context.filePath`, and `tFileDelete_1` deletes the file, failing
  the step if the delete does not succeed.
- *Branch B — second SQL statement.* `tDBRow_2` (`tSnowflakeRow`) runs another Snowflake
  statement. Its statement text is likewise not in the extract — **unable to determine
  from metadata — verify with team.**

There is no explicit commit or close component in the extracted flow, and no `tRunJob`,
so this job neither calls nor is shown calling any other job.

## Settings tables

### `tFileInputDelimited_1` — source file reader

| Setting | Value | What it means |
|---|---|---|
| `FILENAME` | `context.filePath` | Reads whichever file the current loop iteration set, rather than a fixed name. |
| `ROWSEPARATOR` | `"|$|"` | Records are separated by the literal three characters `|$|`, not by newlines. Any tool or hand-edit that "fixes" line endings will corrupt the file. |
| `CSV_OPTION` | `false` | Standard delimited parsing; no CSV quote/escape handling. Values containing the field delimiter will split incorrectly. |
| `USE_EXISTING_DYNAMIC` | `false` | Columns are fixed to the declared 29-column layout, not discovered at runtime. A source file whose column order changes will load into the wrong fields. |

### `tFileProperties_1` — file metadata reader

| Setting | Value | What it means |
|---|---|---|
| `FILENAME` | `context.filePath` | Inspects the file currently being processed. |
| `MD5` | `false` | No checksum is calculated, so there is no content-integrity check on the incoming file. |

### `tFileList_1`, `tFileList_2`, `tFileList_3` — directory scanners

| Setting | Value | What it means |
|---|---|---|
| `DIRECTORY` | `context.sourceDir` | All three scan the same configured drop folder. |
| `LIST_MODE` | `FILES` | Directories are ignored; only files are returned. |
| `INCLUDSUBDIR` | `false` | Files in subfolders are never picked up. |
| `CASE_SENSITIVE` | `YES` | Filename matching respects upper/lower case. |
| `ERROR` | `false` | An unreadable or missing directory does not raise an error here. |

### `tDBOutput_1` — Snowflake target

| Setting | Value | What it means |
|---|---|---|
| `PROPERTIES` | `{"@id":4,"@type":"org.talend.components.snowflake.…` (truncated) | Points at a Snowflake component configuration object; table, schema, and write action are not recoverable from this extract. |
| Reject columns present | 9 error columns on the schema | The component is configured to be able to emit rejected rows, but no reject link appears in the flow. |

### `tFileArchive_1` — archiver

| Setting | Value | What it means |
|---|---|---|
| `SOURCE` | `context.sourceDir` | Archives from the configured drop folder. |
| `SOURCE_FILE` | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s…"` | A hardcoded Windows path inside a developer's Talend Studio install. This should be parameterised. |
| `TARGET` | `context.archiveDir + context.fileName + ".zip"` | Writes one zip per file into the date-stamped archive folder — but `context.fileName` is never assigned by any component in this job (see *Issues observed*). |
| `SUB_DIRECTROY` | `false` | The archive is flat; no folder structure is preserved. |
| `MKDIR` | `true` | Creates the archive folder if it does not exist. |

### `tFileDelete_1` — cleanup

| Setting | Value | What it means |
|---|---|---|
| `FILENAME` | `context.filePath` | Deletes the file for the current iteration. |
| `DIRECTORY` / `PATH` | `"C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d…"` | Hardcoded developer workstation paths. Should be parameterised. |
| `FAILON` | `true` | A failed delete fails the step. |
| `FOLDER` | `false` | Deletes files only, never directories. |

### `tSetKeystore_1` — TLS material

| Setting | Value | What it means |
|---|---|---|
| `SET_TRUSTSTORE` | `false` | Truststore configuration is switched off. |
| `SET_TRUSTSTORE_KEYSTORE` | `false` | The combined truststore/keystore option is also off. |
| `SSL_TRUSTSERVER_TRUSTSTORE` | `"C:/clientTrustStore.trustStore"` | A hardcoded local truststore path is still populated even though the flags above are off. |
| `TRUSTSTORE_TYPE` / `KEYSTORE_TYPE` | `JKS` / `PKCS12` | Standard Java keystore formats. |

### `tParallelize_1` — fan-out controller

| Setting | Value | What it means |
|---|---|---|
| `WAIT_FOR` | `All` | Waits for every parallel branch before continuing. |
| `SLEEPTIME` | `100` | Polls branch completion every 100 ms. |
| `DIE_ON_ERROR` | `false` | If a parallel branch fails, the job keeps going and can still report success. |

### `tFlowMeter_1` — row counter

| Setting | Value | What it means |
|---|---|---|
| `USEROWLABEL` | `true` | Counts are tagged with a label for reporting. |
| `METTERLABEL` | `"MyLabel"` | The label is still Talend's placeholder default, so counts are not identifiable by job or table in monitoring output. |
| `ABSOLUTE` | `Absolute` | Reports a running total rather than a delta from a previous meter. |

## Dependencies & configuration

**Other jobs.** No `tRunJob` component appears in this job, and nothing in the extract
shows another job calling it. Whether it is scheduled directly, chained from an
orchestrator job, or triggered externally is **unable to be determined from metadata —
verify with team.**

**Database.** One Snowflake connection (`tDBConnection_1`) serves `tDBRow_1`,
`tDBOutput_1`, and `tDBRow_2`. `tDBRow_1` and `tDBRow_2` both reference the same
component properties object (`"@id":3`).

**Context variables.**

| Variable | Used by | Why |
|---|---|---|
| `context.sourceDir` | `tFileList_1`, `tFileList_2`, `tFileList_3`, `tFileArchive_1` | The drop folder the job reads from and later cleans out. |
| `context.archiveDir` | `tJava_1`, `tFileArchive_1` | Base archive path, rewritten at runtime with a date suffix. |
| `context.filePath` | `tJava_2/3/4`, `tFileInputDelimited_1`, `tFileProperties_1`, `tFileDelete_1` | Scratch variable holding the file currently being processed. Written by Java snippets during iteration. |
| `context.fileName` | `tFileArchive_1` | Used to build the zip name — but never assigned anywhere in this job. |

The context **group** these variables belong to is not present in the extract —
**unable to determine from metadata — verify with team.**

## Glossary

| Component / term | Plain English |
|---|---|
| `tPrejob` | A starting block that runs setup work before the main job begins. |
| `tJava` | A small block of custom Java code, usually used to set or tweak a variable. |
| `tJavaRow` | Custom Java code that runs once per row of data passing through. |
| `tSetKeystore` | Loads the certificates/keys used for encrypted (SSL/TLS) connections. |
| `tSnowflakeConnection` | Opens one shared login session to the Snowflake data warehouse. |
| `tSnowflakeRow` | Runs a raw SQL statement against Snowflake (not a row-by-row data load). |
| `tSnowflakeOutput` | Writes rows of data into a Snowflake table. |
| `tFileList` | Lists the files in a folder and loops over them one by one. |
| `tFileInputDelimited` | Reads a text file where fields are split by a delimiter and turns it into rows and columns. |
| `tFileProperties` | Reads facts *about* a file (size, path, last-modified time) rather than its contents. |
| `tMap` | The transformation workbench: renames, reshapes, filters, joins, and derives columns. |
| `tFlowMeter` | Counts rows as they pass through, for monitoring. |
| `tFileArchive` | Compresses files into a zip archive. |
| `tFileDelete` | Deletes a file from disk. |
| `tParallelize` | Runs several branches of the job at the same time and waits for them. |
| `ITERATE` link | "Do the next thing once per item in the loop." |
| `FLOW` link | "Pass these rows of data onward." |
| `SUBJOB_OK` / `COMPONENT_OK` link | "Only continue if the previous section/component finished successfully." |

## Issues observed

Each item below cites the specific metadata it comes from. None of them are assumptions
about intent.

1. **`context.fileName` is never assigned.** `tFileArchive_1` builds its target as
   `context.archiveDir + context.fileName + ".zip"`, but no component in this job sets
   `context.fileName` — `tJava_2`, `tJava_3`, and `tJava_4` all set `context.filePath`.
   If `fileName` is a static context value, every file in a run is archived to the same
   zip path and earlier archives may be overwritten. **High priority to verify.**

2. **Files are deleted based on a fresh directory listing, not on what was loaded.**
   `tFileList_1` (load), `tFileList_2` (archive), and `tFileList_3` (delete) each
   independently list `context.sourceDir`. Any file that lands in the folder after the
   load loop but before the delete loop will be archived and deleted without ever being
   loaded — silent data loss with no error raised.

3. **Parallel branch failures are not fatal.** `tParallelize_1` has `DIE_ON_ERROR=false`
   with `WAIT_FOR=All`. The archive/delete branch and the `tDBRow_2` branch can both
   fail while the job still completes. Combined with item 2, a failed archive followed
   by a successful delete would lose the source file.

4. **No visible trigger into `tDBRow_1`.** The extracted flow shows
   `tSetKeystore_1 → tDBConnection_1` and, separately, `tDBRow_1 → tFileList_1`, but
   nothing links `tDBConnection_1` to `tDBRow_1`. Either the extract is incomplete or the
   main sub-job starts independently of the connection sub-job. Verify in Studio before
   assuming ordering is guaranteed.

5. **`tJavaRow_1` is a dead end.** It receives the seven file-property columns from
   `tFileProperties_1` and has no outgoing link. The file metadata is collected but its
   destination is not visible in the extract. If `LASTMODIFIED` in `tMap_1` is meant to
   come from `mtime`, that path is not evidenced here.

6. **Reject handling is declared but not wired.** `tDBOutput_1` carries the nine
   Snowflake reject columns and `tDBRow_1` / `tDBRow_2` carry `errorCode` /
   `errorMessage`, yet no reject (`REJECT`) links appear in the flow. Rows Snowflake
   refuses have no visible destination.

7. **No commit or connection close.** The extract shows no `tSnowflakeCommit`,
   `tSnowflakeClose`, or `tPostjob`. Whether the write is auto-committed is **unable to
   determine from metadata — verify with team.**

8. **Hardcoded developer-workstation paths (should be parameterised).**
   - `tFileArchive_1.SOURCE_FILE` = `C:/Talend-Studio-20211109_1610-V8.0.1/workspace/s…`
   - `tFileDelete_1.DIRECTORY` and `.PATH` = `C:/Talend-Studio-20211109_1610-V8.0.1/workspace/d…`
   - `tSetKeystore_1.SSL_TRUSTSERVER_TRUSTSTORE` = `C:/clientTrustStore.trustStore`
   These are Windows paths tied to one Studio install and one machine. They will not
   resolve on a Linux job server.

9. **Keystore flags contradict the configured path.** `SET_TRUSTSTORE=false` and
   `SET_TRUSTSTORE_KEYSTORE=false` while `SSL_TRUSTSERVER_TRUSTSTORE` still holds a
   path. Confirm whether TLS trust material is actually being applied to the Snowflake
   connection or whether the component is effectively inert.

10. **Flow meter label is the default placeholder.** `METTERLABEL="MyLabel"`, so row
    counts landing in monitoring cannot be attributed to this job or table.

11. **Non-standard row separator with no CSV parsing.** `ROWSEPARATOR="|$|"` combined
    with `CSV_OPTION=false` means the format is brittle: no quoting or escaping is
    honoured, so any address field containing the field delimiter will shift columns.

12. **Duplicated column block in the extracted `tFileInputDelimited_1` schema.** The
    29-column layout appears twice, followed by `errorCode` / `errorMessage`. This most
    likely reflects the component's main and reject schemas being flattened together by
    the extraction, rather than a genuine 60-column file — but that should be confirmed
    in Studio rather than assumed.

13. **Version never incremented.** Version 0.1 with a last-modified date roughly eleven
    months after creation. There is no usable version history in the metadata.

14. **Context variables used as mutable global scratch space.** `context.filePath` is
    rewritten by three different Java components. Because `tParallelize_1` runs branches
    concurrently, any future change that puts two `filePath` writers in different
    parallel branches would produce a race condition.
