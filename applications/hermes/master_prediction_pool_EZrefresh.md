# master_prediction_pool_EZrefresh

Source: [master_prediction_pool_EZrefresh.ipynb](../../src/r/master_prediction_pool_EZrefresh.ipynb)

R notebook for executing a selected set of SQL scripts from the notebook's working directory and summarizing execution statuses.

| Object | Name |
| --- | --- |
| Table | None directly defined; selected SQL files determine database objects affected. |
| Stored procedure | None directly defined. |
| Task | None defined. |

**Inputs:** R packages `hh.analytics` and `hh.snowflake`, their package loader/Snowflake connection, and SQL files in the current working directory.

**Logic:**

1. Loads the R helper packages and lists files in the current directory (not recursively).
2. Keeps `.sql` files beginning with `transform_businessrules`, `transform_criteria`, or `transform_prediction_pool`. The `master_prediction_pool` inclusion is commented out; `transform_prediction_pool` does not match the current `transform_prediction_scores_pool.sql` filename.
3. Assigns hard-coded filename priorities, sorts by priority/name, reads each selected file, and passes its full SQL text to `querySnowflake()`.
4. Unnests execution results and counts rows by returned status. This runs the selected scripts as written; it does not parse task dependencies or automatically call each newly defined procedure.

The notebook's filename ordering is independent of the declared Snowflake task graph. Its default directory must contain the intended SQL files for the selection to find them.

## Output columns

R object `x`:

| Column | Meaning |
| --- | --- |
| `file_name` | Selected SQL filename from the current working directory. |
| `priority` | Filename-based execution-order priority. |
| `query` | Full SQL text read from the file. |
| `execute` | Result list returned by querySnowflake(); nested fields depend on the helper. |

Final execution-status summary:

| Column | Meaning |
| --- | --- |
| `status` | Execution status returned by querySnowflake(). |
| `n` | Number of returned result rows with that status. |
