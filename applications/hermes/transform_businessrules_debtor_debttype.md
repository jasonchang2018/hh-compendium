# transform_businessrules_debtor_debttype

Source: [transform_businessrules_debtor_debttype.sql](../../src/sql/transform_businessrules_debtor_debttype.sql)

Builds debt-type, department, placement-tier, backlog, and commercial features.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_businessrules_debtor_debttype` |
| Stored procedure | `edwprodhh.hermes.calculate_transform_businessrules_debtor_debttype()` |
| Task | `edwprodhh.hermes.replace_transform_businessrules_debtor_debttype` |

The task uses `hermes_wh` and runs after all of these declared predecessors:

- `edwprodhh.hermes.replace_master_config_treatment_router`

It calls the stored procedure.

**Inputs:** `edwprodhh.pub_jchang.master_debtor`, `edwprodhh.hermes.master_config_treatment_router`, `edwprodhh.pub_jchang.master_plgroup_map`.

**Logic:**

1. Maps debt type, industry detail, and party into binary indicator columns.
2. Identifies backlog using explicit client/group/placement rules or `debt_type = 'BACKLOG'`; the retained `gov` column name does not restrict it to government accounts.
3. Classifies commercial accounts using the source business flag and a categorization function, with healthcare/EMS exclusions and a nonblank-name requirement.

The procedure rebuilds its output table with `CREATE OR REPLACE TABLE ... AS SELECT`.

## Output columns

`edwprodhh.hermes.transform_businessrules_debtor_debttype`:

| Column | Meaning |
| --- | --- |
| `debtor_idx` | Unique debtor/account identifier. |
| `debt_type` | Source debt-type classification. |
| `party` | Placement/collection-party designation, such as 1P, 3P, or 3P-2. |
| `is_debttype_hc_ai` | Whether the debtor has healthcare industry and debt-type code AI. |
| `is_debttype_hc_sp` | Whether the debtor has healthcare industry and debt-type code SP. |
| `is_debttype_hc_medicare` | Whether the debtor has healthcare industry and debt-type code MEDICARE. |
| `is_debttype_hc_parent` | Whether the debtor has healthcare industry and debt-type code PARENT. |
| `is_debttype_gov_traffic` | Whether debt type or industry detail identifies traffic debt. |
| `is_debttype_gov_tax` | Whether debt type or industry detail identifies tax debt. |
| `is_department_county` | Whether the placement group maps to the county department. |
| `is_department_ems` | Whether the placement group maps to the emergency medical services department. |
| `is_department_hc` | Whether the placement group maps to the healthcare department. |
| `is_department_muni` | Whether the placement group maps to the municipal department. |
| `is_debttype_gov_parking` | Whether debt type or industry detail identifies parking debt. |
| `is_department_state` | Whether the placement group maps to the state department. |
| `is_department_telecom` | Whether the placement group maps to the telecommunications department. |
| `is_debttype_gov_toll` | Whether debt type or industry detail identifies toll debt. |
| `is_department_utl` | Whether the placement group maps to the utilities department. |
| `is_prime` | Whether the placement party is 3P. |
| `is_second` | Whether the placement party is 3P-2. |
| `is_tertiary` | Whether the placement party is 3P-3. |
| `is_quad` | Whether the placement party is 3P-4. |
| `is_debttype_gov_backlog` | Whether explicit client/placement rules or debt type classify the account as backlog; not restricted to government debt. |
| `is_commercial` | Whether the debtor is classified as commercial under the SQL rules. |
