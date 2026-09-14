# transform_businessrules_debtor_prevpacket

Source: [transform_businessrules_debtor_prevpacket.sql](../../src/sql/transform_businessrules_debtor_prevpacket.sql)

Adds prior-placement and payment-history indicators.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_debtor_prevpacket` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_debtor_prevpacket()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_debtor_prevpacket` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_transactions`.

**Logic:**

1. Flags `has_other_placement` when more than one debtor row shares the packet; this is a packet row-count check, not a strict historical-date comparison.
2. Flags `has_previous_payment` when any transaction in the packet has `is_payment = 1`.
3. Left joins the flags back to debtors and defaults missing flags to `0`.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_businessrules_debtor_prevpacket`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `has_other_placement` | Whether more than one debtor row shares the packet. |
| `has_previous_payment` | Whether a payment transaction exists anywhere in the packet. |
