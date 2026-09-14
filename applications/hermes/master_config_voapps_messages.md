# master_config_voapps_messages

Source: [master_config_voapps_messages.sql](../../src/sql/master_config_voapps_messages.sql)

Defines VOAPPS message and caller-number metadata.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_voapps_messages` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates and reloads message IDs/names, caller-number IDs/names/numbers, and the voice-append permission.
2. The Latitude proposal view matches a VOAPPS template to its message ID, supplies the configured caller number, and allows voice append only when its additional debtor/client conditions also pass.

## Output columns

`edwprodhh.hermes.master_config_voapps_messages`:

| Column | Meaning |
| --- | --- |
| `message_id` | VOAPPS message identifier. |
| `message_name` | Descriptive VOAPPS message name. |
| `callernumber_id` | Identifier of the configured VOAPPS caller number. |
| `callernumber_name` | Descriptive name of the configured caller number. |
| `callernumber_number` | Configured caller telephone number. |
| `allow_voice_append` | Whether the message configuration permits appending account information to the voice message. |
