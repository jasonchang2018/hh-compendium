# master_prediction_scores

Source: [master_prediction_scores.sql](../../src/sql/master_prediction_scores.sql)

Combines the seven channel model outputs into final channel and debtor scores.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_scores` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_scores()` |
| Task | `edwprodhh.hermes.replace_master_prediction_scores` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_prediction_scores_emails`
- `edwprodhh.hermes.replace_transform_prediction_scores_voapps`
- `edwprodhh.hermes.replace_transform_prediction_scores_texts`
- `edwprodhh.hermes.replace_transform_prediction_scores_letters`
- `edwprodhh.hermes.replace_transform_prediction_scores_letters_validation`
- `edwprodhh.hermes.replace_transform_prediction_scores_dialer_agent`
- `edwprodhh.hermes.replace_transform_prediction_scores_dialer_agentless`

It calls the stored procedure.

**Inputs:** `edwprodhh.hermes.transform_prediction_scores_pool`, `edwprodhh.hermes.transform_prediction_scores_letters`, `edwprodhh.hermes.transform_prediction_scores_letters_validation`, `edwprodhh.hermes.transform_prediction_scores_texts`, `edwprodhh.hermes.transform_prediction_scores_voapps`, `edwprodhh.hermes.transform_prediction_scores_emails`, `edwprodhh.hermes.transform_prediction_scores_dialer_agent`, `edwprodhh.hermes.transform_prediction_scores_dialer_agentless`.

**Logic:**

1. Left joins each channel/validation score table to `transform_prediction_scores_pool` by debtor.
2. Calculates each combined channel score as `(1 + classification_score) * regression_score`. Missing component scores can leave the combined channel score null.
3. Sets `score_debtor` to the greatest combined score across channels, substituting zero for missing channel values.
4. Carries the component scores and channel cache indicators forward; the debtor-level cache flag is fixed at `0`.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.master_prediction_scores`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
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
| `score_letters` | Combined prediction for letters: (1 + classification score) Ã— regression score. |
| `score_letters_val` | Combined prediction for validation letters: (1 + classification score) Ã— regression score. |
| `score_texts` | Combined prediction for texts: (1 + classification score) Ã— regression score. |
| `score_voapps` | Combined prediction for VOAPPS: (1 + classification score) Ã— regression score. |
| `score_emails` | Combined prediction for emails: (1 + classification score) Ã— regression score. |
| `score_dialer_agent` | Combined prediction for agent dialer calls: (1 + classification score) Ã— regression score. |
| `score_dialer_agentless` | Combined prediction for agentless dialer calls: (1 + classification score) Ã— regression score. |
| `score_debtor` | Greatest combined channel score, treating missing channel values as zero. |
| `score_debtor_is_cached` | Whether the the debtor score was reused from cache (1) rather than calculated fresh (0). |
| `score_letters_is_cached` | Whether the letters score was reused from cache (1) rather than calculated fresh (0). |
| `score_letters_val_is_cached` | Whether the validation letters score was reused from cache (1) rather than calculated fresh (0). |
| `score_texts_is_cached` | Whether the texts score was reused from cache (1) rather than calculated fresh (0). |
| `score_voapps_is_cached` | Whether the VOAPPS score was reused from cache (1) rather than calculated fresh (0). |
| `score_emails_is_cached` | Whether the emails score was reused from cache (1) rather than calculated fresh (0). |
| `score_dialer_agent_is_cached` | Whether the agent dialer calls score was reused from cache (1) rather than calculated fresh (0). |
| `score_dialer_agentless_is_cached` | Whether the agentless dialer calls score was reused from cache (1) rather than calculated fresh (0). |
