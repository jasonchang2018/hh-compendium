# master_config_plgroup_autobudget

Source: [master_config_plgroup_autobudget.sql](../../src/sql/master_config_plgroup_autobudget.sql)

Estimates contact spending capacity from the current eligible packet population.

| Object | Name |
| --- | --- |
| View | `edwprodhh.hermes.master_config_plgroup_autobudget` |
| Table | None defined; this file defines views. |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_config_channel_costs`, `edwprodhh.hermes.master_prediction_pool`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.transform_config_artificialgroup_associations`, `edwprodhh.hermes.master_config_artificialgroup`.

**Logic:**

1. Pivots channel costs and joins the prediction pool to debtor and artificial-group mappings.
2. Groups by artificial group when configured, otherwise by placement group.
3. Counts distinct packets that pass the channel-specific checks, then multiplies by channel cost. Texts, VOAPPS, and emails include a `1.20` multiplier; texts use SMS/MMS costs.
4. These are estimates from a selected set of eligibility checks, not sums of final proposed contacts.

## Output columns

`edwprodhh.hermes.master_config_plgroup_autobudget`:

| Column | Meaning |
| --- | --- |
| `hermes_group` | Group used for allocation; a placement/artificial group for ordinary proposals or a dialer department for calls. |
| `dol_eligible_letters` | Estimated cost capacity from qualifying distinct packets for letters. |
| `dol_eligible_texts` | Estimated cost capacity from qualifying distinct packets for texts. |
| `dol_eligible_voapps` | Estimated cost capacity from qualifying distinct packets for VOAPPS. |
| `dol_eligible_emails` | Estimated cost capacity from qualifying distinct packets for emails. |
