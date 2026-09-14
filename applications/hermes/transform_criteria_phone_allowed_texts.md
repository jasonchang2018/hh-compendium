# transform_criteria_phone_allowed_texts

Source: [transform_criteria_phone_allowed_texts.sql](../../src/sql/transform_criteria_phone_allowed_texts.sql)

Builds valid text phone lists and exclusion reasons for each debtor.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_phone_allowed_texts` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_phone_allowed_texts()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_phone_allowed_texts` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_criteria_texts_exclusions`
- `edwprodhh.hermes.replace_transform_businessrules_debtor_maturity`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_dnc_phones`, `edwprodhh.hermes.transform_criteria_texts_exclusions`, `edwprodhh.pub_jchang.master_texts_bounced`, `edwprodhh.pub_jchang.master_phone_number`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.hermes.transform_businessrules_debtor_maturity`.

**Logic:**

1. Checks DNC/opt-out flags, cell status, recent bounce exclusions, and source-specific text availability.
2. Applies consent rules by system/source/client category and placement-age rules by business class, including explicit client/state exceptions.
3. A phone is valid only when all checks pass. Aggregates valid numbers and separate failure lists with semicolons, returning `NULL` for empty lists.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_criteria_phone_allowed_texts`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `valid_phone_number_texts` | Semicolon-separated distinct phone numbers passing all texts checks; null when none qualify. |
| `invalid_phone_number_texts_dnc` | Semicolon-separated texts phone numbers failing the do-not-call check. |
| `invalid_phone_number_texts_optout` | Semicolon-separated texts phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_texts_cell` | Semicolon-separated texts phone numbers failing the cell-phone status check. |
| `invalid_phone_number_texts_consent` | Semicolon-separated texts phone numbers failing the consent check. |
| `invalid_phone_number_texts_bounces` | Semicolon-separated texts phone numbers failing the bounce-history check. |
| `invalid_phone_number_texts_available` | Semicolon-separated texts phone numbers failing the source-system availability check. |
| `invalid_phone_number_texts_sol` | Semicolon-separated texts phone numbers failing the placement-age/business-class check. |
