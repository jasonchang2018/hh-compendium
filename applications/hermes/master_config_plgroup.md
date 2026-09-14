# master_config_plgroup

Source: [master_config_plgroup.sql](../../src/sql/master_config_plgroup.sql)

Defines placement-group participation, channel permissions, and allocation constraints.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_plgroup` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Creates the table and reloads the configured placement-group rows.
2. Activation and channel flags drive client eligibility. Spend/call minimums, maximums, and margin settings drive proposal and dialer allocation.
3. `budget_group` supports budget grouping; validation-letter settings are separate from ordinary-letter settings. Configuration values are consumed by downstream SQL rather than enforced by this table itself.

## Output columns

`edwprodhh.hermes.master_config_plgroup`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `budget_group` | Configured budget grouping associated with the placement group. |
| `is_client_active_hermes_contacts` | Whether the configured group is active for Hermes contacts. |
| `is_client_allowed_letters_val` | Whether configuration permits validation letters. |
| `is_client_allowed_letters` | Whether configuration permits letters. |
| `is_client_allowed_texts` | Whether configuration permits texts. |
| `is_client_allowed_voapps` | Whether configuration permits VOAPPS. |
| `is_client_allowed_emails` | Whether configuration permits emails. |
| `is_client_allowed_calls_dialeragent` | Whether configuration permits agent dialer calls. |
| `is_client_allowed_calls_dialeragentless` | Whether configuration permits agentless dialer calls. |
| `is_client_allowed_calls_dialeragentless_stamp` | Whether configuration permits agentless dialer stamping. |
| `max_cost_running_client` | Maximum cumulative spending limit for the entire configured group. |
| `max_cost_running_letters_val` | Maximum cumulative spending limit for validation letters. |
| `max_cost_running_letters` | Maximum cumulative spending limit for letters. |
| `max_cost_running_texts` | Maximum cumulative spending limit for texts. |
| `max_cost_running_voapps` | Maximum cumulative spending limit for VOAPPS. |
| `max_cost_running_emails` | Maximum cumulative spending limit for emails. |
| `max_n_running_calls` | Maximum cumulative call-count limit for all calls. |
| `max_n_running_calls_dialeragent` | Maximum cumulative call-count limit for agent dialer calls. |
| `max_n_running_calls_dialeragentless` | Maximum cumulative call-count limit for agentless dialer calls. |
| `max_n_running_calls_dialeragentless_stamp` | Maximum cumulative call-count limit for agentless dialer stamping. |
| `min_cost_running_client` | Minimum cumulative spending target for the entire configured group. |
| `min_cost_running_letters_val` | Minimum cumulative spending target for validation letters. |
| `min_cost_running_letters` | Minimum cumulative spending target for letters. |
| `min_cost_running_texts` | Minimum cumulative spending target for texts. |
| `min_cost_running_voapps` | Minimum cumulative spending target for VOAPPS. |
| `min_cost_running_emails` | Minimum cumulative spending target for emails. |
| `min_n_running_calls` | Minimum cumulative call-count target for all calls. |
| `min_n_running_calls_dialeragent` | Minimum cumulative call-count target for agent dialer calls. |
| `min_n_running_calls_dialeragentless` | Minimum cumulative call-count target for agentless dialer calls. |
| `min_n_running_calls_dialeragentless_stamp` | Minimum cumulative call-count target for agentless dialer stamping. |
| `min_margin_running_client` | Minimum cumulative margin requirement for the entire configured group. |
| `min_margin_running_letters_val` | Minimum cumulative margin requirement for validation letters. |
| `min_margin_running_letters` | Minimum cumulative margin requirement for letters. |
| `min_margin_running_texts` | Minimum cumulative margin requirement for texts. |
| `min_margin_running_voapps` | Minimum cumulative margin requirement for VOAPPS. |
| `min_margin_running_emails` | Minimum cumulative margin requirement for emails. |
