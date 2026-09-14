# master_config_calendar_clients

Source: [master_config_calendar_clients.sql](../../src/sql/master_config_calendar_clients.sql)

Identifies placement groups subject to calendar-based proposal selection.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_calendar_clients` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Recreates and populates the placement-group list.
2. The proposal procedure reads the list when filtering candidates against calendar requirements; the actual placement-day schedules are configured separately in `master_config_calendar_requirements`.

## Output columns

`edwprodhh.hermes.master_config_calendar_clients`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
