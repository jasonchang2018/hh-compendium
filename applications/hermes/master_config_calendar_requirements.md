# master_config_calendar_requirements

Source: [master_config_calendar_requirements.sql](../../src/sql/master_config_calendar_requirements.sql)

Defines contacts due at specified numbers of days after placement.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_calendar_requirements` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates the table and uses `INSERT OVERWRITE` to replace its configured rows.
2. Rows identify placement group, requested channel (including `ANY`), due day, treatment group, and requirement type.
3. `transform_criteria_calendar_requirement` evaluates the schedule against placement age and previous contacts/proposals. These rows specify requirements, not completed contacts.

## Output columns

`edwprodhh.hermes.master_config_calendar_requirements`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `days_after_placement` | Placement-age day on which the calendar contact is due. |
| `treatment_group` | Treatment group to which the rule applies; ALL is a wildcard where supported by the consuming SQL. |
| `requirement_type` | Additional requirement classification stored with the rule. |
