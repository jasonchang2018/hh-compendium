# master_prediction_phone_selection_dialer

Source: [master_prediction_phone_selection_dialer.sql](../../src/sql/master_prediction_phone_selection_dialer.sql)

Selects a dialer phone for each qualified packet using weighted historical outcomes.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_phone_selection_dialer` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_phone_selection_dialer()` |
| Task | `edwprodhh.hermes.replace_master_prediction_phone_selection_dialer` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_proposal`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_dnc_packets`, `edwprodhh.pub_jchang.master_dnc_phones`, `edwprodhh.hermes.transform_criteria_texts_exclusions`, `edwprodhh.pub_jchang.master_phone_number`, `edwprodhh.hermes.master_prediction_pool`, `edwprodhh.hermes.master_prediction_proposal`, `edwprodhh.hermes.master_prediction_dialer_file_log`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_calls`, `edwprodhh.pub_jchang.master_texts`, `edwprodhh.pub_jchang.master_texts_bounced`, `edwprodhh.pub_jchang.master_voapps`, `edwprodhh.pub_jchang.master_voapps_bounced`, `edwprodhh.pub_jchang.transform_payment_attribution_contact_weights`, `edwprodhh.pub_jchang.master_contacts`.

**Logic:**

1. Builds available dialer phone options with DNC/opt-out and pool checks, preserving source-field/debtor-member metadata and applying proposal/history exclusions.
2. Scores phone history from calls, texts, VOAPPS, and payment attribution, including a wrong-number indicator.
3. Converts the raw score with `POWER(1.25, phone_score_raw)`, normalizes per packet, and builds a cumulative probability in randomized phone order.
4. Selects the first cumulative value greater than the packet's random cutoff. Returns all candidates with `is_proposed_phone` marking the selected option.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.master_prediction_phone_selection_dialer`:

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
