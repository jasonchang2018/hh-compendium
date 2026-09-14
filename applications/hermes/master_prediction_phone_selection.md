# master_prediction_phone_selection

Source: [master_prediction_phone_selection.sql](../../src/sql/master_prediction_phone_selection.sql)

Selects packet phone numbers for texts and VOAPPS using eligibility and contact history.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_prediction_phone_selection` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_phone_selection()` |
| Task | `edwprodhh.hermes.replace_master_prediction_phone_selection` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_prediction_pool`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_dnc_packets`, `edwprodhh.pub_jchang.master_dnc_phones`, `edwprodhh.hermes.transform_criteria_texts_exclusions`, `edwprodhh.pub_jchang.master_phone_number`, `edwprodhh.hermes.master_prediction_pool`, `edwprodhh.liquid.miscextra`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_calls`, `edwprodhh.pub_jchang.master_texts`, `edwprodhh.pub_jchang.master_texts_bounced`, `edwprodhh.pub_jchang.master_voapps`, `edwprodhh.pub_jchang.master_voapps_bounced`, `edwprodhh.pub_jchang.transform_payment_attribution_contact_weights`, `edwprodhh.pub_jchang.master_contacts`.

**Logic:**

1. Builds qualified phone options from source phone records, DNC/opt-out checks, and pool eligibility.
2. Scores packet/phone history using call outcomes, text/VOAPPS success or errors, payment attribution, and port indicators.
3. Transforms raw scores with `POWER(1.25, phone_score_raw)`, normalizes within packet/channel, and uses cumulative probabilities with a random cutoff to rank phone choices.
4. Iteratively assigns options, up to the configured calculation's cap of 24 iterations, preventing duplicate selected packets or shared phones within each channel. Cross-channel sharing is explicitly left possible.
5. Returns every candidate row with selection flags and iteration metadata. `is_portin` is present here but is omitted by the corresponding log procedure.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.master_prediction_phone_selection`:

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
| `is_portin` | Whether the packet/phone matches the qualifying source port-in information. |
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
