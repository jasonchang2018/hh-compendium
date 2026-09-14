# insert_master_prediction_time_rotation_log

Source: [insert_master_prediction_time_rotation_log.sql](../../src/sql/insert_master_prediction_time_rotation_log.sql)

Appends an execution snapshot of the time rotation output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_time_rotation_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_time_rotation_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_time_rotation`.

**Logic:**

1. Copies the debtor, channel, upload date, and randomized VOAPPS target timestamp.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_time_rotation_log`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
| `voapps_target_date` | Formatted UTC target timestamp for the selected VOAPPS message. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
