# transform_criteria_phone_allowed_dialer

Source: [transform_criteria_phone_allowed_dialer.sql](../../src/sql/transform_criteria_phone_allowed_dialer.sql)

Builds valid dialer phone lists and exclusion reasons for each debtor.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_phone_allowed_dialer` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_phone_allowed_dialer()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_phone_allowed_dialer` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_criteria_texts_exclusions`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_dnc_phones`, `edwprodhh.hermes.transform_criteria_texts_exclusions`, `edwprodhh.pub_jchang.master_phone_number`.

**Logic:**

1. Removes DNC phones except the two excluded bad-phone source categories, and flags phones found in the FCC/opt-out exclusion result.
2. CUBS requires inclusion in its dialer file; Latitude requires autodialer permission and a non-invalid phone status.
3. Aggregates distinct valid phones and phones failing each check into semicolon-separated lists. Empty lists become `NULL`.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_criteria_phone_allowed_dialer`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `valid_phone_number_dialer` | Semicolon-separated distinct phone numbers passing all dialer calls checks; null when none qualify. |
| `invalid_phone_number_dialer_dnc` | Semicolon-separated dialer calls phone numbers failing the do-not-call check. |
| `invalid_phone_number_dialer_optout` | Semicolon-separated dialer calls phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_dialer_unavailable` | Semicolon-separated dialer calls phone numbers failing the source-system availability check. |
