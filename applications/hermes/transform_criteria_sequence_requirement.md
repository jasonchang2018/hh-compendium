# transform_criteria_sequence_requirement

Source: [transform_criteria_sequence_requirement.sql](../../src/sql/transform_criteria_sequence_requirement.sql)

Chooses channel templates and template priorities for the next contact.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_sequence_requirement` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_sequence_requirement()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_sequence_requirement` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_criteria_settlement_calculation`
- `edwprodhh.hermes.replace_transform_criteria_validation_requirement`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimdebtor`, `edwprodhh.dw.dimfiscal_co_c`, `edwprodhh.dw.dimfiscal_co_a`, `edwprodhh.dw.dimfiscal_tol_c`, `edwprodhh.dw.dimfiscal_tol_a`, `edwprodhh.pub_jchang.master_transactions`, `edwprodhh.pub_jchang.master_debtor_history`, `edwprodhh.pub_jchang.master_letters`, `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.dw.northwestern_upcoming_appts`, `edwprodhh.hermes.master_config_templates_plgroup`, `edwprodhh.hermes.master_config_templates_client`, `edwprodhh.hermes.master_config_templates`, `edwprodhh.liquid.hh_violation`, `edwprodhh.liquid.master`, `edwprodhh.pub_jchang.transform_debtor_latitude`, `edwprodhh.hermes.transform_criteria_settlement_calculation`, `edwprodhh.hermes.transform_criteria_validation_requirement`, `edwprodhh.pub_jchang.master_texts`.

**Logic:**

1. Builds client-specific sequence context from fiscal data, previous contacts/proposals, payments, validation, settlements, and appointment data.
2. Combines enabled placement-group and client template mappings with specialized sequences, including Los Angeles County, Colorado Medicine, NYC, and Northwestern appointments.
3. Uses the ordered client/channel rules to select letter, text, VOAPPS, and email templates and their priority indicators.
4. Returns `text_type` for SMS/MMS handling. Template selection supplies the proposal stage; it does not itself send contacts.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_criteria_sequence_requirement`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `template_letters` | Template chosen by sequence rules for letters. |
| `template_letters_priority` | Priority indicator attached to the selected letters template. |
| `template_texts` | Template chosen by sequence rules for texts. |
| `template_texts_priority` | Priority indicator attached to the selected texts template. |
| `template_voapps` | Template chosen by sequence rules for VOAPPS. |
| `template_voapps_priority` | Priority indicator attached to the selected VOAPPS template. |
| `template_emails` | Template chosen by sequence rules for emails. |
| `template_emails_priority` | Priority indicator attached to the selected emails template. |
| `text_type` | Text message format used for template/cost handling, such as SMS or MMS. |
