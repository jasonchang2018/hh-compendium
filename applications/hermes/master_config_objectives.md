# master_config_objectives

Source: [master_config_objectives.sql](../../src/sql/master_config_objectives.sql)

Defines the weights used to combine proposal ranking objectives.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_objectives` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates and reloads `metric_name` / `weight` rows.
2. Proposal and dialer ranking queries pivot these weights and combine profit and margin ranks into `rank_weighted`.

## Output columns

`edwprodhh.hermes.master_config_objectives`:

| Column | Meaning |
| --- | --- |
| `metric_name` | Ranking objective name, such as Profit or Margin. |
| `weight` | Weight assigned to the ranking objective. |
