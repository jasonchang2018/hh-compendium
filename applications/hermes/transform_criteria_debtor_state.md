# transform_criteria_debtor_state

Source: [transform_criteria_debtor_state.sql](../../src/sql/transform_criteria_debtor_state.sql)

Computes channel-specific geographic eligibility and a client-state match feature.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_debtor_state` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_debtor_state()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_debtor_state` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimclient`, `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.hermes.master_prediction_dialer_file_log`, `edwprodhh.pub_jchang.dimzip`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.pub_jchang.master_plgroup_map`.

**Logic:**

1. Builds allowed-state/ZIP mappings, client-state associations, and recent packet contact/proposal attempt checks.
2. Evaluates separate letter, text, VOAPPS, email, agent-dialer, and agentless rules, including ZIP exclusions, state restrictions, FDCPA/industry branches, and explicit client exceptions.
3. Some phone-channel checks also require recent-attempt limits to pass; VOAPPS checks both debtor state and ZIP-derived state.
4. `match_client_state` indicates whether the debtor's state matches the client's aggregated states. These are the rules encoded in this SQL, not an independent statement of legal requirements.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_debtor_state`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `state` | Debtor state used in geographic eligibility checks. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `is_fdcpa` | Source client flag indicating whether FDCPA-specific rule branches apply. |
| `ash_cli` | Client ASH_CLI attribute carried from the source client table. |
| `pass_state_letters` | Whether letters pass the geographic restrictions. |
| `pass_state_texts` | Whether texts pass the geographic restrictions. |
| `pass_state_voapps` | Whether VOAPPS pass the geographic restrictions. |
| `pass_state_emails` | Whether emails pass the geographic restrictions. |
| `pass_state_dialeragent` | Whether agent dialer calls pass the geographic restrictions. |
| `pass_state_dialeragentless` | Whether agentless dialer calls pass the geographic restrictions. |
| `match_client_state` | Whether the debtor state matches the aggregated client-state mapping. |
