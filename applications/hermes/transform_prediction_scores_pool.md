# transform_prediction_scores_pool

Source: [transform_prediction_scores_pool.sql](../../src/sql/transform_prediction_scores_pool.sql)

Prepares the shared debtor and feature dataset used by the channel scoring procedures.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_prediction_scores_pool` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_prediction_scores_pool()` |
| Task | `edwprodhh.hermes.replace_transform_prediction_scores_pool` |

The task runs on `hermes_wh` after `edwprodhh.hermes.replace_transform_prediction_scores_cached` and calls the stored procedure. Each execution rebuilds the table using `CREATE OR REPLACE TABLE ... AS SELECT`.

Logic:

1. Read `edwprodhh.hermes.master_prediction_pool`.
2. Keep a row when at least one of these flags equals `1`: `is_eligible_letters`, `is_eligible_texts`, `is_eligible_voapps`, `is_eligible_emails`, `is_eligible_dialer_agent`, `is_eligible_dialer_agentless`, `is_eligible_debtor`, or `needs_letters_val_score`.
3. Copy `debtor_idx`, `client_idx`, `pl_group`, the eligibility flags, and the model input features. Features include assigned amount, placement/debt age, debt type, department, placement tier, commercial status, previous contact counts by channel, household income, client-state match, and previous placement/payment indicators.
4. Apply `ORDER BY RANDOM()` to randomize the build query's row order. Consumers must use their own `ORDER BY` if they require a defined read order.

This procedure copies existing features and eligibility decisions; it does not call prediction models or deduplicate debtors. The seven channel/validation scoring tasks run after this task and apply their own eligibility filters.

## Output columns

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `is_eligible_letters` | Whether the debtor is eligible for letters. |
| `is_eligible_texts` | Whether the debtor is eligible for texts. |
| `is_eligible_voapps` | Whether the debtor is eligible for VOAPPS. |
| `is_eligible_emails` | Whether the debtor is eligible for emails. |
| `is_eligible_dialer_agent` | Whether the debtor is eligible for agent dialer calls. |
| `is_eligible_dialer_agentless` | Whether the debtor is eligible for agentless dialer calls. |
| `is_eligible_debtor` | Whether the debtor passes the basic account-status and active-account checks. |
| `needs_letters_val_score` | Whether the account meets the criteria for calculating a validation-letter score. |
| `assigned` | Original assigned account amount. |
| `age_placement` | Days from placement to the current date. |
| `age_debt` | Days since charge-off/last-charge date, falling back to placement date. |
| `is_debttype_hc_ai` | Whether the debtor has healthcare industry and debt-type code AI. |
| `is_debttype_hc_sp` | Whether the debtor has healthcare industry and debt-type code SP. |
| `is_debttype_hc_medicare` | Whether the debtor has healthcare industry and debt-type code MEDICARE. |
| `is_debttype_hc_parent` | Whether the debtor has healthcare industry and debt-type code PARENT. |
| `is_debttype_gov_backlog` | Whether explicit client/placement rules or debt type classify the account as backlog; not restricted to government debt. |
| `is_debttype_gov_parking` | Whether debt type or industry detail identifies parking debt. |
| `is_department_county` | Whether the placement group maps to the county department. |
| `is_department_ems` | Whether the placement group maps to the emergency medical services department. |
| `is_department_hc` | Whether the placement group maps to the healthcare department. |
| `is_department_muni` | Whether the placement group maps to the municipal department. |
| `is_department_state` | Whether the placement group maps to the state department. |
| `is_department_telecom` | Whether the placement group maps to the telecommunications department. |
| `is_debttype_gov_toll` | Whether debt type or industry detail identifies toll debt. |
| `is_department_utl` | Whether the placement group maps to the utilities department. |
| `is_prime` | Whether the placement party is 3P. |
| `is_second` | Whether the placement party is 3P-2. |
| `is_tertiary` | Whether the placement party is 3P-3. |
| `is_quad` | Whether the placement party is 3P-4. |
| `is_commercial` | Whether the debtor is classified as commercial under the SQL rules. |
| `prev_n_contacts` | Number of previous contacts. |
| `prev_n_letters` | Number of previous letters. |
| `prev_n_voapps` | Number of previous VOAPPS. |
| `prev_n_texts` | Number of previous texts. |
| `prev_n_emails` | Number of previous emails. |
| `prev_n_dialer_agent` | Number of previous agent dialer calls. |
| `prev_n_dialer_agentless` | Number of previous agentless dialer calls. |
| `prev_n_outbound_manual` | Number of previous manual outbound calls. |
| `prev_n_inbounds` | Number of previous inbound calls. |
| `median_household_income` | ZIP-code median household income joined to the debtor. |
| `match_client_state` | Whether the debtor state matches the aggregated client-state mapping. |
| `has_other_placement` | Whether more than one debtor row shares the packet. |
| `has_previous_payment` | Whether a payment transaction exists anywhere in the packet. |
