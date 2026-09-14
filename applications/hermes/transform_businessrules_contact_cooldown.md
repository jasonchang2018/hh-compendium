# transform_businessrules_contact_cooldown

Source: [transform_businessrules_contact_cooldown.sql](../../src/sql/transform_businessrules_contact_cooldown.sql)

Calculates contact history and channel cooldown flags for each debtor.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_contact_cooldown` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_contact_cooldown()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_contact_cooldown` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_businessrules_contact_priority_minimums`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_calls`, `edwprodhh.pub_jchang.master_letters`, `edwprodhh.pub_jchang.master_contacts`, `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.hermes.master_prediction_dialer_file_log`, `edwprodhh.dw.dimdebtor`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.hermes.transform_businessrules_contact_priority_minimums`.

**Logic:**

1. Aggregates actual packet contacts, prior proposals, dialer proposals, and latest placement dates. Maintains lifetime, recent seven-day, and post-placement counts/dates.
2. Evaluates channel-specific warmup, contact-count, and elapsed-time conditions with placement-group exceptions and minimum-contact priorities.
3. Combines the count/date flags into each channel's cooldown result and calculates `pass_7in7`. Prior proposals participate so a pending recommendation can suppress another contact.
4. History columns explain why a debtor passes or fails; model scoring also uses the contact-count features.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_businessrules_contact_cooldown`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `next_date_letters` | Earlier of the source next-strategy and next-notice-print dates, using SQL LEAST. |
| `prev_n_contacts` | Number of previous contacts. |
| `prev_n_letters` | Number of previous letters. |
| `prev_n_voapps` | Number of previous VOAPPS. |
| `prev_n_texts` | Number of previous texts. |
| `prev_n_emails` | Number of previous emails. |
| `prev_n_inbounds` | Number of previous inbound calls. |
| `prev_n_dialer_agent` | Number of previous agent dialer calls. |
| `prev_n_dialer_agentless` | Number of previous agentless dialer calls. |
| `prev_n_outbound_manual` | Number of previous manual outbound calls. |
| `prev_n_voapps_7` | Number of previous VOAPPS in the recent seven-day window. |
| `prev_n_texts_7` | Number of previous texts in the recent seven-day window. |
| `prev_n_dialer_agent_7` | Number of previous agent dialer calls in the recent seven-day window. |
| `prev_n_dialer_agentless_7` | Number of previous agentless dialer calls in the recent seven-day window. |
| `prev_n_outbound_manual_7` | Number of previous manual outbound calls in the recent seven-day window. |
| `prev_date_contacts` | Most recent date of contacts. |
| `prev_date_letters` | Most recent date of letters. |
| `prev_date_voapps` | Most recent date of VOAPPS. |
| `prev_date_texts` | Most recent date of texts. |
| `prev_date_emails` | Most recent date of emails. |
| `prev_date_inbounds` | Most recent date of inbound calls. |
| `prev_date_dialer_agent` | Most recent date of agent dialer calls. |
| `prev_date_dialer_agentless` | Most recent date of agentless dialer calls. |
| `prev_date_outbound_manual` | Most recent date of manual outbound calls. |
| `prev_date_rpc` | Most recent date of right-party contact. |
| `prev_n_letters_proposed` | Number of previous letter proposals. |
| `prev_n_voapps_proposed` | Number of previous VOAPPS proposals. |
| `prev_n_texts_proposed` | Number of previous text proposals. |
| `prev_n_emails_proposed` | Number of previous email proposals. |
| `prev_n_voapps_7_proposed` | Number of previous VOAPPS proposals in the recent seven-day window. |
| `prev_n_texts_7_proposed` | Number of previous text proposals in the recent seven-day window. |
| `prev_date_contacts_proposed` | Most recent date of contacts proposals. |
| `prev_date_letters_proposed` | Most recent date of letter proposals. |
| `prev_date_voapps_proposed` | Most recent date of VOAPPS proposals. |
| `prev_date_texts_proposed` | Most recent date of text proposals. |
| `prev_date_emails_proposed` | Most recent date of email proposals. |
| `prev_n_dialeragent_proposed` | Number of previous agent dialer call proposals. |
| `prev_n_dialeragentless_proposed` | Number of previous agentless dialer call proposals. |
| `prev_date_dialeragent_proposed` | Most recent date of agent dialer call proposals. |
| `prev_date_dialeragentless_proposed` | Most recent date of agentless dialer call proposals. |
| `prev_n_contacts_postbatch` | Number of previous contacts since the packet's latest placement. |
| `prev_n_letters_postbatch` | Number of previous letters since the packet's latest placement. |
| `prev_n_voapps_postbatch` | Number of previous VOAPPS since the packet's latest placement. |
| `prev_n_texts_postbatch` | Number of previous texts since the packet's latest placement. |
| `prev_n_emails_postbatch` | Number of previous emails since the packet's latest placement. |
| `prev_n_inbounds_postbatch` | Number of previous inbound calls since the packet's latest placement. |
| `prev_n_dialer_agent_postbatch` | Number of previous agent dialer calls since the packet's latest placement. |
| `prev_n_dialer_agentless_postbatch` | Number of previous agentless dialer calls since the packet's latest placement. |
| `prev_n_outbound_manual_postbatch` | Number of previous manual outbound calls since the packet's latest placement. |
| `prev_date_contacts_postbatch` | Most recent date of contacts since the packet's latest placement. |
| `prev_date_letters_postbatch` | Most recent date of letters since the packet's latest placement. |
| `prev_date_voapps_postbatch` | Most recent date of VOAPPS since the packet's latest placement. |
| `prev_date_texts_postbatch` | Most recent date of texts since the packet's latest placement. |
| `prev_date_emails_postbatch` | Most recent date of emails since the packet's latest placement. |
| `prev_date_inbounds_postbatch` | Most recent date of inbound calls since the packet's latest placement. |
| `prev_date_dialer_agent_postbatch` | Most recent date of agent dialer calls since the packet's latest placement. |
| `prev_date_dialer_agentless_postbatch` | Most recent date of agentless dialer calls since the packet's latest placement. |
| `prev_date_outbound_manual_postbatch` | Most recent date of manual outbound calls since the packet's latest placement. |
| `prev_n_letters_proposed_postbatch` | Number of previous letter proposals since the packet's latest placement. |
| `prev_n_voapps_proposed_postbatch` | Number of previous VOAPPS proposals since the packet's latest placement. |
| `prev_n_texts_proposed_postbatch` | Number of previous text proposals since the packet's latest placement. |
| `prev_n_emails_proposed_postbatch` | Number of previous email proposals since the packet's latest placement. |
| `prev_date_contacts_proposed_postbatch` | Most recent date of contacts proposals since the packet's latest placement. |
| `prev_date_letters_proposed_postbatch` | Most recent date of letter proposals since the packet's latest placement. |
| `prev_date_voapps_proposed_postbatch` | Most recent date of VOAPPS proposals since the packet's latest placement. |
| `prev_date_texts_proposed_postbatch` | Most recent date of text proposals since the packet's latest placement. |
| `prev_date_emails_proposed_postbatch` | Most recent date of email proposals since the packet's latest placement. |
| `pass_letters_warmup` | Whether the debtor passes the initial letter waiting-period check. |
| `pass_letters_cooldown_prev_n` | Whether letters pass the prior-contact count limits. |
| `pass_letters_cooldown_prev_date` | Whether letters pass the waiting periods since previous contacts/proposals. |
| `pass_voapps_cooldown_prev_n` | Whether VOAPPS pass the prior-contact count limits. |
| `pass_voapps_cooldown_prev_date` | Whether VOAPPS pass the waiting periods since previous contacts/proposals. |
| `pass_texts_cooldown_prev_n` | Whether texts pass the prior-contact count limits. |
| `pass_texts_cooldown_prev_date` | Whether texts pass the waiting periods since previous contacts/proposals. |
| `pass_emails_cooldown_prev_n` | Whether emails pass the prior-contact count limits. |
| `pass_emails_cooldown_prev_date` | Whether emails pass the waiting periods since previous contacts/proposals. |
| `pass_dialeragent_cooldown_prev_n` | Whether agent dialer calls pass the prior-contact count limits. |
| `pass_dialeragent_cooldown_prev_date` | Whether agent dialer calls pass the waiting periods since previous contacts/proposals. |
| `pass_dialeragentless_cooldown_prev_n` | Whether agentless dialer calls pass the prior-contact count limits. |
| `pass_dialeragentless_cooldown_prev_date` | Whether agentless dialer calls pass the waiting periods since previous contacts/proposals. |
| `pass_letters_cooldown` | Whether letters pass the combined cooldown checks. |
| `pass_voapps_cooldown` | Whether VOAPPS pass the combined cooldown checks. |
| `pass_texts_cooldown` | Whether texts pass the combined cooldown checks. |
| `pass_emails_cooldown` | Whether emails pass the combined cooldown checks. |
| `pass_dialeragent_cooldown` | Whether agent dialer calls pass the combined cooldown checks. |
| `pass_dialeragentless_cooldown` | Whether agentless dialer calls pass the combined cooldown checks. |
| `pass_7in7` | Whether the debtor passes the combined seven-in-seven contact-frequency check. |
