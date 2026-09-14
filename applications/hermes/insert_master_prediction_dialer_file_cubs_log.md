# insert_master_prediction_dialer_file_cubs_log

Source: [insert_master_prediction_dialer_file_cubs_log.sql](../../src/sql/insert_master_prediction_dialer_file_cubs_log.sql)

Appends an execution snapshot of the dialer file cubs output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_dialer_file_cubs_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_dialer_file_cubs_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_dialer_file_cubs`.

**Logic:**

1. Copies the CUBS dialer export columns. The source view already limits rows to today's selected CUBS contacts and excludes migrated placement groups.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_dialer_file_cubs_log`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `debtornumber` | Account number in the source system. |
| `phone` | Candidate or selected telephone number, depending on the output. |
| `subteam` | Dialer group/department supplied to the destination system; null for non-dialer rows. |
| `campaigntype` | CUBS campaign code: A for agent calls or U for agentless calls. |
| `priority` | Dialer order assigned from a randomized sorter biased by time zone; lower numbers are earlier. |
| `phone_field` | Source field associated with the selected dialer phone. |
| `phone_pkt_member` | Packet member associated with the selected dialer phone. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
