# master_prediction_scores_transformation_cubs

Source: [master_prediction_scores_transformation_cubs.sql](../../src/sql/master_prediction_scores_transformation_cubs.sql)

Exposes CUBS-oriented score and treatment fields through a family of views.

| Object | Name |
| --- | --- |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs` |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_hh` |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_co` |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_dc` |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_chi` |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_pre` |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_tol` |
| View | `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtorval_hh` |
| Table | None defined; this file defines views. |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_prediction_scores_transformation`, `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimdebtor`.

**Logic:**

1. Joins transformed debtor scores to debtor and CUBS dimension data; maps local/global debtor deciles to the export fields.
2. Uses the rounded median local decile within a packet to assign `GRP1` through `GRP4`.
3. Sets treatment labels to `TEST` and validation expiration to placement date plus ten days.
4. Defines six logon-specific debtor views and an HH validation view with their respective column subsets. These are live views over the current transformation table.

## Output columns

`edwprodhh.hermes.master_prediction_scores_transformation_cubs`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `packet` | CUBS packet identifier. |
| `debtornumber` | Account number in the source system. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `local` | Placement-group debtor-score decile exposed in the CUBS view. |
| `global` | Global debtor-score decile exposed in the CUBS view. |
| `equabli_treatment_group` | CUBS treatment-group label; currently TEST. |
| `dialergrp` | GRP1â€“GRP4 derived from the packet's rounded median local debtor-score decile. |
| `equabli_validation_treatment_group` | CUBS validation treatment-group label; currently TEST. |
| `equabli_validation_expiration_date` | Placement date plus ten days for the CUBS validation export. |

`edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_hh`, `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_co`, `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_dc`, `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_chi`, `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_pre`, `edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtor_tol`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `packet` | CUBS packet identifier. |
| `debtornumber` | Account number in the source system. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `local` | Placement-group debtor-score decile exposed in the CUBS view. |
| `global` | Global debtor-score decile exposed in the CUBS view. |
| `equabli_treatment_group` | CUBS treatment-group label; currently TEST. |
| `dialergrp` | GRP1â€“GRP4 derived from the packet's rounded median local debtor-score decile. |

`edwprodhh.hermes.master_prediction_scores_transformation_cubs_debtorval_hh`:

| Column | Meaning |
| --- | --- |
| `logon` | CUBS business-unit/logon code, such as HH, CO, or TOL. |
| `packet` | CUBS packet identifier. |
| `debtornumber` | Account number in the source system. |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `local` | Placement-group debtor-score decile exposed in the CUBS view. |
| `global` | Global debtor-score decile exposed in the CUBS view. |
| `equabli_validation_treatment_group` | CUBS validation treatment-group label; currently TEST. |
| `equabli_validation_expiration_date` | Placement date plus ten days for the CUBS validation export. |
