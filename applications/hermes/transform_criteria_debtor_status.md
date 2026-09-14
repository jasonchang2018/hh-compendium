# transform_criteria_debtor_status

Source: [transform_criteria_debtor_status.sql](../../src/sql/transform_criteria_debtor_status.sql)

Evaluates source-system account status and whether the debtor is active for Hermes.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_criteria_debtor_status` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_criteria_debtor_status()` |
| Task | `edwprodhh.hermes.replace_transform_criteria_debtor_status` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.dw.dimdebtor`, `edwprodhh.pub_jchang.transform_debtor_latitude`, `edwprodhh.hermes.master_config_blocked_accounts`.

**Logic:**

1. Uses different allowed statuses for CUBS and Latitude, with specific TPL desk/status exceptions.
2. Blocks explicitly listed accounts before applying active status, placement-date, desk, and client/group exclusions.
3. Returns separate status and active flags so downstream eligibility can require both.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

`pass_*` fields record individual pass/fail checks; `is_priority_*` fields identify contact priorities. The prediction pool combines the applicable checks into final channel eligibility.

## Output columns

`edwprodhh.hermes.transform_criteria_debtor_status`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `status` | Account status code from the source system. |
| `cancel_dt` | Account cancellation date/time from the source system. |
| `balance_dimdebtor` | Current debtor balance from the source debtor data. |
| `pass_debtor_status` | Whether the debtor passes the source-system allowed-status checks. |
| `pass_debtor_active` | Whether the debtor passes the active-account, placement, desk, and blocked-account checks. |
