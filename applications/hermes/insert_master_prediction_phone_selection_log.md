# insert_master_prediction_phone_selection_log

Source: [insert_master_prediction_phone_selection_log.sql](../../src/sql/insert_master_prediction_phone_selection_log.sql)

Appends an execution snapshot of the phone selection output.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_phone_selection_log` |
| Stored procedure | `edwprodhh.hermes.insert_master_prediction_phone_selection_log(EXECUTE_TIME TIMESTAMP_LTZ(9))` |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_phone_selection`.

**Logic:**

1. Copies all text/VOAPPS phone candidates, historical metrics, probabilities, selection flags, and iteration metadata. The source table's `is_portin` column is not included in this log insert.
2. Adds the supplied `EXECUTE_TIME TIMESTAMP_LTZ(9)` to each inserted row. The procedure uses an explicit target column list and does not create the destination table.
3. Called by `edwprodhh.hermes.master_prediction_log` in [master_prediction_execution.sql](../../src/sql/master_prediction_execution.sql); it has no task of its own.
4. The insert appends all rows returned by its source with no additional filter or deduplication. Repeating the call can append another snapshot of the same data.

## Output columns

`edwprodhh.hermes.master_prediction_phone_selection_log`:

| Column | Meaning |
| --- | --- |
| `packet_idx` | Identifier grouping related debtor accounts into a packet. |
| `phone` | Candidate or selected telephone number, depending on the output. |
| `is_eligible_texts` | Whether this packet/phone is eligible for texts. |
| `is_eligible_voapps` | Whether this packet/phone is eligible for VOAPPS. |
| `ob_call_is_answered` | Count of qualifying answered outbound calls for the packet/phone. |
| `ob_call_is_not_answered` | Count of unanswered outbound calls for the packet/phone. |
| `ob_call_is_rpc` | Count of outbound calls meeting the SQL's right-party-contact condition. |
| `ob_call_is_not_rpc` | Count of outbound calls with rpc = 0 and talk time below 60 seconds. |
| `ib_call_n` | Count of inbound calls for the packet/phone. |
| `text_is_successful` | Count of text records treated as successful for the packet/phone. |
| `text_is_error` | Count of bounced text records for the packet/phone. |
| `voapp_is_successful` | Count of VOAPPS records treated as successful for the packet/phone. |
| `voapp_is_error` | Count of bounced VOAPPS records for the packet/phone. |
| `attr_last` | Whether a qualifying contact on this packet/phone received last-contact payment attribution. |
| `is_portout` | Whether the packet/phone matches the qualifying source port-out information. |
| `phone_score_raw` | Weighted phone-history score before exponentiation and probability normalization. |
| `phone_score_transform_texts` | Exponentiated raw score used as the selection weight for texts. |
| `phone_score_transform_voapps` | Exponentiated raw score used as the selection weight for VOAPPS. |
| `phone_score_texts` | Normalized within-packet selection probability for texts. |
| `phone_score_voapps` | Normalized within-packet selection probability for VOAPPS. |
| `phone_score_texts_cdf` | Cumulative within-packet phone-selection probability for texts. |
| `phone_score_voapps_cdf` | Cumulative within-packet phone-selection probability for VOAPPS. |
| `rand_cutoff` | Random value between 0 and 1 used to select/rank phone options. |
| `packet_priority` | Packet rank used to resolve competition for shared phone numbers. |
| `n_packet_options_texts` | Number of eligible packet phone options for texts. |
| `selection_calc_texts` | Cumulative probability minus the random cutoff, wrapped into [0, 1), used to rank texts. |
| `phone_priority_texts` | Within-packet phone preference rank for texts. |
| `n_packet_options_voapps` | Number of eligible packet phone options for VOAPPS. |
| `selection_calc_voapps` | Cumulative probability minus the random cutoff, wrapped into [0, 1), used to rank VOAPPS. |
| `phone_priority_voapps` | Within-packet phone preference rank for VOAPPS. |
| `is_proposed_phone_texts` | Whether this phone was selected for texts. |
| `is_proposed_phone_voapps` | Whether this phone was selected for VOAPPS. |
| `iteration_num` | Phone-selection iteration in which the candidate was selected; null when not selected. |
| `execute_time` | Timestamp supplied by the logging caller to identify the execution snapshot. |
