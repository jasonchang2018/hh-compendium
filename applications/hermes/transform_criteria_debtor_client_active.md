# transform_criteria_debtor_client_active

Source: [transform_criteria_debtor_client_active.sql](../../src/sql/transform_criteria_debtor_client_active.sql)

Combines placement-group channel permissions with client exclusions.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_debtor_client_active` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_debtor_client_active()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_debtor_client_active` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.hermes.master_config_client_exclude`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_config_plgroup`.

**Logic:**

1. Aggregates exclusion channels per client and left joins the debtor's placement-group configuration.
2. Requires the group to be active and the individual channel to be allowed; `ALL` or a matching channel exclusion blocks the result.
3. Missing activation/permission settings fail the explicit `= 1` checks. Validation-letter and agentless-stamp permissions have separate output flags.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_debtor_client_active`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `pass_client_active_hermes_contacts` | Whether the debtor passes the client activation and ALL-exclusion checks. |
| `is_client_allowed_letters_val` | Whether configuration permits validation letters. |
| `is_client_allowed_letters` | Whether configuration permits letters. |
| `is_client_allowed_texts` | Whether configuration permits texts. |
| `is_client_allowed_voapps` | Whether configuration permits VOAPPS. |
| `is_client_allowed_emails` | Whether configuration permits emails. |
| `is_client_allowed_calls_dialeragent` | Whether configuration permits agent dialer calls. |
| `is_client_allowed_calls_dialeragentless` | Whether configuration permits agentless dialer calls. |
| `is_client_allowed_calls_dialeragentless_stamp` | Whether configuration permits agentless dialer stamping. |
