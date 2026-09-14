# master_prediction_time_rotation

Source: [master_prediction_time_rotation.sql](../../src/sql/master_prediction_time_rotation.sql)

Assigns a randomized VOAPPS delivery timestamp to selected proposals.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_time_rotation` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_time_rotation()` |
| Task | `edwprodhh.hermes.replace_master_prediction_time_rotation` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_proposal`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.dimzip`, `edwprodhh.hermes.master_prediction_proposal`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_prediction_phone_selection`.

**Logic:**

1. Maps ZIP codes and area codes to the SQL's standardized time-zone windows.
2. Uses the later of the ZIP/area-code start times and the earlier of their end times. Missing mappings default to 12:00ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“14:00 Central.
3. Samples a random second within that window on the proposal upload date, converts America/Chicago time to UTC, and formats the output timestamp.
4. Keeps selected VOAPPS proposals and returns debtor, channel, upload date, and target timestamp. The logging task reads this output without a declared dependency on this refresh task.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.master_prediction_time_rotation`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `upload_date` | Date the recommendation or segment is intended to appear in the operational export. |
| `voapps_target_date` | Formatted UTC target timestamp for the selected VOAPPS message. |
