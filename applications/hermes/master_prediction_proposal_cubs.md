# master_prediction_proposal_cubs

Source: [master_prediction_proposal_cubs.sql](../../src/sql/master_prediction_proposal_cubs.sql)

Exposes today's selected CUBS contact recommendations.

| Object | Name |
| --- | --- |
| View | `edwprodhh.hermes.master_prediction_proposal_cubs` |
| View | `edwprodhh.hermes.master_prediction_proposal_cubs_hh` |
| View | `edwprodhh.hermes.master_prediction_proposal_cubs_co` |
| View | `edwprodhh.hermes.master_prediction_proposal_cubs_dc` |
| View | `edwprodhh.hermes.master_prediction_proposal_cubs_chi` |
| View | `edwprodhh.hermes.master_prediction_proposal_cubs_pre` |
| View | `edwprodhh.hermes.master_prediction_proposal_cubs_tol` |
| Table | None defined; this file defines views. |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_proposal_log`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.pub_jchang.master_plgroup_map`.

**Logic:**

1. Reads selected proposal-log rows with today's upload date.
2. Renames text contacts to `Texts` and appends the uppercase template to text/letter/email channel labels when a template exists.
3. Joins CUBS debtor identifiers and excludes placement groups with a Latitude migration date.
4. Defines separate HH, CO, DC, CHI, PRE, and TOL views with the same three columns.

## Output columns

`edwprodhh.hermes.master_prediction_proposal_cubs`, `edwprodhh.hermes.master_prediction_proposal_cubs_hh`, `edwprodhh.hermes.master_prediction_proposal_cubs_co`, `edwprodhh.hermes.master_prediction_proposal_cubs_dc`, `edwprodhh.hermes.master_prediction_proposal_cubs_chi`, `edwprodhh.hermes.master_prediction_proposal_cubs_pre`, `edwprodhh.hermes.master_prediction_proposal_cubs_tol`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `debtornumber` | Account number in the source system. |
| `proposed_channel` | Contact channel associated with a candidate, recommendation, or requirement. |
