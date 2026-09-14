# master_prediction_execution

Source: [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql)

Coordinates execution snapshots and writes per-run contact counts.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_config_treatment_router_log` |
| Table written (existing) | `edwprodhh.hermes.master_prediction_proposal_validation_log` |
| Table written (existing) | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_log` |
| Table written (existing) | `edwprodhh.hermes.master_prediction_execution_log` |
| Stored procedure | `edwprodhh.hermes.master_prediction_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | `edwprodhh.hermes.sp_master_prediction_log` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_proposal`
- `edwprodhh.hermes.replace_master_prediction_scores_transformation`
- `edwprodhh.hermes.replace_master_prediction_dialer_file`

It calls the stored procedure.

**Inputs:** `edwprodhh.hermes.master_config_treatment_router`, `edwprodhh.hermes.master_prediction_proposal_validation`, `edwprodhh.hermes.master_prediction_scores_transformation_cubs`, `edwprodhh.hermes.master_prediction_proposal`.

**Logic:**

1. `master_prediction_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` snapshots treatment routing, validation proposals, and CUBS score transformations directly, and calls the individual prediction/config log procedures with the same timestamp.
2. Logs pool, scores, proposals, score transformations, phone choices, time rotation, configuration, dialer outputs, and CUBS/Latitude export views in the procedure's written order.
3. Appends one execution-summary row counting selected proposals by the six channel labels in `master_prediction_proposal`; the separate dialer table is not included in these counts.
4. The logging task waits for ordinary proposals, generic score transformation, and the dialer file. It does not explicitly wait for Latitude score transformation or time rotation, although it reads their outputs.
5. After the procedure/task definitions, the file includes standalone timestamp-specific log deletion statements and a latest-execution query. Those maintenance statements are not part of the scheduled procedure.

The output columns below cover the four direct inserts. Other snapshot schemas are documented in the individual `insert_master_prediction*.md` files and the two configuration log SQL files.

## Output columns

`edwprodhh.hermes.master_config_treatment_router_log`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `treatment_group` | Assigned experiment treatment group; currently null in the treatment router. |
| `treatment_description` | Description of the assigned treatment; currently null in the treatment router. |
| `test_name` | Experiment name; currently null in the treatment router. |
| `test_description` | Experiment description; currently null in the treatment router. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |

`edwprodhh.hermes.master_prediction_proposal_validation_log`:

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
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |

`edwprodhh.hermes.master_prediction_scores_transformation_cubs_log`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `packet` | CUBS packet identifier. |
| `debtornumber` | Account number in the source system. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `local` | Placement-group debtor-score decile exposed in the CUBS view. |
| `global` | Global debtor-score decile exposed in the CUBS view. |
| `equabli_treatment_group` | CUBS treatment-group label; currently TEST. |
| `dialergrp` | GRP1â€“GRP4 derived from the packet's rounded median local debtor-score decile. |
| `equabli_validation_treatment_group` | CUBS validation treatment-group label; currently TEST. |
| `equabli_validation_expiration_date` | Placement date plus ten days for the CUBS validation export. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |

`edwprodhh.hermes.master_prediction_execution_log`:

| Column | Meaning |
| --- | --- |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
| `n_proposed_letters` | Count of selected letters rows in the ordinary proposal table for this execution. |
| `n_proposed_texts` | Count of selected texts rows in the ordinary proposal table for this execution. |
| `n_proposed_voapps` | Count of selected VOAPPS rows in the ordinary proposal table for this execution. |
| `n_proposed_emails` | Count of selected emails rows in the ordinary proposal table for this execution. |
| `n_proposed_dialer_agent` | Count of selected agent dialer calls rows in the ordinary proposal table for this execution. |
| `n_proposed_dialer_agentless` | Count of selected agentless dialer calls rows in the ordinary proposal table for this execution. |
