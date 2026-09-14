# transform_prediction_scores_cached

Source: [transform_prediction_scores_cached.sql](../../src/sql/transform_prediction_scores_cached.sql)

Builds the cache structure used to reuse previously logged prediction scores. Caching is currently disabled.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_prediction_scores_cached` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_prediction_scores_cached()` |
| Task | `edwprodhh.hermes.replace_transform_prediction_scores_cached` |

The task runs on `hermes_wh` after `edwprodhh.hermes.replace_master_prediction_pool` and calls the stored procedure. Each execution rebuilds the table using `CREATE OR REPLACE TABLE ... AS SELECT`.

Logic:

1. Read `edwprodhh.hermes.master_prediction_scores_log` and select `debtor_idx`, the overall debtor score, and the channel scores plus their regression/classification components.
2. Rename `score_debtor` to `score_debtor_`. Retain scores for letters, validation letters (`letters_val`), texts, VOAPPS, emails, agent dialer, and agentless dialer.
3. Apply `WHERE FALSE`, which intentionally excludes every row. Each execution therefore replaces the cache with an empty table; the SQL comment attributes this to v3 performance.
4. The query also defines `ROW_NUMBER() OVER (PARTITION BY debtor_idx ORDER BY execute_time DESC) = 1` through `QUALIFY`. If the filter is changed to admit rows, this keeps the latest qualifying log entry per debtor.

The commented seven-day and weekday/debtor-suffix filters are inactive. Downstream scoring procedures use this table for cache lookups, but receive no matches under the current configuration. The scoring-pool task runs after this task.

## Output columns

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `score_debtor_` | Previously logged debtor score, renamed with a trailing underscore in the cache. |
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
