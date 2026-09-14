# master_config_templates_plgroup

Source: [master_config_templates_plgroup.sql](../../src/sql/master_config_templates_plgroup.sql)

Defines enabled templates by placement group and exposes them as a normalized view.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_templates_plgroup_long` |
| View | `edwprodhh.hermes.master_config_templates_plgroup` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.hermes.master_config_templates`.

**Logic:**

1. Creates and reloads `master_config_templates_plgroup_long`, with one row per placement group and a separate enablement column for each template identifier.
2. The `master_config_templates_plgroup` view unpivots the template columns, keeps `is_enabled = 1`, and joins the template catalog for channel names.
3. The view outputs one enabled placement-group/template mapping per row.

## Output columns

`edwprodhh.hermes.master_config_templates_plgroup_long`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `sbt_98` | Enablement flag for template `SBT_98`; the normalized view retains mappings with value 1. |
| `sbt_110` | Enablement flag for template `SBT_110`; the normalized view retains mappings with value 1. |
| `sbt_117` | Enablement flag for template `SBT_117`; the normalized view retains mappings with value 1. |
| `sbt_116` | Enablement flag for template `SBT_116`; the normalized view retains mappings with value 1. |
| `sbt_99` | Enablement flag for template `SBT_99`; the normalized view retains mappings with value 1. |
| `sbt_133` | Enablement flag for template `SBT_133`; the normalized view retains mappings with value 1. |
| `sbt_141` | Enablement flag for template `SBT_141`; the normalized view retains mappings with value 1. |
| `sbt_142` | Enablement flag for template `SBT_142`; the normalized view retains mappings with value 1. |
| `sbt_136` | Enablement flag for template `SBT_136`; the normalized view retains mappings with value 1. |
| `sbt_137` | Enablement flag for template `SBT_137`; the normalized view retains mappings with value 1. |
| `sbt_138` | Enablement flag for template `SBT_138`; the normalized view retains mappings with value 1. |
| `sbt_139` | Enablement flag for template `SBT_139`; the normalized view retains mappings with value 1. |
| `sbt_97` | Enablement flag for template `SBT_97`; the normalized view retains mappings with value 1. |
| `sbt_143` | Enablement flag for template `SBT_143`; the normalized view retains mappings with value 1. |
| `sbt_144` | Enablement flag for template `SBT_144`; the normalized view retains mappings with value 1. |
| `sbt_145` | Enablement flag for template `SBT_145`; the normalized view retains mappings with value 1. |
| `sbt_146` | Enablement flag for template `SBT_146`; the normalized view retains mappings with value 1. |
| `sbt_147` | Enablement flag for template `SBT_147`; the normalized view retains mappings with value 1. |
| `sbt_148` | Enablement flag for template `SBT_148`; the normalized view retains mappings with value 1. |
| `sbt_151` | Enablement flag for template `SBT_151`; the normalized view retains mappings with value 1. |
| `sbt_152` | Enablement flag for template `SBT_152`; the normalized view retains mappings with value 1. |
| `sbt_156` | Enablement flag for template `SBT_156`; the normalized view retains mappings with value 1. |
| `sbt_157` | Enablement flag for template `SBT_157`; the normalized view retains mappings with value 1. |
| `sbt_158` | Enablement flag for template `SBT_158`; the normalized view retains mappings with value 1. |
| `sbt_159` | Enablement flag for template `SBT_159`; the normalized view retains mappings with value 1. |
| `sbt_160` | Enablement flag for template `SBT_160`; the normalized view retains mappings with value 1. |
| `mdtl1` | Enablement flag for template `MDTL1`; the normalized view retains mappings with value 1. |
| `md107` | Enablement flag for template `MD107`; the normalized view retains mappings with value 1. |
| `mdavc` | Enablement flag for template `MDAVC`; the normalized view retains mappings with value 1. |
| `mdcu1` | Enablement flag for template `MDCU1`; the normalized view retains mappings with value 1. |
| `mdcu2` | Enablement flag for template `MDCU2`; the normalized view retains mappings with value 1. |
| `mdpr1` | Enablement flag for template `MDPR1`; the normalized view retains mappings with value 1. |
| `edtl1` | Enablement flag for template `EDTL1`; the normalized view retains mappings with value 1. |
| `edcu1` | Enablement flag for template `EDCU1`; the normalized view retains mappings with value 1. |
| `edcu2` | Enablement flag for template `EDCU2`; the normalized view retains mappings with value 1. |
| `ed105` | Enablement flag for template `ED105`; the normalized view retains mappings with value 1. |
| `ed107` | Enablement flag for template `ED107`; the normalized view retains mappings with value 1. |
| `eo107` | Enablement flag for template `EO107`; the normalized view retains mappings with value 1. |
| `eo103` | Enablement flag for template `EO103`; the normalized view retains mappings with value 1. |
| `eo111` | Enablement flag for template `EO111`; the normalized view retains mappings with value 1. |
| `eo104` | Enablement flag for template `EO104`; the normalized view retains mappings with value 1. |
| `eo106` | Enablement flag for template `EO106`; the normalized view retains mappings with value 1. |
| `eo105` | Enablement flag for template `EO105`; the normalized view retains mappings with value 1. |
| `eo101` | Enablement flag for template `EO101`; the normalized view retains mappings with value 1. |
| `eo108` | Enablement flag for template `EO108`; the normalized view retains mappings with value 1. |
| `eo109` | Enablement flag for template `EO109`; the normalized view retains mappings with value 1. |
| `vo28761` | Enablement flag for template `VO28761`; the normalized view retains mappings with value 1. |
| `vo27848` | Enablement flag for template `VO27848`; the normalized view retains mappings with value 1. |
| `vo27847` | Enablement flag for template `VO27847`; the normalized view retains mappings with value 1. |
| `vo27846` | Enablement flag for template `VO27846`; the normalized view retains mappings with value 1. |
| `vo27845` | Enablement flag for template `VO27845`; the normalized view retains mappings with value 1. |
| `vo27844` | Enablement flag for template `VO27844`; the normalized view retains mappings with value 1. |
| `vo27843` | Enablement flag for template `VO27843`; the normalized view retains mappings with value 1. |
| `vo27842` | Enablement flag for template `VO27842`; the normalized view retains mappings with value 1. |
| `vo27841` | Enablement flag for template `VO27841`; the normalized view retains mappings with value 1. |
| `vo27839` | Enablement flag for template `VO27839`; the normalized view retains mappings with value 1. |
| `vo27838` | Enablement flag for template `VO27838`; the normalized view retains mappings with value 1. |
| `vo27837` | Enablement flag for template `VO27837`; the normalized view retains mappings with value 1. |
| `vo27836` | Enablement flag for template `VO27836`; the normalized view retains mappings with value 1. |
| `vo27835` | Enablement flag for template `VO27835`; the normalized view retains mappings with value 1. |
| `vo27834` | Enablement flag for template `VO27834`; the normalized view retains mappings with value 1. |
| `vo27833` | Enablement flag for template `VO27833`; the normalized view retains mappings with value 1. |
| `vo27832` | Enablement flag for template `VO27832`; the normalized view retains mappings with value 1. |
| `vo27831` | Enablement flag for template `VO27831`; the normalized view retains mappings with value 1. |
| `vo27830` | Enablement flag for template `VO27830`; the normalized view retains mappings with value 1. |
| `vo27829` | Enablement flag for template `VO27829`; the normalized view retains mappings with value 1. |
| `vo27828` | Enablement flag for template `VO27828`; the normalized view retains mappings with value 1. |
| `vo27827` | Enablement flag for template `VO27827`; the normalized view retains mappings with value 1. |
| `vo27826` | Enablement flag for template `VO27826`; the normalized view retains mappings with value 1. |
| `vo27825` | Enablement flag for template `VO27825`; the normalized view retains mappings with value 1. |
| `vo27824` | Enablement flag for template `VO27824`; the normalized view retains mappings with value 1. |
| `vo27823` | Enablement flag for template `VO27823`; the normalized view retains mappings with value 1. |
| `vo27822` | Enablement flag for template `VO27822`; the normalized view retains mappings with value 1. |
| `vo27821` | Enablement flag for template `VO27821`; the normalized view retains mappings with value 1. |
| `vo27819` | Enablement flag for template `VO27819`; the normalized view retains mappings with value 1. |
| `vo27818` | Enablement flag for template `VO27818`; the normalized view retains mappings with value 1. |
| `vo27817` | Enablement flag for template `VO27817`; the normalized view retains mappings with value 1. |
| `vo27815` | Enablement flag for template `VO27815`; the normalized view retains mappings with value 1. |
| `vo27814` | Enablement flag for template `VO27814`; the normalized view retains mappings with value 1. |
| `vo27813` | Enablement flag for template `VO27813`; the normalized view retains mappings with value 1. |
| `vo27812` | Enablement flag for template `VO27812`; the normalized view retains mappings with value 1. |
| `vo27811` | Enablement flag for template `VO27811`; the normalized view retains mappings with value 1. |
| `vo27810` | Enablement flag for template `VO27810`; the normalized view retains mappings with value 1. |
| `vo27809` | Enablement flag for template `VO27809`; the normalized view retains mappings with value 1. |
| `vo27808` | Enablement flag for template `VO27808`; the normalized view retains mappings with value 1. |
| `vo27807` | Enablement flag for template `VO27807`; the normalized view retains mappings with value 1. |
| `vo27806` | Enablement flag for template `VO27806`; the normalized view retains mappings with value 1. |
| `vo27805` | Enablement flag for template `VO27805`; the normalized view retains mappings with value 1. |
| `vo27804` | Enablement flag for template `VO27804`; the normalized view retains mappings with value 1. |
| `vo27803` | Enablement flag for template `VO27803`; the normalized view retains mappings with value 1. |
| `vo27802` | Enablement flag for template `VO27802`; the normalized view retains mappings with value 1. |
| `vo21270` | Enablement flag for template `VO21270`; the normalized view retains mappings with value 1. |
| `vo21269` | Enablement flag for template `VO21269`; the normalized view retains mappings with value 1. |
| `vo21268` | Enablement flag for template `VO21268`; the normalized view retains mappings with value 1. |
| `vo21267` | Enablement flag for template `VO21267`; the normalized view retains mappings with value 1. |
| `vo21264` | Enablement flag for template `VO21264`; the normalized view retains mappings with value 1. |
| `vo21263` | Enablement flag for template `VO21263`; the normalized view retains mappings with value 1. |
| `vo29569` | Enablement flag for template `VO29569`; the normalized view retains mappings with value 1. |
| `vo29570` | Enablement flag for template `VO29570`; the normalized view retains mappings with value 1. |
| `vo29571` | Enablement flag for template `VO29571`; the normalized view retains mappings with value 1. |
| `vo29572` | Enablement flag for template `VO29572`; the normalized view retains mappings with value 1. |
| `vo29933` | Enablement flag for template `VO29933`; the normalized view retains mappings with value 1. |
| `vo29951` | Enablement flag for template `VO29951`; the normalized view retains mappings with value 1. |
| `vo29976` | Enablement flag for template `VO29976`; the normalized view retains mappings with value 1. |
| `vo31247` | Enablement flag for template `VO31247`; the normalized view retains mappings with value 1. |

`edwprodhh.hermes.master_config_templates_plgroup`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `channel` | Contact channel associated with the template or rule. |
| `template` | Contact template identifier. |
