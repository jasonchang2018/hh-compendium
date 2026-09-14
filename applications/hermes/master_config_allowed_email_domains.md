# master_config_allowed_email_domains

Source: [master_config_allowed_email_domains.sql](../../src/sql/master_config_allowed_email_domains.sql)

Defines the email-domain allowlist used when selecting usable email addresses.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_allowed_email_domains` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates the single-column configuration table and loads the domains listed in the script.
2. Email eligibility checks require the extracted address domain to appear here; this file does not validate individual addresses.

## Output columns

`edwprodhh.hermes.master_config_allowed_email_domains`:

| Column | Meaning |
| --- | --- |
| `domain` | Allowed email-domain value. |
