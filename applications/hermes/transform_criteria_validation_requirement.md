# transform_criteria_validation_requirement

Source: [transform_criteria_validation_requirement.sql](../../src/sql/transform_criteria_validation_requirement.sql)

Determines whether validation has been received and the required wait has elapsed.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_validation_requirement` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_validation_requirement()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_validation_requirement` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.liquid.miscextra`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.pub_jchang.master_plgroup_map`, `edwprodhh.pub_jchang.master_letters`, `edwprodhh.pub_jchang.transform_validations_latitude`, `edwprodhh.dw.dimfiscal_hh_b`, `edwprodhh.dw.dimfiscal_co_c`, `edwprodhh.dw.dimfiscal_chi_b`, `edwprodhh.dw.dimfiscal_pre_b`, `edwprodhh.dw.dimfiscal_tol_c`.

**Logic:**

1. Collects validation contacts and source-system validation/fiscal history, including packet placement chains for NTTA.
2. Requires validation for NTTA and applicable FDCPA clients, while first-party and TPL branches are exempt.
3. Calculates distinct waiting-period checks for nonoffer, offer, and dialer contact, then combines receipt/date checks into debtor-level pass flags.
4. Rolls debtor checks up to packet-level flags, considering active packet members when the current debtor is active; explicit NTTA exceptions apply to dialer eligibility.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_validation_requirement`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `packet_idx` | Identifier grouping related debtor accounts into a packet. |
| `validation_letter_date` | Validation date selected from the available contact/source-system history. |
| `requires_validation` | Whether the account is subject to the SQL validation requirement. |
| `pass_received_validation` | Whether the debtor passes the validation receipt check. |
| `pass_validation_age_nonoffer` | Whether the debtor-level validation waiting period has elapsed for nonoffer contacts. |
| `pass_validation_age_offer` | Whether the debtor-level validation waiting period has elapsed for offer contacts. |
| `pass_validation_age_dialer` | Whether the debtor-level validation waiting period has elapsed for dialer contacts. |
| `pass_received_other_contacts` | Receipt-of-other-contacts check; retained as a legacy placeholder and currently set to NULL. |
| `pass_validation_requirement_debtor_nonoffer` | Whether the debtor-level combined validation requirement passes for nonoffer contacts. |
| `pass_validation_requirement_debtor_offer` | Whether the debtor-level combined validation requirement passes for offer contacts. |
| `pass_validation_requirement_debtor_dialer` | Whether the debtor-level combined validation requirement passes for dialer contacts. |
| `pass_validation_requirement_nonoffer` | Whether the packet-level combined validation requirement passes for nonoffer contacts. |
| `pass_validation_requirement_offer` | Whether the packet-level combined validation requirement passes for offer contacts. |
| `pass_validation_requirement_dialer` | Whether the packet-level combined validation requirement passes for dialer contacts. |
