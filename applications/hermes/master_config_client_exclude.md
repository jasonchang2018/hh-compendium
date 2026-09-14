# master_config_client_exclude

Source: [master_config_client_exclude.sql](../../src/sql/master_config_client_exclude.sql)

Defines client-specific exclusions from one or all contact channels.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_client_exclude` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Recreates and populates client/channel exclusion rows.
2. The client-activity transform aggregates each client's exclusions and blocks `ALL` or the matching named channel, in addition to placement-group permissions.

## Output columns

`edwprodhh.hermes.master_config_client_exclude`:

| Column | Meaning |
| --- | --- |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `exclude_channel` | Excluded contact-channel label, or ALL to exclude every channel. |
