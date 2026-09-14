# transform_criteria_calendar_requirement

Source: [transform_criteria_calendar_requirement.sql](../../src/sql/transform_criteria_calendar_requirement.sql)

Identifies overdue calendar contacts within the configured due window.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_calendar_requirement` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_calendar_requirement()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_calendar_requirement` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_config_calendar_requirements`.

**Logic:**

1. Aggregates the latest actual contact by channel and latest selected proposal per packet.
2. Joins placement-day requirements and calculates placement age and contact/proposal offsets from placement.
3. A requirement becomes a priority from its due day through the following nine days, unless a relevant contact or proposal occurred at least as recently as two days before that due day.
4. Returns the required channel only for a priority row and uses row ranking to choose a requirement per debtor.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_calendar_requirement`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `age_placement` | Days from placement to the current date. |
| `sent_contact_days_since_placement` | Days from placement to the latest actual contacts contact. |
| `sent_letter_days_since_placement` | Days from placement to the latest actual letters contact. |
| `sent_text_days_since_placement` | Days from placement to the latest actual texts contact. |
| `sent_voapp_days_since_placement` | Days from placement to the latest actual VOAPPS contact. |
| `sent_email_days_since_placement` | Days from placement to the latest actual emails contact. |
| `proposal_days_since_placement` | Days between placement and the latest qualifying packet proposal upload. |
| `is_priority_calendar_requirement` | Whether a configured calendar contact is due and not already satisfied. |
| `channel_calendar_requirement` | Channel required by the due calendar rule; null when no calendar priority applies. |
