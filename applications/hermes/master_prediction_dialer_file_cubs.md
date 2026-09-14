# master_prediction_dialer_file_cubs

Source: [master_prediction_dialer_file_cubs.sql](../../src/sql/master_prediction_dialer_file_cubs.sql)

Exposes today's selected CUBS dialer records and logon-specific views.

| Object | Name |
| --- | --- |
| View | `edwprodhh.hermes.master_prediction_dialer_file_cubs` |
| View | `edwprodhh.hermes.master_prediction_dialer_file_cubs_hh` |
| View | `edwprodhh.hermes.master_prediction_dialer_file_cubs_co` |
| View | `edwprodhh.hermes.master_prediction_dialer_file_cubs_dc` |
| View | `edwprodhh.hermes.master_prediction_dialer_file_cubs_chi` |
| View | `edwprodhh.hermes.master_prediction_dialer_file_cubs_pre` |
| View | `edwprodhh.hermes.master_prediction_dialer_file_cubs_tol` |
| Table | None defined; this file defines views. |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_dialer_file_log`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_plgroup_map`.

**Logic:**

1. Reads selected dialer log rows whose upload date is today and joins CUBS debtor identifiers.
2. Excludes placement groups with a recorded Latitude migration date.
3. Maps agent calls to campaign type `A` and agentless calls to `U`; emits the configured phone, subteam, priority, and phone-source fields.
4. Defines HH, CO, DC, CHI, PRE, and TOL views using the same output columns filtered by logon.

## Output columns

`edwprodhh.hermes.master_prediction_dialer_file_cubs`, `edwprodhh.hermes.master_prediction_dialer_file_cubs_hh`, `edwprodhh.hermes.master_prediction_dialer_file_cubs_co`, `edwprodhh.hermes.master_prediction_dialer_file_cubs_dc`, `edwprodhh.hermes.master_prediction_dialer_file_cubs_chi`, `edwprodhh.hermes.master_prediction_dialer_file_cubs_pre`, `edwprodhh.hermes.master_prediction_dialer_file_cubs_tol`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `debtornumber` | Account number in the source system. |
| `phone` | Candidate or selected telephone number, depending on the output. |
| `subteam` | Dialer group/department supplied to the destination system; null for non-dialer rows. |
| `campaigntype` | CUBS campaign code: A for agent calls or U for agentless calls. |
| `priority` | Dialer order assigned from a randomized sorter biased by time zone; lower numbers are earlier. |
| `phone_field` | Source field associated with the selected dialer phone. |
| `phone_pkt_member` | Packet member associated with the selected dialer phone. |
