# insert_master_prediction_phone_selection_dialer_log

Source: [insert_master_prediction_phone_selection_dialer_log.sql](../../src/sql/insert_master_prediction_phone_selection_dialer_log.sql)

Appends an execution snapshot of the phone selection dialer output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_phone_selection_dialer_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_phone_selection_dialer_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_phone_selection_dialer`.

**Logic:**

1. Copies all dialer phone candidates, source metadata, historical metrics, probabilities, and the selected-phone flag.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_phone_selection_dialer_log`:

| Column | Meaning |
| --- | --- |
| `packet_idx` | Identifier grouping related debtor accounts into a packet. |
| `phone` | Candidate or selected telephone number, depending on the output. |
| `dialer_file_label` | Source dialer eligibility/category label retained for the phone. |
| `source_field_agg` | Aggregated source-field names associated with the packet/phone. |
| `debtor_idx_agg` | Aggregated debtor identifiers associated with the packet/phone. |
| `ob_call_is_answered` | Count of qualifying answered outbound calls for the packet/phone. |
| `ob_call_is_not_answered` | Count of unanswered outbound calls for the packet/phone. |
| `ob_call_is_rpc` | Count of outbound calls meeting the SQL's right-party-contact condition. |
| `ob_call_is_not_rpc` | Count of outbound calls with rpc = 0 and talk time below 60 seconds. |
| `ob_call_is_wrong_number` | Count of outbound calls carrying a wrong-number wrap code. |
| `ib_call_n` | Count of inbound calls for the packet/phone. |
| `text_is_successful` | Count of text records treated as successful for the packet/phone. |
| `text_is_error` | Count of bounced text records for the packet/phone. |
| `voapp_is_successful` | Count of VOAPPS records treated as successful for the packet/phone. |
| `voapp_is_error` | Count of bounced VOAPPS records for the packet/phone. |
| `attr_last` | Whether a qualifying contact on this packet/phone received last-contact payment attribution. |
| `phone_score_raw` | Weighted phone-history score before exponentiation and probability normalization. |
| `phone_score_transform` | POWER(1.25, phone_score_raw), used as a relative phone-selection weight. |
| `phone_score` | Normalized phone-selection probability within the packet. |
| `phone_score_cdf` | Cumulative phone-selection probability within the packet. |
| `rand_cutoff` | Random value between 0 and 1 used to select/rank phone options. |
| `is_proposed_phone` | Whether this dialer phone was selected for the packet. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
