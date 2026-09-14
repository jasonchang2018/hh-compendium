# master_config_blocked_accounts

Source: [master_config_blocked_accounts.sql](../../src/sql/master_config_blocked_accounts.sql)

Lists debtor accounts that must fail the active-account eligibility check.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_blocked_accounts` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Recreates the table and inserts the explicitly listed debtor identifiers.
2. `transform_criteria_debtor_status` matches these identifiers and sets `pass_debtor_active` to `0`.

## Output columns

`edwprodhh.hermes.master_config_blocked_accounts`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
