# master_config_constraints_global

Source: [master_config_constraints_global.sql](../../src/sql/master_config_constraints_global.sql)

Defines global spending, volume, contract, and profitability settings plus daily allocation weights.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_constraints_global` |
| View | `edwprodhh.hermes.master_config_constraints_global_weightsdow` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates, truncates, and reloads named numeric constraints, including total/channel budgets, monthly VOAPPS/text contracts, dynamic reserve, and marginal/running thresholds.
2. Defines `master_config_constraints_global_weightsdow` with one row per weekday number. Its active output uses `0.20` weights, including a fixed `weight_total`, despite intermediate spend-adjustment calculations.
3. The main proposal procedure currently uses its own fixed `0.2` weights; validation and dialer procedures read the daily-weight view.

## Output columns

`edwprodhh.hermes.master_config_constraints_global`:

| Column | Meaning |
| --- | --- |
| `constraint_name` | Name of the global spending, volume, contract, or profitability constraint. |
| `value` | Numeric setting for the named global constraint. |

`edwprodhh.hermes.master_config_constraints_global_weightsdow`:

| Column | Meaning |
| --- | --- |
| `dow` | Day-of-week number used to select daily budget weights. |
| `weight_letters_val` | Daily allocation multiplier for validation letters. |
| `weight_letters` | Daily allocation multiplier for letters. |
| `weight_voapps` | Daily allocation multiplier for VOAPPS. |
| `weight_texts` | Daily allocation multiplier for texts. |
| `weight_emails` | Daily allocation multiplier for emails. |
| `weight_total` | Daily allocation multiplier for the total budget. |
| `weight_dialeragent` | Daily allocation multiplier for agent dialer calls. |
| `weight_dialeragentless` | Daily allocation multiplier for agentless dialer calls. |
