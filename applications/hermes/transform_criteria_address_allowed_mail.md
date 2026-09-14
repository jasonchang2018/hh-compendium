# transform_criteria_address_allowed_mail

Source: [transform_criteria_address_allowed_mail.sql](../../src/sql/transform_criteria_address_allowed_mail.sql)

Copies mailing-address fields and evaluates letter-address eligibility.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_address_allowed_mail` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_address_allowed_mail()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_address_allowed_mail` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_businessrules_debtor_maturity`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimfiscal_chi_b`, `edwprodhh.dw.dimfiscal_co_c`, `edwprodhh.dw.dimfiscal_co_b`, `edwprodhh.dw.dimfiscal_dc_c`, `edwprodhh.dw.dimfiscal_hh_b`, `edwprodhh.dw.dimfiscal_pre_b`, `edwprodhh.dw.dimfiscal_tol_c`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.hermes.transform_businessrules_debtor_maturity`, `edwprodhh.pub_jchang.transform_debtor_latitude`.

**Logic:**

1. Calls `contact_address_valid_mail` and rejects Latitude returned-mail records.
2. Applies special rules for Los Angeles County's `FTA` communication descriptor and Houston EMS service age (over four years fails).
3. Returns the address and a binary pass flag; it does not standardize or replace the source address.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_address_allowed_mail`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `mailing_address` | Debtor mailing street address. |
| `mailing_city` | Debtor mailing city. |
| `mailing_state` | Debtor mailing state. |
| `mailing_zip_code` | Debtor mailing ZIP/postal code. |
| `pass_address_letters` | Whether the debtor passes the mail-address validity and applicable client-specific restrictions. |
