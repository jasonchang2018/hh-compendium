# master_config_treatment_router

Source: [master_config_treatment_router.sql](../../src/sql/master_config_treatment_router.sql)

Builds debtor-level fields for experiment and treatment routing.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_treatment_router` |
| Stored procedure | None defined in this file. |
| Task | `edwprodhh.hermes.replace_master_config_treatment_router` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.hermes_root`

It executes the table rebuild directly.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`.

**Logic:**

1. Finds numeric two-digit debtor suffixes and chooses the earliest placement/debtor per packet as the packet mapping.
2. Inner joins that mapping to debtors; packets without a qualifying numeric suffix are excluded.
3. All four treatment/test fields are currently `NULL` because no tests are active. The script defines both an immediate table build and the task's equivalent rebuild SQL.

## Output columns

`edwprodhh.hermes.master_config_treatment_router`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `treatment_group` | Assigned experiment treatment group; currently null in the treatment router. |
| `treatment_description` | Description of the assigned treatment; currently null in the treatment router. |
| `test_name` | Experiment name; currently null in the treatment router. |
| `test_description` | Experiment description; currently null in the treatment router. |
