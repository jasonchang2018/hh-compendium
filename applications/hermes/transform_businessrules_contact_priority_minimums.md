# transform_businessrules_contact_priority_minimums

Source: [transform_businessrules_contact_priority_minimums.sql](../../src/sql/transform_businessrules_contact_priority_minimums.sql)

Flags debtors that have not yet met configured contact-count targets.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_contact_priority_minimums` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_contact_priority_minimums()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_contact_priority_minimums` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.pub_jchang.transform_contacts`, `edwprodhh.hermes.master_config_treatment_router`, `edwprodhh.hermes.master_config_contact_minimums`.

**Logic:**

1. Counts contacts since placement at packet level. The letter count subtracts one validation letter for FDCPA clients, with a floor of zero.
2. Matches channel rules after their initial delay. Prefers an unmet rule still within its deadline, selecting the shortest such deadline; otherwise selects the longest deadline.
3. Sets priority when the selected rule's contact count is unmet. Missing rules default to no priority.
4. Outputs the placement age, observed counts, and six channel priority flags for downstream cooldown and proposal logic.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_businessrules_contact_priority_minimums`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `batch_date` | Account placement date. |
| `days_since_placement` | Days from placement to the current date. |
| `prev_n_letters_since_placement` | Number of previous letters since this debtor's placement (packet contact history). |
| `prev_n_texts_since_placement` | Number of previous texts since this debtor's placement (packet contact history). |
| `prev_n_voapps_since_placement` | Number of previous VOAPPS since this debtor's placement (packet contact history). |
| `prev_n_emails_since_placement` | Number of previous emails since this debtor's placement (packet contact history). |
| `prev_n_dialer_agent_since_placement` | Number of previous agent dialer calls since this debtor's placement (packet contact history). |
| `prev_n_dialer_agentless_since_placement` | Number of previous agentless dialer calls since this debtor's placement (packet contact history). |
| `is_priority_minimum_letters` | Whether the configured minimum contact count is unmet for letters. |
| `is_priority_minimum_texts` | Whether the configured minimum contact count is unmet for texts. |
| `is_priority_minimum_voapps` | Whether the configured minimum contact count is unmet for VOAPPS. |
| `is_priority_minimum_emails` | Whether the configured minimum contact count is unmet for emails. |
| `is_priority_minimum_dialeragent` | Whether the configured minimum contact count is unmet for agent dialer calls. |
| `is_priority_minimum_dialeragentless` | Whether the configured minimum contact count is unmet for agentless dialer calls. |
