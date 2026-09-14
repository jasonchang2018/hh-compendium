# transform_criteria_validation_eligibility

Source: [transform_criteria_validation_eligibility.sql](../../src/sql/transform_criteria_validation_eligibility.sql)

Determines whether Hermes can propose a new validation contact.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_validation_eligibility` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_validation_eligibility()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_validation_eligibility` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_criteria_validation_requirement`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_prediction_proposal_validation_log`, `edwprodhh.hermes.master_config_plgroup`, `edwprodhh.hermes.transform_criteria_validation_requirement`.

**Logic:**

1. Rejects debtors with an applicable validation proposal in the last ten days, an existing validation date, or missing active validation-letter configuration.
2. Currently permits letters only for the specified NTTA backlog clients when their packet contains no forward-flow accounts.
3. Validation email and text eligibility are currently fixed at `0`.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_criteria_validation_eligibility`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `can_receive_validation_letter` | Whether a new validation letter is allowed; currently restricted to the eligible NTTA backlog case. |
| `can_receive_validation_email` | Whether a validation email is allowed; currently fixed at 0. |
| `can_receive_validation_text` | Whether a validation text is allowed; currently fixed at 0. |
