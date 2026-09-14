# insert_master_prediction_scores_transformation_log

Source: [insert_master_prediction_scores_transformation_log.sql](../../src/sql/insert_master_prediction_scores_transformation_log.sql)

Appends an execution snapshot of the scores transformation output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_scores_transformation_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_scores_transformation_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_scores_transformation`.

**Logic:**

1. Copies the transformed debtor score and segment, renames the percentile/decile fields by dropping `_debtor`, and writes `packet_idx` as `NULL`.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_scores_transformation_log`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `packet_idx` | Legacy packet identifier; this insert writes NULL. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `score_debtor` | Debtor score after adding random tie-breaking noise between -0.001 and 0.001. |
| `percentile_global` | Relative debtor-score rank (row rank / count) across the scored population. |
| `percentile_local` | Relative debtor-score rank (row rank / count) within the placement group. |
| `decile_global` | Debtor-score decile from CEIL(percentile Ã— 10); higher means a higher score across the scored population. |
| `decile_local` | Debtor-score decile from CEIL(percentile Ã— 10); higher means a higher score within the placement group. |
| `segment_global` | Fixed global score segment matched using configured lower/upper boundaries. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
