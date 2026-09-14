# transform_criteria_phone_allowed_voapps

Source: [transform_criteria_phone_allowed_voapps.sql](../../src/sql/transform_criteria_phone_allowed_voapps.sql)

Builds valid VOAPPS phone lists and exclusion reasons for each debtor.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_phone_allowed_voapps` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_phone_allowed_voapps()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_phone_allowed_voapps` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_criteria_texts_exclusions`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_dnc_phones`, `edwprodhh.hermes.transform_criteria_texts_exclusions`, `edwprodhh.pub_jchang.master_voapps_bounced`, `edwprodhh.pub_jchang.dimzip`, `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.pub_jchang.master_calls`, `edwprodhh.pub_jchang.master_voapps`, `edwprodhh.pub_jchang.master_phone_number`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_client`.

**Logic:**

1. Checks DNC/opt-out flags, cell status, bounce history, and source-specific phone availability and consent.
2. Counts prior qualifying voicemail messages by packet and phone; the applicable client categories require both counts to be below three.
3. Applies area-code restrictions, including New York and FDCPA District of Columbia mappings.
4. Aggregates valid phones and a separate semicolon-separated list for each failure reason; empty lists become `NULL`.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_criteria_phone_allowed_voapps`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `valid_phone_number_voapps` | Semicolon-separated distinct phone numbers passing all VOAPPS checks; null when none qualify. |
| `invalid_phone_number_voapps_dnc` | Semicolon-separated VOAPPS phone numbers failing the do-not-call check. |
| `invalid_phone_number_voapps_optout` | Semicolon-separated VOAPPS phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_voapps_cell` | Semicolon-separated VOAPPS phone numbers failing the cell-phone status check. |
| `invalid_phone_number_voapps_consent` | Semicolon-separated VOAPPS phone numbers failing the consent check. |
| `invalid_phone_number_voapps_bounces` | Semicolon-separated VOAPPS phone numbers failing the bounce-history check. |
| `invalid_phone_number_voapps_available` | Semicolon-separated VOAPPS phone numbers failing the source-system availability check. |
| `invalid_phone_number_voapps_ruleof3` | Semicolon-separated VOAPPS phone numbers failing the three-message limit check. |
| `invalid_phone_number_voapps_areacode` | Semicolon-separated VOAPPS phone numbers failing the area-code geography check. |
