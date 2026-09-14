# master_prediction_proposal_validation

Source: [master_prediction_proposal_validation.sql](../../src/sql/master_prediction_proposal_validation.sql)

Selects validation contacts within client and global budgets.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_proposal_validation` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_proposal_validation()` |
| Task | `edwprodhh.hermes.replace_master_prediction_proposal_validation` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_scores`

It calls the stored procedure.

**Inputs:** `edwprodhh.hermes.master_prediction_pool`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_config_channel_costs`, `edwprodhh.hermes.master_config_constraints_global_weightsdow`, `edwprodhh.hermes.master_config_constraints_global`, `edwprodhh.hermes.master_config_plgroup`.

**Logic:**

1. Unpivots eligible letter/email/text validation flags into contact options and attaches unit costs.
2. Ranks NTTA first (with its charge-off date ordering), then channel preference and placement/debtor ordering; keeps the best option per packet.
3. Applies client and global cumulative-cost limits and minimums using daily weights.
4. Returns candidate validation options with `is_proposed_contact` marking the selected rows; rejected options remain for diagnostics. Upload dates are next day MondayÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“Thursday, next Monday on Friday, and null on weekends. Upstream eligibility currently disables validation email/text channels.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.master_prediction_proposal_validation`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `packet_idx` | Identifier grouping related debtor accounts into a packet. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `batch_date` | Account placement date. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `marginal_cost` | Estimated cost of this contact option. |
| `rank_weighted` | Combined/assigned selection rank after the procedure's priority rules; lower is better. |
| `is_proposed_contact` | 1 when the candidate was selected as a contact recommendation; 0 otherwise. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
