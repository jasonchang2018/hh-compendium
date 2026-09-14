# master_prediction_pool

Source: [master_prediction_pool.sql](../../src/sql/master_prediction_pool.sql)

Combines debtor attributes, rule results, and channel eligibility into the central prediction dataset.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.master_prediction_pool` |
| Stored procedure | `edwprodhh.hermes.calculate_master_prediction_pool()` |
| Task | `edwprodhh.hermes.replace_master_prediction_pool` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_transform_businessrules_contact_cooldown`
- `edwprodhh.hermes.replace_transform_businessrules_contact_priority_minimums`
- `edwprodhh.hermes.replace_transform_businessrules_contact_priority_delay`
- `edwprodhh.hermes.replace_transform_businessrules_debtor_balance`
- `edwprodhh.hermes.replace_transform_businessrules_debtor_maturity`
- `edwprodhh.hermes.replace_transform_businessrules_debtor_income`
- `edwprodhh.hermes.replace_transform_businessrules_debtor_debttype`
- `edwprodhh.hermes.replace_transform_businessrules_debtor_prevpacket`
- `edwprodhh.hermes.replace_transform_criteria_validation_eligibility`
- `edwprodhh.hermes.replace_transform_criteria_validation_requirement`
- `edwprodhh.hermes.replace_transform_criteria_sequence_requirement`
- `edwprodhh.hermes.replace_transform_criteria_calendar_requirement`
- `edwprodhh.hermes.replace_transform_criteria_debtor_status`
- `edwprodhh.hermes.replace_transform_criteria_debtor_state`
- `edwprodhh.hermes.replace_transform_criteria_debtor_client_active`
- `edwprodhh.hermes.replace_transform_criteria_phone_allowed`
- `edwprodhh.hermes.replace_transform_criteria_address_allowed_mail`
- `edwprodhh.hermes.replace_transform_criteria_address_allowed_email`
- `edwprodhh.hermes.replace_transform_criteria_misc`
- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.transform_criteria_debtor_client_active`, `edwprodhh.hermes.transform_criteria_debtor_status`, `edwprodhh.hermes.transform_criteria_debtor_state`, `edwprodhh.hermes.transform_criteria_validation_eligibility`, `edwprodhh.hermes.transform_criteria_validation_requirement`, `edwprodhh.hermes.transform_criteria_settlement_calculation`, `edwprodhh.hermes.transform_criteria_sequence_requirement`, `edwprodhh.hermes.transform_criteria_calendar_requirement`, `edwprodhh.hermes.transform_criteria_address_allowed_email`, `edwprodhh.hermes.transform_criteria_address_allowed_mail`, `edwprodhh.hermes.transform_criteria_phone_allowed`, `edwprodhh.hermes.transform_businessrules_contact_cooldown`, `edwprodhh.hermes.transform_businessrules_contact_priority_minimums`, `edwprodhh.hermes.transform_businessrules_contact_priority_delay`, `edwprodhh.hermes.transform_businessrules_debtor_balance`, `edwprodhh.hermes.transform_businessrules_debtor_income`, `edwprodhh.hermes.transform_businessrules_debtor_maturity`, `edwprodhh.hermes.transform_businessrules_debtor_debttype`, `edwprodhh.hermes.transform_businessrules_debtor_prevpacket`, `edwprodhh.hermes.transform_criteria_misc`, `edwprodhh.hermes.master_config_treatment_router`, `edwprodhh.hermes.master_config_plgroup`, `edwprodhh.pub_jchang.master_plgroup_map`.

**Logic:**

1. Keeps configured placement groups with placement dates from today minus 1,460 days through today; requires active debtors except for TPL, and uses Latitude records for migrated groups. Inner joins the criteria, business-rule, and treatment results, so a missing result excludes that debtor.
2. Computes separate eligibility flags for letters, texts, VOAPPS, emails, agent calls, agentless calls, and validation channels. The required checks differ by channel and include explicit client/template exceptions.
3. `is_eligible_debtor` requires passing status and active checks. `needs_letters_val_score` is a separate flag and does not require that validation has never been received.
4. Truncates the existing pool table and inserts the explicitly named columns. The output preserves the diagnostic fields used to explain eligibility; scoring-pool filtering happens downstream.

## Output columns

`edwprodhh.hermes.master_prediction_pool`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `treatment_group` | Assigned experiment treatment group; currently null in the treatment router. |
| `treatment_description` | Description of the assigned treatment; currently null in the treatment router. |
| `test_name` | Experiment name; currently null in the treatment router. |
| `test_description` | Experiment description; currently null in the treatment router. |
| `pass_client_active_hermes_contacts` | Whether the debtor passes the client activation and ALL-exclusion checks. |
| `status` | Account status code from the source system. |
| `cancel_dt` | Account cancellation date/time from the source system. |
| `pass_debtor_status` | Whether the debtor passes the source-system allowed-status checks. |
| `pass_debtor_active` | Whether the debtor passes the active-account, placement, desk, and blocked-account checks. |
| `pass_client_allowed_letters_val` | Whether client configuration and exclusions permit validation letters. |
| `pass_client_allowed_letters` | Whether client configuration and exclusions permit letters. |
| `pass_client_allowed_texts` | Whether client configuration and exclusions permit texts. |
| `pass_client_allowed_voapps` | Whether client configuration and exclusions permit VOAPPS. |
| `pass_client_allowed_emails` | Whether client configuration and exclusions permit emails. |
| `pass_client_allowed_calls_dialeragent` | Whether client configuration and exclusions permit agent dialer calls. |
| `pass_client_allowed_calls_dialeragentless` | Whether client configuration and exclusions permit agentless dialer calls. |
| `pass_client_allowed_calls_dialeragentless_stamp` | Whether client configuration and exclusions permit agentless dialer stamping. |
| `requires_validation` | Whether the account is subject to the SQL validation requirement. |
| `pass_received_validation` | Whether the debtor passes the validation receipt check. |
| `pass_validation_age_nonoffer` | Whether the debtor-level validation waiting period has elapsed for nonoffer contacts. |
| `pass_validation_age_offer` | Whether the debtor-level validation waiting period has elapsed for offer contacts. |
| `pass_validation_age_dialer` | Whether the debtor-level validation waiting period has elapsed for dialer contacts. |
| `pass_validation_requirement_debtor_nonoffer` | Whether the debtor-level combined validation requirement passes for nonoffer contacts. |
| `pass_validation_requirement_debtor_offer` | Whether the debtor-level combined validation requirement passes for offer contacts. |
| `pass_validation_requirement_debtor_dialer` | Whether the debtor-level combined validation requirement passes for dialer contacts. |
| `pass_validation_requirement_nonoffer` | Whether the packet-level combined validation requirement passes for nonoffer contacts. |
| `pass_validation_requirement_offer` | Whether the packet-level combined validation requirement passes for offer contacts. |
| `pass_validation_requirement_dialer` | Whether the packet-level combined validation requirement passes for dialer contacts. |
| `validation_letter_date` | Validation date selected from the available contact/source-system history. |
| `email_address` | Email address; the address-eligibility output may contain a semicolon-separated list of usable addresses. |
| `pass_address_emails` | Whether the debtor passes the usable-email, permission, opt-out, and bounce checks. |
| `client_evalidation_status` | Indicator for the HH FDCPA client e-validation configuration; 1 when the configured status matches eVAL. |
| `is_emailable` | Source/fiscal permission to email the debtor, before the other address and opt-out checks. |
| `mailing_address` | Debtor mailing street address. |
| `mailing_city` | Debtor mailing city. |
| `mailing_state` | Debtor mailing state. |
| `mailing_zip_code` | Debtor mailing ZIP/postal code. |
| `pass_address_letters` | Whether the debtor passes the mail-address validity and applicable client-specific restrictions. |
| `valid_phone_number_voapps` | Semicolon-separated distinct phone numbers passing all VOAPPS checks; null when none qualify. |
| `valid_phone_number_texts` | Semicolon-separated distinct phone numbers passing all texts checks; null when none qualify. |
| `valid_phone_number_dialer` | Semicolon-separated distinct phone numbers passing all dialer calls checks; null when none qualify. |
| `phone_number_debtor` | Primary debtor phone number copied from source data. |
| `invalid_phone_number_dialer_dnc` | Semicolon-separated dialer calls phone numbers failing the do-not-call check. |
| `invalid_phone_number_dialer_optout` | Semicolon-separated dialer calls phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_dialer_unavailable` | Semicolon-separated dialer calls phone numbers failing the source-system availability check. |
| `invalid_phone_number_voapps_dnc` | Semicolon-separated VOAPPS phone numbers failing the do-not-call check. |
| `invalid_phone_number_voapps_optout` | Semicolon-separated VOAPPS phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_voapps_cell` | Semicolon-separated VOAPPS phone numbers failing the cell-phone status check. |
| `invalid_phone_number_voapps_consent` | Semicolon-separated VOAPPS phone numbers failing the consent check. |
| `invalid_phone_number_voapps_bounces` | Semicolon-separated VOAPPS phone numbers failing the bounce-history check. |
| `invalid_phone_number_voapps_available` | Semicolon-separated VOAPPS phone numbers failing the source-system availability check. |
| `invalid_phone_number_voapps_ruleof3` | Semicolon-separated VOAPPS phone numbers failing the three-message limit check. |
| `invalid_phone_number_voapps_areacode` | Semicolon-separated VOAPPS phone numbers failing the area-code geography check. |
| `invalid_phone_number_texts_dnc` | Semicolon-separated texts phone numbers failing the do-not-call check. |
| `invalid_phone_number_texts_optout` | Semicolon-separated texts phone numbers failing the opt-out/FCC check. |
| `invalid_phone_number_texts_cell` | Semicolon-separated texts phone numbers failing the cell-phone status check. |
| `invalid_phone_number_texts_consent` | Semicolon-separated texts phone numbers failing the consent check. |
| `invalid_phone_number_texts_bounces` | Semicolon-separated texts phone numbers failing the bounce-history check. |
| `invalid_phone_number_texts_available` | Semicolon-separated texts phone numbers failing the source-system availability check. |
| `invalid_phone_number_texts_sol` | Semicolon-separated texts phone numbers failing the placement-age/business-class check. |
| `cell_code_debtor` | Debtor cell code; retained as a legacy placeholder and currently set to NULL. |
| `cell_code_packet_agg` | Aggregated packet cell codes; retained as a legacy placeholder and currently set to NULL. |
| `cell_code_packet_factorized` | Factorized packet cell code; retained as a legacy placeholder and currently set to NULL. |
| `cell_code_packet` | Packet cell code; retained as a legacy placeholder and currently set to NULL. |
| `phone_number_source` | Phone source; retained as a legacy placeholder and currently set to NULL. |
| `current_status_phone` | Current phone status; retained as a legacy placeholder and currently set to NULL. |
| `commercial_code` | Commercial classification code from debtor fiscal data. |
| `state` | Debtor state used in geographic eligibility checks. |
| `is_fdcpa` | Source client flag indicating whether FDCPA-specific rule branches apply. |
| `ash_cli` | Client ASH_CLI attribute carried from the source client table. |
| `payplan` | Existing payment-plan value from the debtor source. |
| `pass_phone_voapps` | Whether VOAPPS pass the debtor-level phone eligibility checks. |
| `pass_phone_texts` | Whether texts pass the debtor-level phone eligibility checks. |
| `pass_phone_dialeragent` | Whether agent dialer calls pass the debtor-level phone eligibility checks. |
| `pass_phone_dialeragentless` | Whether agentless dialer calls pass the debtor-level phone eligibility checks. |
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
| `pass_delay_letters` | Whether letters pass the initial placement delay. |
| `pass_delay_texts` | Whether texts pass the initial placement delay. |
| `pass_delay_voapps` | Whether VOAPPS pass the initial placement delay. |
| `pass_delay_emails` | Whether emails pass the initial placement delay. |
| `pass_delay_dialeragent` | Whether agent dialer calls pass the initial placement delay. |
| `pass_delay_dialeragentless` | Whether agentless dialer calls pass the initial placement delay. |
| `assigned` | Original assigned account amount. |
| `balance_dimdebtor` | Current debtor balance from the source debtor data. |
| `balance_dimdebtor_packet` | Sum of debtor balances across the packet. |
| `pass_debtor_balance` | Whether the debtor passes the minimum debtor-balance check. |
| `pass_packet_balance` | Whether the debtor passes the minimum packet-balance check. |
| `pass_packet_balance_dialeragent` | Whether the debtor passes the agent-dialer packet-balance threshold. |
| `pass_debtor_assigned` | Whether the debtor passes the positive assigned-amount check. |
| `experian_score` | Experian score; retained as a legacy placeholder and currently set to NULL. |
| `pass_debtor_experian` | Experian eligibility check; retained as a legacy placeholder and currently set to NULL. |
| `median_household_income` | ZIP-code median household income joined to the debtor. |
| `pass_debtor_income` | Whether the debtor passes the placement-group-specific income threshold (missing income passes). |
| `has_previous_payment` | Whether a payment transaction exists anywhere in the packet. |
| `debtor_is_first_in_packet` | First-debtor-in-packet indicator; retained as a legacy placeholder and currently set to NULL. |
| `has_other_placement` | Whether more than one debtor row shares the packet. |
| `last_payment_date` | Last payment date; retained as a legacy placeholder and currently set to NULL. |
| `pass_contraints_packet_last_payment` | Packet last-payment check; retained as a legacy placeholder and currently set to NULL. |
| `desk_team_name` | Desk/team name; retained as a legacy placeholder and currently set to NULL. |
| `pass_existing_payplan` | Existing payment-plan check; retained as a legacy placeholder and currently set to NULL. |
| `age_placement` | Days from placement to the current date. |
| `age_debt` | Days since charge-off/last-charge date, falling back to placement date. |
| `age_packet` | Days since the most recent placement in the packet. |
| `age_date_of_service` | Days since the selected service/admission/discharge date, with debt/placement-date fallbacks. |
| `pass_debtor_age_dialeragent` | Whether the debtor passes the agent-dialer packet-age limit. |
| `pass_debtor_age_placement` | Whether the debtor passes the placement/service-age restrictions and client exceptions. |
| `pass_debtor_age_packet` | Whether the debtor passes the general packet-age limit. |
| `pass_debtor_age_scorecard` | Whether the debtor passes the configured scorecard placement-age window. |
| `tax_year` | Tax year; retained as a legacy placeholder and currently set to NULL. |
| `pass_debtor_tax_year` | Tax-year check; retained as a legacy placeholder and currently set to NULL. |
| `debt_type` | Source debt-type classification. |
| `party` | Placement/collection-party designation, such as 1P, 3P, or 3P-2. |
| `is_debttype_gov_parking` | Whether debt type or industry detail identifies parking debt. |
| `is_debttype_gov_toll` | Whether debt type or industry detail identifies toll debt. |
| `is_debttype_gov_traffic` | Whether debt type or industry detail identifies traffic debt. |
| `is_debttype_gov_tax` | Whether debt type or industry detail identifies tax debt. |
| `is_debttype_gov_backlog` | Whether explicit client/placement rules or debt type classify the account as backlog; not restricted to government debt. |
| `is_debttype_hc_ai` | Whether the debtor has healthcare industry and debt-type code AI. |
| `is_debttype_hc_sp` | Whether the debtor has healthcare industry and debt-type code SP. |
| `is_debttype_hc_medicare` | Whether the debtor has healthcare industry and debt-type code MEDICARE. |
| `is_debttype_hc_parent` | Whether the debtor has healthcare industry and debt-type code PARENT. |
| `is_department_ems` | Whether the placement group maps to the emergency medical services department. |
| `is_department_hc` | Whether the placement group maps to the healthcare department. |
| `is_department_muni` | Whether the placement group maps to the municipal department. |
| `is_department_state` | Whether the placement group maps to the state department. |
| `is_department_county` | Whether the placement group maps to the county department. |
| `is_department_telecom` | Whether the placement group maps to the telecommunications department. |
| `is_department_utl` | Whether the placement group maps to the utilities department. |
| `is_prime` | Whether the placement party is 3P. |
| `is_second` | Whether the placement party is 3P-2. |
| `is_tertiary` | Whether the placement party is 3P-3. |
| `is_quad` | Whether the placement party is 3P-4. |
| `is_commercial` | Whether the debtor is classified as commercial under the SQL rules. |
| `pass_state_letters` | Whether letters pass the geographic restrictions. |
| `pass_state_texts` | Whether texts pass the geographic restrictions. |
| `pass_state_voapps` | Whether VOAPPS pass the geographic restrictions. |
| `pass_state_emails` | Whether emails pass the geographic restrictions. |
| `pass_state_dialeragent` | Whether agent dialer calls pass the geographic restrictions. |
| `pass_state_dialeragentless` | Whether agentless dialer calls pass the geographic restrictions. |
| `match_client_state` | Whether the debtor state matches the aggregated client-state mapping. |
| `pass_debtor_first_score_dialer_agent` | Initial agent-dialer score check; retained as a legacy placeholder and currently set to NULL. |
| `template_letters` | Template chosen by sequence rules for letters. |
| `template_letters_priority` | Priority indicator attached to the selected letters template. |
| `template_texts` | Template chosen by sequence rules for texts. |
| `template_texts_priority` | Priority indicator attached to the selected texts template. |
| `template_voapps` | Template chosen by sequence rules for VOAPPS. |
| `template_voapps_priority` | Priority indicator attached to the selected VOAPPS template. |
| `template_emails` | Template chosen by sequence rules for emails. |
| `template_emails_priority` | Priority indicator attached to the selected emails template. |
| `text_type` | Text message format used for template/cost handling, such as SMS or MMS. |
| `min_sif_remaining` | Minimum allowed remaining-payment fraction, e.g. 0.50 for 50%, from client/age settlement rules. |
| `sif_chance_cutoff` | Probability cutoff used to decide whether to introduce a new settlement offer. |
| `sif_amount_raw` | Sampled remaining-payment percentage before final settlement/proposal checks. |
| `propose_as_sif` | Whether the SQL selects a settlement offer after validation, balance, and history checks. |
| `proposed_sif_amount` | Final proposed remaining-payment percentage as an integer; null when no settlement is proposed. |
| `is_priority_calendar_requirement` | Whether a configured calendar contact is due and not already satisfied. |
| `channel_calendar_requirement` | Channel required by the due calendar rule; null when no calendar priority applies. |
| `can_receive_validation_letter` | Whether a new validation letter is allowed; currently restricted to the eligible NTTA backlog case. |
| `can_receive_validation_email` | Whether a validation email is allowed; currently fixed at 0. |
| `can_receive_validation_text` | Whether a validation text is allowed; currently fixed at 0. |
| `pass_misc_letters` | Whether letters pass the additional client-specific checks. |
| `pass_misc_texts` | Whether texts pass the additional client-specific checks. |
| `pass_misc_voapps` | Whether VOAPPS pass the additional client-specific checks. |
| `pass_misc_emails` | Whether emails pass the additional client-specific checks. |
| `pass_misc_dialeragent` | Whether agent dialer calls pass the additional client-specific checks. |
| `pass_misc_dialeragentless` | Whether agentless dialer calls pass the additional client-specific checks. |
| `is_eligible_letters` | Whether the debtor is eligible for letters. |
| `is_eligible_texts` | Whether the debtor is eligible for texts. |
| `is_eligible_voapps` | Whether the debtor is eligible for VOAPPS. |
| `is_eligible_emails` | Whether the debtor is eligible for emails. |
| `is_eligible_dialer_agent` | Whether the debtor is eligible for agent dialer calls. |
| `is_eligible_dialer_agentless` | Whether the debtor is eligible for agentless dialer calls. |
| `is_eligible_debtor` | Whether the debtor passes the basic account-status and active-account checks. |
| `is_eligible_letters_val` | Whether the debtor is eligible for validation letters. |
| `is_eligible_emails_val` | Whether the debtor is eligible for validation emails. |
| `is_eligible_texts_val` | Whether the debtor is eligible for validation texts. |
| `needs_letters_val_score` | Whether the account meets the criteria for calculating a validation-letter score. |
