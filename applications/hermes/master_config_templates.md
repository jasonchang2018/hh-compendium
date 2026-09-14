# master_config_templates

Source: [master_config_templates.sql](../../src/sql/master_config_templates.sql)

Defines the contact-template catalog.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_templates` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates and reloads template identifiers with their channel and template type.
2. Template-selection and proposal queries use the catalog to interpret templates and associate enabled templates with channels.

## Output columns

`edwprodhh.hermes.master_config_templates`:

| Column | Meaning |
| --- | --- |
| `template` | Contact template identifier. |
| `channel` | Contact channel associated with the template or rule. |
| `template_type` | Template category, such as settlement or standard collection messaging. |
