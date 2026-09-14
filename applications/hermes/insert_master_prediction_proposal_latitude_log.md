# insert_master_prediction_proposal_latitude_log

Source: [insert_master_prediction_proposal_latitude_log.sql](../../src/sql/insert_master_prediction_proposal_latitude_log.sql)

Appends an execution snapshot of the proposal latitude output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_proposal_latitude_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_proposal_latitude_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_proposal_latitude`.

**Logic:**

1. Copies the Latitude export fields for ordinary, dialer, and validation recommendations. Today's upload filtering and branch-specific field mapping occur in the source view.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_proposal_latitude_log`:

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
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
