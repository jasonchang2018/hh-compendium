# master_config_templates_client

Source: [master_config_templates_client.sql](../../src/sql/master_config_templates_client.sql)

Defines template mappings for individual clients.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_templates_client` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates the table and inserts client/channel/template rows. Its truncate statement is commented out, so executing only the insert appends rows.
2. The sequence-requirement procedure reads these mappings alongside placement-group template settings and client-specific sequence rules.

## Output columns

`edwprodhh.hermes.master_config_templates_client`:

| Column | Meaning |
| --- | --- |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `channel` | Contact channel associated with the template or rule. |
| `template` | Contact template identifier. |
