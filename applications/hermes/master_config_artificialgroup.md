# master_config_artificialgroup

Source: [master_config_artificialgroup.sql](../../src/sql/master_config_artificialgroup.sql)

Defines shared configuration for clients grouped outside their normal placement groups.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_config_artificialgroup_associations` |
| Table | `edwprodhh.hermes.master_config_artificialgroup` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** Configuration values embedded in the SQL script.

**Logic:**

1. Loads `transform_config_artificialgroup_associations` to map client identifiers to an `artificial_group`.
2. Loads `master_config_artificialgroup` with group activation/channel permissions, maximum and minimum spend or call counts, and minimum margins.
3. Proposal and dialer logic can use the artificial group as `hermes_group` to apply shared constraints across its associated clients.

## Output columns

`edwprodhh.hermes.transform_config_artificialgroup_associations`:

| Column | Meaning |
| --- | --- |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `artificial_group` | Configured grouping of clients outside their usual placement groups. |

`edwprodhh.hermes.master_config_artificialgroup`:

| Column | Meaning |
| --- | --- |
| `artificial_group` | Configured grouping of clients outside their usual placement groups. |
| `is_client_active_hermes_contacts` | Whether the configured group is active for Hermes contacts. |
| `is_client_allowed_letters` | Whether configuration permits letters. |
| `is_client_allowed_texts` | Whether configuration permits texts. |
| `is_client_allowed_voapps` | Whether configuration permits VOAPPS. |
| `is_client_allowed_emails` | Whether configuration permits emails. |
| `is_client_allowed_calls_dialeragent` | Whether configuration permits agent dialer calls. |
| `is_client_allowed_calls_dialeragentless` | Whether configuration permits agentless dialer calls. |
| `is_client_allowed_calls_dialeragentless_stamp` | Whether configuration permits agentless dialer stamping. |
| `max_cost_running_client` | Maximum cumulative spending limit for the entire configured group. |
| `max_cost_running_letters` | Maximum cumulative spending limit for letters. |
| `max_cost_running_texts` | Maximum cumulative spending limit for texts. |
| `max_cost_running_voapps` | Maximum cumulative spending limit for VOAPPS. |
| `max_cost_running_emails` | Maximum cumulative spending limit for emails. |
| `max_n_running_calls` | Maximum cumulative call-count limit for all calls. |
| `max_n_running_calls_dialeragent` | Maximum cumulative call-count limit for agent dialer calls. |
| `max_n_running_calls_dialeragentless` | Maximum cumulative call-count limit for agentless dialer calls. |
| `max_n_running_calls_dialeragentless_stamp` | Maximum cumulative call-count limit for agentless dialer stamping. |
| `min_cost_running_client` | Minimum cumulative spending target for the entire configured group. |
| `min_cost_running_letters` | Minimum cumulative spending target for letters. |
| `min_cost_running_texts` | Minimum cumulative spending target for texts. |
| `min_cost_running_voapps` | Minimum cumulative spending target for VOAPPS. |
| `min_cost_running_emails` | Minimum cumulative spending target for emails. |
| `min_n_running_calls` | Minimum cumulative call-count target for all calls. |
| `min_n_running_calls_dialeragent` | Minimum cumulative call-count target for agent dialer calls. |
| `min_n_running_calls_dialeragentless` | Minimum cumulative call-count target for agentless dialer calls. |
| `min_n_running_calls_dialeragentless_stamp` | Minimum cumulative call-count target for agentless dialer stamping. |
| `min_margin_running_client` | Minimum cumulative margin requirement for the entire configured group. |
| `min_margin_running_letters` | Minimum cumulative margin requirement for letters. |
| `min_margin_running_texts` | Minimum cumulative margin requirement for texts. |
| `min_margin_running_voapps` | Minimum cumulative margin requirement for VOAPPS. |
| `min_margin_running_emails` | Minimum cumulative margin requirement for emails. |
