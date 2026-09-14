# transform_criteria_address_allowed_email

Source: [transform_criteria_address_allowed_email.sql](../../src/sql/transform_criteria_address_allowed_email.sql)

Selects usable email addresses and computes debtor email eligibility.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_address_allowed_email` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_address_allowed_email()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_address_allowed_email` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_directory_email`, `edwprodhh.pub_jchang.transform_emails_cubs_log`, `edwprodhh.hermes.master_config_allowed_email_domains`, `edwprodhh.pub_jchang.master_emails`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimfiscal_chi_b`, `edwprodhh.dw.dimfiscal_co_c`, `edwprodhh.dw.dimfiscal_dc_c`, `edwprodhh.dw.dimfiscal_hh_b`, `edwprodhh.dw.dimfiscal_pre_b`, `edwprodhh.dw.dimfiscal_tol_c`, `edwprodhh.hermes.transform_criteria_emails_exclusions`, `edwprodhh.dw.dimdebtor`, `edwprodhh.pub_jchang.master_client`.

**Logic:**

1. Deduplicates debtor/address records by latest authorization date, favoring the restrictive status when dates tie.
2. Retains allowed domains and source-specific authorized/active statuses; excludes addresses with adverse delivery history and aggregates usable addresses with semicolons.
3. Combines fiscal emailable settings, packet opt-outs, and bounce exclusions to produce `pass_address_emails`. CUBS and Latitude have different permission branches.
4. Also exposes the client e-validation indicator and the fiscal/source-derived `is_emailable` flag.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_address_allowed_email`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `email_address` | Email address; the address-eligibility output may contain a semicolon-separated list of usable addresses. |
| `client_evalidation_status` | Indicator for the HH FDCPA client e-validation configuration; 1 when the configured status matches eVAL. |
| `is_emailable` | Source/fiscal permission to email the debtor, before the other address and opt-out checks. |
| `pass_address_emails` | Whether the debtor passes the usable-email, permission, opt-out, and bounce checks. |
