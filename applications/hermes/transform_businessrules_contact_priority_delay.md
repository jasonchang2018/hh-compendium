# transform_businessrules_contact_priority_delay

Source: [transform_businessrules_contact_priority_delay.sql](../../src/sql/transform_businessrules_contact_priority_delay.sql)

Determines whether each channel's initial waiting period has elapsed.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_contact_priority_delay` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_contact_priority_delay()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_contact_priority_delay` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_config_treatment_router`, `edwprodhh.hermes.master_config_contact_minimums`.

**Logic:**

1. Calculates days since placement and joins channel rules using placement-group/treatment matches or `ALL`.
2. For each debtor and channel, chooses the matching rule with the longest `delay_days_placement`.
3. Sets the channel pass flag when placement age is at least that delay; missing rules default to a pass.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_businessrules_contact_priority_delay`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `batch_date` | Account placement date. |
| `days_since_placement` | Days from placement to the current date. |
| `pass_delay_letters` | Whether letters pass the initial placement delay. |
| `pass_delay_texts` | Whether texts pass the initial placement delay. |
| `pass_delay_voapps` | Whether VOAPPS pass the initial placement delay. |
| `pass_delay_emails` | Whether emails pass the initial placement delay. |
| `pass_delay_dialeragent` | Whether agent dialer calls pass the initial placement delay. |
| `pass_delay_dialeragentless` | Whether agentless dialer calls pass the initial placement delay. |
