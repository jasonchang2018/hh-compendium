# insert_master_prediction_scores_log

Source: [insert_master_prediction_scores_log.sql](../../src/sql/insert_master_prediction_scores_log.sql)

Appends an execution snapshot of the scores output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_scores_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_scores_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_scores`.

**Logic:**

1. Copies combined debtor/channel scores, regression/classification components, and cache indicators.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_scores_log`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `score_debtor` | Greatest combined channel score, treating missing channel values as zero. |
| `score_letters` | Combined prediction for letters: (1 + classification score) Ã— regression score. |
| `score_letters_val` | Combined prediction for validation letters: (1 + classification score) Ã— regression score. |
| `score_texts` | Combined prediction for texts: (1 + classification score) Ã— regression score. |
| `score_voapps` | Combined prediction for VOAPPS: (1 + classification score) Ã— regression score. |
| `score_emails` | Combined prediction for emails: (1 + classification score) Ã— regression score. |
| `score_dialer_agent` | Combined prediction for agent dialer calls: (1 + classification score) Ã— regression score. |
| `score_dialer_agentless` | Combined prediction for agentless dialer calls: (1 + classification score) Ã— regression score. |
| `score_letters_reg` | Regression-model prediction for letters. |
| `score_letters_val_reg` | Regression-model prediction for validation letters. |
| `score_texts_reg` | Regression-model prediction for texts. |
| `score_voapps_reg` | Regression-model prediction for VOAPPS. |
| `score_emails_reg` | Regression-model prediction for emails. |
| `score_dialer_agent_reg` | Regression-model prediction for agent dialer calls. |
| `score_dialer_agentless_reg` | Regression-model prediction for agentless dialer calls. |
| `score_letters_clf` | Classification-model prediction for letters. |
| `score_letters_val_clf` | Classification-model prediction for validation letters. |
| `score_texts_clf` | Classification-model prediction for texts. |
| `score_voapps_clf` | Classification-model prediction for VOAPPS. |
| `score_emails_clf` | Classification-model prediction for emails. |
| `score_dialer_agent_clf` | Classification-model prediction for agent dialer calls. |
| `score_dialer_agentless_clf` | Classification-model prediction for agentless dialer calls. |
| `score_debtor_is_cached` | Whether the the debtor score was reused from cache (1) rather than calculated fresh (0). |
| `score_letters_is_cached` | Whether the letters score was reused from cache (1) rather than calculated fresh (0). |
| `score_letters_val_is_cached` | Whether the validation letters score was reused from cache (1) rather than calculated fresh (0). |
| `score_texts_is_cached` | Whether the texts score was reused from cache (1) rather than calculated fresh (0). |
| `score_voapps_is_cached` | Whether the VOAPPS score was reused from cache (1) rather than calculated fresh (0). |
| `score_emails_is_cached` | Whether the emails score was reused from cache (1) rather than calculated fresh (0). |
| `score_dialer_agent_is_cached` | Whether the agent dialer calls score was reused from cache (1) rather than calculated fresh (0). |
| `score_dialer_agentless_is_cached` | Whether the agentless dialer calls score was reused from cache (1) rather than calculated fresh (0). |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
