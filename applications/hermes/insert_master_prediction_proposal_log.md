# insert_master_prediction_proposal_log

Source: [insert_master_prediction_proposal_log.sql](../../src/sql/insert_master_prediction_proposal_log.sql)

Appends an execution snapshot of the proposal output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_proposal_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_proposal_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_proposal`.

**Logic:**

1. Copies every proposal candidate and its selection flag; sets the legacy `is_eligible_tax` column to `0` and preserves the existing request ID.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_proposal_log`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `artificial_group` | Configured grouping of clients outside their usual placement groups. |
| `hermes_group` | Group used for allocation; a placement/artificial group for ordinary proposals or a dialer department for calls. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `is_priority_minimum` | Whether this channel option has an unmet minimum-contact priority. |
| `is_priority_calendar_requirement` | Whether a configured calendar contact is due and not already satisfied. |
| `marginal_fee` | Predicted fee/revenue for the channel option, including any explicit SQL adjustment. |
| `marginal_cost` | Estimated cost of this contact option. |
| `marginal_profit` | Predicted fee minus estimated contact cost. |
| `marginal_margin` | Marginal profit divided by marginal cost. |
| `rank_profit` | Candidate rank based on profit and priority ordering; lower is better. |
| `rank_margin` | Candidate rank based on margin and priority ordering; lower is better. |
| `rank_weighted` | Combined/assigned selection rank after the procedure's priority rules; lower is better. |
| `is_proposed_contact` | 1 when the candidate was selected as a contact recommendation; 0 otherwise. |
| `phone_number` | Selected contact phone number; null when the contact does not use a phone. |
| `is_fasttrack` | Whether the row comes from the explicit fast-track request branch. |
| `iteration` | Allocation iteration associated with the selected proposal. |
| `iteration_desc` | Allocation pass label, such as SPECIAL, SUBSCRIPTION, DYNAMIC, or FASTTRACK. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
| `is_eligible_tax` | Legacy tax-eligibility field; written as 0 by the proposal log procedure. |
| `template` | Contact template identifier. |
| `text_type` | Text message format used for template/cost handling, such as SMS or MMS. |
| `sif_remaining` | Remaining-payment percentage attached to the proposed settlement template. |
| `request_id` | Identifier used to correlate a selected recommendation with downstream processing/contact history. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
