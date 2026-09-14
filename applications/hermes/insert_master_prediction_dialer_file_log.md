# insert_master_prediction_dialer_file_log

Source: [insert_master_prediction_dialer_file_log.sql](../../src/sql/insert_master_prediction_dialer_file_log.sql)

Appends an execution snapshot of the dialer file output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_dialer_file_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_dialer_file_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_dialer_file`.

**Logic:**

1. Copies every dialer candidate and its selection flag. Generates a new 16-character random `request_id` only for selected contacts; unselected rows receive null.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_dialer_file_log`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `hermes_group` | Group used for allocation; a placement/artificial group for ordinary proposals or a dialer department for calls. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `is_priority_minimum` | Whether this channel option has an unmet minimum-contact priority. |
| `is_priority_calendar_requirement` | Whether a configured calendar contact is due and not already satisfied. |
| `marginal_fee` | Predicted fee/revenue for the channel option, including any explicit SQL adjustment. |
| `marginal_cost` | Estimated cost of this contact option. |
| `marginal_n` | Contact-count contribution of the option; 1 per dialer candidate. |
| `marginal_profit` | Predicted fee minus estimated contact cost. |
| `marginal_margin` | Marginal profit divided by marginal fee. |
| `rank_profit` | Candidate rank based on profit and priority ordering; lower is better. |
| `rank_margin` | Candidate rank based on margin and priority ordering; lower is better. |
| `rank_weighted` | Combined/assigned selection rank after the procedure's priority rules; lower is better. |
| `is_proposed_contact` | 1 when the candidate was selected as a contact recommendation; 0 otherwise. |
| `is_fasttrack` | Whether the row comes from the explicit fast-track request branch. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
| `phone` | Candidate or selected telephone number, depending on the output. |
| `phone_field` | Source field associated with the selected dialer phone. |
| `phone_pkt_member` | Packet member associated with the selected dialer phone. |
| `priority` | Dialer order assigned from a randomized sorter biased by time zone; lower numbers are earlier. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
| `request_id` | Identifier used to correlate a selected recommendation with downstream processing/contact history. |
