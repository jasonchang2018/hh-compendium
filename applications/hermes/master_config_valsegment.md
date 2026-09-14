# master_config_valsegment

Source: [master_config_valsegment.sql](../../src/sql/master_config_valsegment.sql)

Defines client and placement-group overrides for Latitude validation segments.

| Object | Name |
| --- | --- |
| Table | `edwprodhh.hermes.master_config_valsegments_client` |
| Table | `edwprodhh.hermes.master_config_valsegments_plgroup` |
| View | `edwprodhh.hermes.master_config_valsegments` |
| Stored procedure | None defined in this file. |
| Task | None defined in this file. |

**Inputs:** `edwprodhh.pub_jchang.master_client`.

**Logic:**

1. Creates separate client-level and placement-group configuration tables. The sample inserts and truncates are commented out.
2. The `master_config_valsegments` view includes Latitude clients and chooses the client override first, then the placement-group override, then the default `10`.

## Output columns

`edwprodhh.hermes.master_config_valsegments_client`:

| Column | Meaning |
| --- | --- |
| `client_idx` | Unique client identifier used to join configuration and client data. |
| `max_segment` | Maximum configured validation segment; the configuration views default missing limits to 10. |

`edwprodhh.hermes.master_config_valsegments_plgroup`:

| Column | Meaning |
| --- | --- |
| `pl_group` | Placement group associated with the account or configuration rule. |
| `max_segment` | Maximum configured validation segment; the configuration views default missing limits to 10. |

`edwprodhh.hermes.master_config_valsegments`:

| Column | Meaning |
| --- | --- |
| `client` | Source-system client code; these configuration views return Latitude clients. |
| `max_segment` | Maximum configured validation segment; the configuration views default missing limits to 10. |
