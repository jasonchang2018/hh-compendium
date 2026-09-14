# master_prediction_scores_transformation_latitude_export

Source: [master_prediction_scores_transformation_latitude_export.sql](../../src/sql/master_prediction_scores_transformation_latitude_export.sql)

Exposes today's Latitude validation segments for export.

| Object | Name |
| --- | --- |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_latitude_export` |
| Table | None defined; this file defines views. |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_scores_transformation_latitude_log`, `edwprodhh.pub_jchang.master_debtor`.

**Logic:**

1. Reads logged Latitude score transformations and joins debtor identifiers to source `debtornumber`.
2. Keeps non-null validation segments whose `upload_date` equals the current date.
3. This is a view over the log; it does not execute the scoring procedure or create an external file.

## Output columns

`edwprodhh.hermes.master_prediction_scores_transformation_latitude_export`:

| Column | Meaning |
| --- | --- |
| `debtornumber` | Account number in the source system. |
| `segment_letters_val` | Latitude validation segment: 0 for an already validated packet, otherwise 1 (best) through 10. |
