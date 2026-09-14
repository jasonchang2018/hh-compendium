# transform_prediction_scores_letters

Source: [transform_prediction_scores_letters.sql](../../src/sql/transform_prediction_scores_letters.sql)

Produces regression and classification prediction scores for letters.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_prediction_scores_letters` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_prediction_scores_letters()` |
| Task | `edwprodhh.hermes.replace_transform_prediction_scores_letters` |

The task runs on `hermes_wh` after `edwprodhh.hermes.replace_transform_prediction_scores_pool` and calls the stored procedure. Each execution rebuilds the table using `CREATE OR REPLACE TABLE ... AS SELECT`.

Logic:

1. Read `edwprodhh.hermes.transform_prediction_scores_pool` and keep only rows where `is_eligible_letters = 1`. Other debtors are excluded from the output.
2. Left join `edwprodhh.hermes.transform_prediction_scores_cached` on `debtor_idx`, requiring cached `score_letters` to be non-null. A matching row supplies both cached component scores; the components are not separately checked for nulls.
3. If no cache row matches, call `edwprodhh.hermes.PROD_PREDICT_V5_LETTER_REG` and `edwprodhh.hermes.PROD_PREDICT_V5_LETTER_CLF`. Inputs are built with `OBJECT_CONSTRUCT_KEEP_NULL`, preserving null values. Features include assigned amount, placement/debt age, department and debt type, placement tier, prior contact counts, commercial status, client-state match, household income, and previous placement/payment indicators.
4. Extract each model's `:value:prediction` and cast the score to `FLOAT`. Set the cache indicator to `1` for a matched cache row or `0` for fresh predictions.

The [cache SQL](../../src/sql/transform_prediction_scores_cached.sql) currently uses `WHERE FALSE`, so its refresh produces an empty table. With that configuration, this procedure calculates fresh predictions and sets the cache indicator to `0`.

## Output columns

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Debtor identifier from the scoring pool. |
| `score_letters_reg` | Regression prediction. |
| `score_letters_clf` | Classification prediction. |
| `score_letters_is_cached` | Whether the scores came from the cache. |
