# insert_master_prediction_scores_transformation_latitude_log

Source: [insert_master_prediction_scores_transformation_latitude_log.sql](../../src/sql/insert_master_prediction_scores_transformation_latitude_log.sql)

Appends an execution snapshot of the scores transformation latitude output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_scores_transformation_latitude_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_scores_transformation_latitude_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_scores_transformation_latitude`.

**Logic:**

1. Copies debtor/group, validation segment, and upload date from the Latitude transformation table.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_scores_transformation_latitude_log`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `segment_letters_val` | Latitude validation segment: 0 for an already validated packet, otherwise 1 (best) through 10. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
