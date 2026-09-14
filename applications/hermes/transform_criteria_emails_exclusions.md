# transform_criteria_emails_exclusions

Source: [transform_criteria_emails_exclusions.sql](../../src/sql/transform_criteria_emails_exclusions.sql)

Summarizes email delivery failures by address.

| Object | Name |
| --- | --- |
| View | `edwprodhh.hermes.transform_criteria_emails_exclusions` |
| Table | None defined; this file defines views. |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.liquid.cmi_renkim_returnhistory`, `edwprodhh.pub_jchang.transform_emails_bounced_cubs`.

**Logic:**

1. Reads the specified Latitude Renkim return codes and CUBS bounced-email records.
2. Unions both sources and counts records per email address as `n_bounces`.
3. The view does not itself apply a minimum bounce threshold; the email-address transform decides which addresses to exclude.

## Output columns

`edwprodhh.hermes.transform_criteria_emails_exclusions`:

| Column | Meaning |
| --- | --- |
| `email_address` | Email address; the address-eligibility output may contain a semicolon-separated list of usable addresses. |
| `n_bounces` | Number of email bounce/return records aggregated for the address. |
