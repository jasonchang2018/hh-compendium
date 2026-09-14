# insert_master_prediction_proposal_cubs_log

Source: [insert_master_prediction_proposal_cubs_log.sql](../../src/sql/insert_master_prediction_proposal_cubs_log.sql)

Appends an execution snapshot of the proposal cubs output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_proposal_cubs_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_proposal_cubs_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_proposal_cubs`.

**Logic:**

1. Copies the CUBS proposal export columns. The source view already filters to today's selected contacts and formats channel/template labels.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_proposal_cubs_log`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `debtornumber` | Account number in the source system. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
