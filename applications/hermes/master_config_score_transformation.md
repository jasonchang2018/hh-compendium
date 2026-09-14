# master_config_score_transformation

Source: [master_config_score_transformation.sql](../../src/sql/master_config_score_transformation.sql)

Defines fixed boundaries for the global debtor-score segments.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_score_transformation` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates ten segment rows using literal `SELECT ... UNION ALL` statements.
2. The score-transformation procedure matches scores using `score > segment_lo AND score <= segment_hi`.
3. Segment 2 currently has identical lower and upper bounds (`0.180`), so that interval cannot match a score.

## Output columns

`edwprodhh.hermes.master_config_score_transformation`:

| Column | Meaning |
| --- | --- |
| `segment` | Fixed debtor-score segment identifier. |
| `segment_lo` | Exclusive lower score boundary of the segment. |
| `segment_hi` | Inclusive upper score boundary of the segment. |
