# transform_businessrules_debtor_maturity

Source: [transform_businessrules_debtor_maturity.sql](../../src/sql/transform_businessrules_debtor_maturity.sql)

Calculates account ages and the age-related eligibility checks.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_debtor_maturity` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_debtor_maturity()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_debtor_maturity` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimfiscal_chi_b`, `edwprodhh.dw.dimfiscal_co_c`, `edwprodhh.dw.dimfiscal_dc_c`, `edwprodhh.dw.dimfiscal_hh_a`, `edwprodhh.dw.dimfiscal_hh_b`, `edwprodhh.dw.dimfiscal_hh_c`, `edwprodhh.dw.dimfiscal_tol_c`, `edwprodhh.hermes.master_config_treatment_router`, `edwprodhh.pub_jchang.master_client`, `edwprodhh.hermes.master_config_scorecard_priority`.

**Logic:**

1. Computes placement age, debt age, age since the latest placement in the packet, and service age using fiscal dates with fallback dates.
2. Agent-dialer packet age is limited to `545` days and the general packet-age check to `730` days.
3. Placement eligibility applies group-specific recalls/date cutoffs, utility turn-off ages, and CUBS FDCPA service-age restrictions. Scorecard eligibility compares placement months with configured `scorecard_months`.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_businessrules_debtor_maturity`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `age_placement` | Days from placement to the current date. |
| `age_debt` | Days since charge-off/last-charge date, falling back to placement date. |
| `age_packet` | Days since the most recent placement in the packet. |
| `age_date_of_service` | Days since the selected service/admission/discharge date, with debt/placement-date fallbacks. |
| `pass_debtor_age_dialeragent` | Whether the debtor passes the agent-dialer packet-age limit. |
| `pass_debtor_age_placement` | Whether the debtor passes the placement/service-age restrictions and client exceptions. |
| `pass_debtor_age_packet` | Whether the debtor passes the general packet-age limit. |
| `pass_debtor_age_scorecard` | Whether the debtor passes the configured scorecard placement-age window. |
