# transform_businessrules_debtor_income

Source: [transform_businessrules_debtor_income.sql](../../src/sql/transform_businessrules_debtor_income.sql)

Adds ZIP-code household income and an income eligibility flag.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_debtor_income` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_debtor_income()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_debtor_income` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_mbutler.master_zip_code_stats`, `edwprodhh.hermes.master_config_treatment_router`.

**Logic:**

1. Joins debtor ZIP codes to `master_zip_code_stats`.
2. Uses a `30,000` minimum for explicitly listed placement groups and `40,000` for other groups.
3. The check substitutes `1,000,000` when income is missing, so missing income passes; the output income value itself remains the joined value.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_businessrules_debtor_income`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `median_household_income` | ZIP-code median household income joined to the debtor. |
| `pass_debtor_income` | Whether the debtor passes the placement-group-specific income threshold (missing income passes). |
