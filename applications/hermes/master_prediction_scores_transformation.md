# master_prediction_scores_transformation

Source: [master_prediction_scores_transformation.sql](../../src/sql/master_prediction_scores_transformation.sql)

Converts debtor scores into relative ranks, deciles, and fixed score segments.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_scores_transformation` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_scores_transformation()` |
| Task | `edwprodhh.hermes.replace_master_prediction_scores_transformation` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_scores`

It calls the stored procedure.

**Inputs:** `edwprodhh.hermes.master_prediction_scores`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_config_score_transformation`.

**Logic:**

1. Keeps non-null debtor scores and adds random noise between `-0.001` and `0.001` to break ties.
2. Calculates row-rank/count percentiles globally and within placement group, then uses `CEIL(percentile * 10)` for deciles.
3. Joins fixed segment boundaries using an exclusive lower and inclusive upper score bound.
4. Outputs the perturbed score and debtor-level rank fields. Higher deciles represent higher scores.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.master_prediction_scores_transformation`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `score_debtor` | Debtor score after adding random tie-breaking noise between -0.001 and 0.001. |
| `percentile_global_debtor` | Relative debtor-score rank (row rank / count) across the scored population. |
| `percentile_local_debtor` | Relative debtor-score rank (row rank / count) within the placement group. |
| `decile_global_debtor` | Debtor-score decile from CEIL(percentile Ã— 10); higher means a higher score across the scored population. |
| `decile_local_debtor` | Debtor-score decile from CEIL(percentile Ã— 10); higher means a higher score within the placement group. |
| `segment_global` | Fixed global score segment matched using configured lower/upper boundaries. |
