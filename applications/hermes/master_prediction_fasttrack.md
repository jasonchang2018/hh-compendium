# master_prediction_fasttrack

Source: [master_prediction_fasttrack.sql](../../src/sql/master_prediction_fasttrack.sql)

Stores explicit debtor/channel/template requests for the proposal fast-track path.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_fasttrack` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates, truncates, and loads the manually listed requests.
2. The proposal procedure joins these rows to debtor/pool data, chooses one fast-track row per packet, and applies the fast-track branch's own checks and upload-date logic.
3. Fast-track packets replace ordinary proposal rows for those packets. The proposal procedure truncates this table after processing, so it is a consumed input rather than permanent history.

## Output columns

`edwprodhh.hermes.master_prediction_fasttrack`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `template` | Contact template identifier. |
