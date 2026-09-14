# master_config_batch_priority

Source: [master_config_batch_priority.sql](../../src/sql/master_config_batch_priority.sql)

Defines channel spending limits and minimums by placement group and placement month.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_batch_priority` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates the configuration table and replaces its configured values from the script.
2. Each row supplies letter, text, VOAPPS, and email spend minimums and maximums for a `pl_group` / `batch_month` combination.
3. The proposal procedure joins this configuration for batch-level budget checks. Its separate legacy `BATCH_PRIORITY` iteration is commented out; the configuration still participates in active allocation logic.

## Output columns

`edwprodhh.hermes.master_config_batch_priority`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `batch_month` | Placement-month key used for batch spending constraints. |
| `spend_min_letters` | Minimum batch spending target for letters. |
| `spend_min_texts` | Minimum batch spending target for texts. |
| `spend_min_voapps` | Minimum batch spending target for VOAPPS. |
| `spend_min_emails` | Minimum batch spending target for emails. |
| `spend_max_letters` | Maximum batch spending limit for letters. |
| `spend_max_texts` | Maximum batch spending limit for texts. |
| `spend_max_voapps` | Maximum batch spending limit for VOAPPS. |
| `spend_max_emails` | Maximum batch spending limit for emails. |
