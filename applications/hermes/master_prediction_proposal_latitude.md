# master_prediction_proposal_latitude

Source: [master_prediction_proposal_latitude.sql](../../src/sql/master_prediction_proposal_latitude.sql)

Combines today's Latitude digital, dialer, and validation recommendations for export.

| Object | Name |
| --- | --- |
| View | `edwprodhh.hermes.master_prediction_proposal_latitude` |
| Table | None defined; this file defines views. |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_prediction_time_rotation_log`, `edwprodhh.hermes.master_prediction_pool`, `edwprodhh.hermes.master_config_voapps_messages`, `edwprodhh.hermes.master_prediction_dialer_file_log`, `edwprodhh.hermes.master_prediction_proposal_validation_log`.

**Logic:**

1. Builds three compatible result sets from selected proposal, dialer-file, and validation logs with today's upload date, then combines them using `UNION ALL`.
2. Ordinary contacts retain template, selected phone, text type, settlement value, and request ID. Text channel labels become `Texts`.
3. VOAPPS rows receive logged send time, configured caller number, message ID derived from the template, and ZIP code; voice append additionally requires non-FDCPA status and message permission.
4. Dialer rows supply phone and subteam. Validation rows currently map NTTA to `NTHF1` and have a null request ID.

## Output columns

`edwprodhh.hermes.master_prediction_proposal_latitude`:

| Column | Meaning |
| --- | --- |
| `number` | Latitude account number. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
| `template` | Contact template identifier. |
| `phone_number` | Selected contact phone number; null when the contact does not use a phone. |
| `subteam` | Dialer group/department supplied to the destination system; null for non-dialer rows. |
| `text_type` | Text message format used for template/cost handling, such as SMS or MMS. |
| `settlement_amt` | Settlement remaining-payment percentage passed from the proposal, despite the amount-like field name. |
| `voapps_target_date` | Formatted UTC target timestamp for the selected VOAPPS message. |
| `voapps_caller_number` | Configured caller telephone number for a VOAPPS export row. |
| `voapps_message_id` | VOAPPS message ID derived by removing the VO prefix from the template. |
| `voapps_zip_code` | Debtor mailing ZIP code supplied with the VOAPPS export. |
| `voapps_voice_append` | Debtor number appended when voice append is allowed and the client is non-FDCPA; otherwise null. |
| `hermes_request_id` | Hermes recommendation identifier passed to the Latitude export; null for the validation branch. |
