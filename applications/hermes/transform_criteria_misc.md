# transform_criteria_misc

Source: [transform_criteria_misc.sql](../../src/sql/transform_criteria_misc.sql)

Applies additional placement-group-specific channel checks.

| Object | Name |
| --- | --- |
| Table written (existing) | `edwprodhh.hermes.transform_criteria_misc` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_misc()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_misc` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_contacts`.

**Logic:**

1. Calculates active packet size and last contact dates.
2. For Bay Area Toll Authority letters, rejects packets with at least `95` active accounts, backlog placements, or a last letter date on/after 90 days before placement.
3. Other groups pass the letter check, and the other five channel flags are currently fixed at `1`.
4. Builds a temporary result, truncates the existing output table, and inserts the named columns.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_misc`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `pass_misc_letters` | Whether letters pass the additional client-specific checks. |
| `pass_misc_texts` | Whether texts pass the additional client-specific checks. |
| `pass_misc_voapps` | Whether VOAPPS pass the additional client-specific checks. |
| `pass_misc_emails` | Whether emails pass the additional client-specific checks. |
| `pass_misc_dialeragent` | Whether agent dialer calls pass the additional client-specific checks. |
| `pass_misc_dialeragentless` | Whether agentless dialer calls pass the additional client-specific checks. |
