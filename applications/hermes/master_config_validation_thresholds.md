# master_config_validation_thresholds

Source: [master_config_validation_thresholds.sql](../../src/sql/master_config_validation_thresholds.sql)

Maps placement-group validation cutoffs to Latitude client codes.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.transform_config_validation_thresholds` |
| View | `edwprodhh.hermes.master_config_validation_thresholds` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.pub_jchang.master_client`.

**Logic:**

1. Creates and loads `transform_config_validation_thresholds` with a maximum segment per placement group.
2. The view joins Latitude clients to those thresholds, defaults missing limits to `10`, and returns distinct client/limit pairs.

## Output columns

`edwprodhh.hermes.transform_config_validation_thresholds`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `max_segment` | Maximum configured validation segment; the configuration views default missing limits to 10. |

`edwprodhh.hermes.master_config_validation_thresholds`:

| Column | Meaning |
| --- | --- |
| `client` | Source-system client code; these configuration views return Latitude clients. |
| `max_segment` | Maximum configured validation segment; the configuration views default missing limits to 10. |
