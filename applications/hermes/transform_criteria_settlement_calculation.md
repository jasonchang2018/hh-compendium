# transform_criteria_settlement_calculation

Source: [transform_criteria_settlement_calculation.sql](../../src/sql/transform_criteria_settlement_calculation.sql)

Calculates whether to propose a settlement and the proposed remaining-payment percentage.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_settlement_calculation` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_settlement_calculation()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_settlement_calculation` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`
- `edwprodhh.hermes.replace_transform_criteria_validation_requirement`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_client`, `edwprodhh.liquid.customer`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.pub_jchang.master_payment_attribution_long`, `edwprodhh.hermes.transform_criteria_validation_requirement`.

**Logic:**

1. Builds allowed settlement groups and client/age-based minimum remaining amounts, then combines them at packet level.
2. Uses prior settlement proposals and payment-attribution history to support sampled settlement choices; otherwise samples an allowed amount in five-point increments.
3. New settlement sampling uses a `0.150` cutoff for tertiary/quaternary placements and `0.075` otherwise. Validation age, low balances, and high remaining-payment percentages can prevent a new offer.
4. Carries forward or adjusts active prior offers through explicit rules. `proposed_sif_amount` is an integer remaining-payment percentage, not a currency amount.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_criteria_settlement_calculation`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `packet_idx` | Identifier grouping related debtor accounts into a packet. |
| `min_sif_remaining` | Minimum allowed remaining-payment fraction, e.g. 0.50 for 50%, from client/age settlement rules. |
| `sif_chance_cutoff` | Probability cutoff used to decide whether to introduce a new settlement offer. |
| `sif_amount_raw` | Sampled remaining-payment percentage before final settlement/proposal checks. |
| `propose_as_sif` | Whether the SQL selects a settlement offer after validation, balance, and history checks. |
| `proposed_sif_amount` | Final proposed remaining-payment percentage as an integer; null when no settlement is proposed. |
