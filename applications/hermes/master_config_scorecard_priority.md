# master_config_scorecard_priority

Source: [master_config_scorecard_priority.sql](../../src/sql/master_config_scorecard_priority.sql)

Defines the placement-age window for scorecard priority by placement group.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_scorecard_priority` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Recreates and loads placement-group rows with a `scorecard_months` value.
2. The maturity transform compares months since placement with this window, and proposal ranking uses the configuration to identify scorecard priority.

## Output columns

`edwprodhh.hermes.master_config_scorecard_priority`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `scorecard_months` | Configured placement-age window in months for scorecard priority. |
