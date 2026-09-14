# master_config_contact_minimums

Source: [master_config_contact_minimums.sql](../../src/sql/master_config_contact_minimums.sql)

Defines contact-count targets and waiting periods after placement.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_contact_minimums` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Recreates and reloads rules keyed by placement group, channel, and treatment group, with `ALL` available as a wildcard in consuming transforms.
2. `number_contacts` and `within_days_placement` drive minimum-contact priorities; `delay_days_placement` controls when a channel may begin.
3. Stores `requirement_type` as additional rule metadata. The delay and minimum transforms determine which matching rule takes precedence.

## Output columns

`edwprodhh.hermes.master_config_contact_minimums`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `number_contacts` | Required contact count for the configured rule. |
| `within_days_placement` | Placement-age deadline for meeting the configured contact-count target. |
| `delay_days_placement` | Minimum placement age before the contact rule/channel may apply. |
| `treatment_group` | Treatment group to which the rule applies; ALL is a wildcard where supported by the consuming SQL. |
| `requirement_type` | Additional requirement classification stored with the rule. |
