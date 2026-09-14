# master_prediction_scores_transformation_latitude

Source: [master_prediction_scores_transformation_latitude.sql](../../src/sql/master_prediction_scores_transformation_latitude.sql)

Assigns Latitude validation-letter score segments and upload dates.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_scores_transformation_latitude` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_scores_transformation_latitude()` |
| Task | `edwprodhh.hermes.replace_master_prediction_scores_transformation_latitude` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_scores`

It calls the stored procedure.

**Inputs:** `edwprodhh.hermes.master_prediction_pool`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_prediction_scores`.

**Logic:**

1. Truncates the existing destination and selects Latitude debtors with a non-null validation-letter score.
2. Assigns segment `0` when the packet already passes nonoffer validation requirements; otherwise applies fixed score thresholds yielding segments `1` (highest score) through `10`.
3. Calculates next-day or next-week upload dates, with Sunday executions producing a null upload date.
4. Inserts the four output columns from a temporary result. The logging task calls its log procedure but has no declared dependency on this refresh task.

## Output columns

`edwprodhh.hermes.master_prediction_scores_transformation_latitude`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `segment_letters_val` | Latitude validation segment: 0 for an already validated packet, otherwise 1 (best) through 10. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
