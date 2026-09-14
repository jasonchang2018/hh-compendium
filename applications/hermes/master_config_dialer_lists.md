# master_config_dialer_lists

Source: [master_config_dialer_lists.sql](../../src/sql/master_config_dialer_lists.sql)

Defines desired sizes of agent and agentless dialer lists.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_dialer_lists` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Recreates and loads list-name rows with separate agent and agentless counts.
2. The dialer-file procedure uses these counts alongside group limits and daily weights when allocating calls.

## Output columns

`edwprodhh.hermes.master_config_dialer_lists`:

| Column | Meaning |
| --- | --- |
| `list_name` | Configured dialer-list name. |
| `n_dialeragent` | Configured size of the agent dialer list. |
| `n_dialeragentless` | Configured size of the agentless dialer list. |
