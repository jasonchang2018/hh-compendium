# transform_criteria_texts_exclusions

Source: [transform_criteria_texts_exclusions.sql](../../src/sql/transform_criteria_texts_exclusions.sql)

Classifies text responses and errors and attaches phone opt-out flags.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_texts_exclusions` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_texts_exclusions()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_texts_exclusions` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.transform_electronicsmedia`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_optout_phones`.

**Logic:**

1. Normalizes electronic-media text content, distinguishing inbound responses from carrier, phone, and address errors.
2. Aggregates flags by debtor/packet/phone, then propagates them across the packet/phone combination.
3. Sets `stop_text_intent` for inbound responses and `stop_text_error` for specified rejection/address errors; either sets `stop_text`.
4. Joins the phone opt-out source to add `is_phone_fcc_flagged`, then rebuilds the final table from the complete intermediate result.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_criteria_texts_exclusions`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `packet_idx` | Identifier grouping related debtor accounts into a packet. |
| `phone_number` | Telephone number associated with the text-response/error records. |
| `has_inbound_response` | Whether qualifying inbound text content exists for the packet/phone. |
| `has_carrier_error` | Whether carrier-error text content was observed. |
| `has_carrier_error_reject` | Whether carrier-returned/rejected text content was observed. |
| `has_phone_error` | Whether an undeliverable, rejected, deleted, or expired phone-message error was observed. |
| `has_phone_error_reject` | Whether an undeliverable, rejected, or deleted phone-message error was observed. |
| `has_address_error` | Whether an invalid-destination-address text error was observed. |
| `stop_text_intent` | Stop-text indicator derived from qualifying inbound responses. |
| `stop_text_error` | Stop-text indicator derived from rejection or address errors. |
| `stop_text` | Combined stop-text indicator; 1 when either the intent or error check triggers. |
| `is_phone_fcc_flagged` | Whether the phone matches the source phone opt-out list. |
