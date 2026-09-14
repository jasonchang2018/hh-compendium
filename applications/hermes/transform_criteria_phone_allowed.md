# transform_criteria_phone_allowed

Source: [transform_criteria_phone_allowed.sql](../../src/sql/transform_criteria_phone_allowed.sql)

Combines the channel phone lists with debtor-level calling and texting restrictions.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_phone_allowed` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_phone_allowed()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_phone_allowed` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_criteria_phone_allowed_voapps`
- `edwprodhh.hermes.replace_transform_criteria_phone_allowed_texts`
- `edwprodhh.hermes.replace_transform_criteria_phone_allowed_dialer`
- `edwprodhh.hermes.replace_transform_criteria_debtor_client_active`

It calls the stored procedure.

**Inputs:** `edwprodhh.dw.dimdeskinfo`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimfiscal_co_a`, `edwprodhh.dw.dimfiscal_co_c`, `edwprodhh.dw.dimdebtor`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.hermes.transform_criteria_phone_allowed_texts`, `edwprodhh.hermes.transform_criteria_phone_allowed_voapps`, `edwprodhh.hermes.transform_criteria_phone_allowed_dialer`, `edwprodhh.hermes.transform_criteria_debtor_client_active`.

**Logic:**

1. Joins valid/invalid phone lists from the text, VOAPPS, and dialer transforms and retains their exclusion reasons.
2. Adds debtor/client/fiscal details, then applies healthcare age, payment-plan, commercial/status, desk, and court-date restrictions where specified.
3. Agentless eligibility normally requires both dialer and VOAPPS phone checks; the enabled agentless-stamp path can use the dialer check alone.
4. Several legacy cell/source/status fields are deliberately output as `NULL`.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_phone_allowed`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `packet_idx` | Identifier grouping related debtor accounts into a packet. |
| `valid_phone_number_voapps` | Semicolon-separated distinct phone numbers passing all VOAPPS checks; null when none qualify. |
| `valid_phone_number_texts` | Semicolon-separated distinct phone numbers passing all texts checks; null when none qualify. |
| `valid_phone_number_dialer` | Semicolon-separated distinct phone numbers passing all dialer calls checks; null when none qualify. |
| `phone_number_debtor` | Primary debtor phone number copied from source data. |
| `invalid_phone_number_dialer_dnc` | Semicolon-separated dialer calls phone numbers failing the do-not-call check. |
| `invalid_phone_number_dialer_optout` | Semicolon-separated dialer calls phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_dialer_unavailable` | Semicolon-separated dialer calls phone numbers failing the source-system availability check. |
| `invalid_phone_number_voapps_dnc` | Semicolon-separated VOAPPS phone numbers failing the do-not-call check. |
| `invalid_phone_number_voapps_optout` | Semicolon-separated VOAPPS phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_voapps_cell` | Semicolon-separated VOAPPS phone numbers failing the cell-phone status check. |
| `invalid_phone_number_voapps_consent` | Semicolon-separated VOAPPS phone numbers failing the consent check. |
| `invalid_phone_number_voapps_bounces` | Semicolon-separated VOAPPS phone numbers failing the bounce-history check. |
| `invalid_phone_number_voapps_available` | Semicolon-separated VOAPPS phone numbers failing the source-system availability check. |
| `invalid_phone_number_voapps_ruleof3` | Semicolon-separated VOAPPS phone numbers failing the three-message limit check. |
| `invalid_phone_number_voapps_areacode` | Semicolon-separated VOAPPS phone numbers failing the area-code geography check. |
| `invalid_phone_number_texts_dnc` | Semicolon-separated texts phone numbers failing the do-not-call check. |
| `invalid_phone_number_texts_optout` | Semicolon-separated texts phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_texts_cell` | Semicolon-separated texts phone numbers failing the cell-phone status check. |
| `invalid_phone_number_texts_consent` | Semicolon-separated texts phone numbers failing the consent check. |
| `invalid_phone_number_texts_bounces` | Semicolon-separated texts phone numbers failing the bounce-history check. |
| `invalid_phone_number_texts_available` | Semicolon-separated texts phone numbers failing the source-system availability check. |
| `invalid_phone_number_texts_sol` | Semicolon-separated texts phone numbers failing the placement-age/business-class check. |
| `cell_code_debtor` | Debtor cell code; retained as a legacy placeholder and currently set to NULL. |
| `cell_code_packet_agg` | Aggregated packet cell codes; retained as a legacy placeholder and currently set to NULL. |
| `cell_code_packet_factorized` | Factorized packet cell code; retained as a legacy placeholder and currently set to NULL. |
| `cell_code_packet` | Packet cell code; retained as a legacy placeholder and currently set to NULL. |
| `phone_number_source` | Phone source; retained as a legacy placeholder and currently set to NULL. |
| `current_status_phone` | Current phone status; retained as a legacy placeholder and currently set to NULL. |
| `commercial_code` | Commercial classification code from debtor fiscal data. |
| `state` | Debtor state used in geographic eligibility checks. |
| `is_fdcpa` | Source client flag indicating whether FDCPA-specific rule branches apply. |
| `ash_cli` | Client ASH_CLI attribute carried from the source client table. |
| `payplan` | Existing payment-plan value from the debtor source. |
| `pass_phone_voapps` | Whether VOAPPS pass the debtor-level phone eligibility checks. |
| `pass_phone_texts` | Whether texts pass the debtor-level phone eligibility checks. |
| `pass_phone_dialeragent` | Whether agent dialer calls pass the debtor-level phone eligibility checks. |
| `pass_phone_dialeragentless` | Whether agentless dialer calls pass the debtor-level phone eligibility checks. |
