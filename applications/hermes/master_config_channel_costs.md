# master_config_channel_costs

Source: [master_config_channel_costs.sql](../../src/sql/master_config_channel_costs.sql)

Defines the unit costs used to estimate the cost of proposed contacts.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_channel_costs` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates, truncates, and reloads the contact-channel cost table.
2. Provides separate SMS and MMS costs alongside the general text, letter, email, and VOAPPS costs.
3. Both dialer costs are currently `NULL`; consuming queries determine how those nulls are handled.

## Output columns

`edwprodhh.hermes.master_config_channel_costs`:

| Column | Meaning |
| --- | --- |
| `contact_channel` | Contact-channel label used to look up unit cost. |
| `unit_cost` | Configured estimated cost of one contact in the channel. |
