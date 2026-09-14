# transform_businessrules_debtor_balance

Source: [transform_businessrules_debtor_balance.sql](../../src/sql/transform_businessrules_debtor_balance.sql)

Calculates debtor and packet balance eligibility.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_debtor_balance` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_debtor_balance()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_debtor_balance` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.dw.dimclient`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_config_treatment_router`.

**Logic:**

1. Copies assigned amount and debtor balance and sums balances over `packet_idx`.
2. Requires debtor balance of at least `5`; packet balance is generally at least `5`, with `15` for DTE EOP.
3. Agent-dialer packet thresholds vary by client/group: the default is the greater of the configured client minimum and `75`, with explicit toll, NTTA, healthcare, and client exceptions.
4. Sets `pass_debtor_assigned` only when assigned amount is positive.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_businessrules_debtor_balance`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `assigned` | Original assigned account amount. |
| `balance_dimdebtor` | Current debtor balance from the source debtor data. |
| `balance_dimdebtor_packet_` | Sum of debtor balances across the packet, before the pool renames the field. |
| `pass_debtor_balance` | Whether the debtor passes the minimum debtor-balance check. |
| `pass_packet_balance` | Whether the debtor passes the minimum packet-balance check. |
| `pass_packet_balance_dialeragent` | Whether the debtor passes the agent-dialer packet-balance threshold. |
| `pass_debtor_assigned` | Whether the debtor passes the positive assigned-amount check. |
