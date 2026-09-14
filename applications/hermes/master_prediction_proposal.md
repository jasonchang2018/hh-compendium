# master_prediction_proposal

Source: [master_prediction_proposal.sql](../../src/sql/master_prediction_proposal.sql)

Allocates ordinary contact recommendations across channels, priorities, and budgets.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_proposal` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_proposal()` |
| Task | `edwprodhh.hermes.replace_master_prediction_proposal` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_proposal_validation`
- `edwprodhh.hermes.replace_master_prediction_phone_selection`

It calls the stored procedure.

**Inputs:** `edwprodhh.hermes.master_config_constraints_global`, `edwprodhh.hermes.master_prediction_scores`, `edwprodhh.hermes.master_config_templates`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_prediction_pool`, `edwprodhh.hermes.transform_config_artificialgroup_associations`, `edwprodhh.hermes.master_config_artificialgroup`, `edwprodhh.hermes.master_config_scorecard_priority`, `edwprodhh.hermes.master_prediction_phone_selection`, `edwprodhh.hermes.master_prediction_proposal_validation`, `edwprodhh.hermes.master_config_calendar_clients`, `edwprodhh.hermes.master_config_objectives`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.hermes.master_config_channel_costs`, `edwprodhh.hermes.master_config_batch_priority`, `edwprodhh.hermes.master_config_plgroup`, `edwprodhh.hermes.master_config_plgroup_autobudget`, `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.dw.dimdate`, `edwprodhh.hermes.master_prediction_fasttrack`.

**Logic:**

1. Unpivots scored letter/text/VOAPPS/email options and attaches packet/group mappings, selected phones, templates, settlement percentages, and minimum/calendar/scorecard priorities. Filters conflicts with validation proposals and channel/calendar requirements.
2. Calculates marginal fee, cost, profit, and margin, then combines profit/margin ranks using configured objective weights. Ordinary proposal margin is `profit / cost`; an explicit NTTA text cohort has a fee multiplier.
3. Runs allocation passes for special contacts, minimums and general spending, subscription capacity, and dynamic reserve. Applies packet uniqueness and global, group, channel, and batch spending constraints while tracking already allocated spend.
4. Combines ordinary candidate rows with the fast-track branch. Marks actual recommendations with `is_proposed_contact`, selected phone, random request ID, iteration, and upload date; ordinary rejected candidates can remain for diagnostics.
5. Applies source/channel-specific weekday rules and hard-coded holiday exclusions. Removes ordinary rows for fast-track packets, drops helper views, and clears the fast-track input table.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.master_prediction_proposal`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `artificial_group` | Configured grouping of clients outside their usual placement groups. |
| `hermes_group` | Group used for allocation; a placement/artificial group for ordinary proposals or a dialer department for calls. |
| `template` | Contact template identifier. |
| `text_type` | Text message format used for template/cost handling, such as SMS or MMS. |
| `sif_remaining` | Remaining-payment percentage attached to the proposed settlement template. |
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
| `request_id` | Identifier used to correlate a selected recommendation with downstream processing/contact history. |
| `is_fasttrack` | Whether the row comes from the explicit fast-track request branch. |
| `iteration` | Allocation iteration associated with the selected proposal. |
| `iteration_desc` | Allocation pass label, such as SPECIAL, SUBSCRIPTION, DYNAMIC, or FASTTRACK. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
