"""Self-check for enrich_documentation.py's Talend Cloud task linking. Run directly: uv run src/documentation/test_enrich_documentation.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from enrich_documentation import (
    correlate_cloud_tasks,
    generate_dependency_matrix_doc,
    summarize_last_execution,
    summarize_schedule,
)

JOBS = [{"name": "Nightly_Load"}, {"name": "Manual_Task"}]


def test_correlate_cloud_tasks_matches_by_artifact_name() -> None:
    cloud_tasks = [
        {
            "name": "Nightly_Load_task",
            "artifact_name": "Nightly_Load",
            "schedule": {"triggers": [{"type": "Cron", "expression": "0 2 * * *"}]},
            "recent_executions": [
                {"status": "EXECUTION_SUCCESS", "start_time": "2026-08-27T02:00:00Z"}
            ],
        }
    ]
    matched, unmatched = correlate_cloud_tasks(JOBS, cloud_tasks)
    assert len(matched) == 1
    assert matched[0]["job"] == "Nightly_Load"
    assert matched[0]["task_name"] == "Nightly_Load_task"
    assert unmatched == []


def test_correlate_cloud_tasks_reports_unmatched() -> None:
    cloud_tasks = [{"name": "Orphan_task", "artifact_name": "Orphan_task"}]
    matched, unmatched = correlate_cloud_tasks(JOBS, cloud_tasks)
    assert matched == []
    assert unmatched == ["Orphan_task"]


def test_summarize_schedule_handles_none_and_triggers() -> None:
    assert summarize_schedule(None) == "No schedule (manual/webhook)"
    assert summarize_schedule({"triggers": []}) == "No schedule (manual/webhook)"
    assert "Cron" in summarize_schedule(
        {"triggers": [{"type": "Cron", "expression": "0 2 * * *"}]}
    )


def test_summarize_last_execution_picks_latest() -> None:
    assert summarize_last_execution([]) == "No recent executions"
    executions = [
        {"status": "EXECUTION_FAILED", "start_time": "2026-08-01T00:00:00Z"},
        {"status": "EXECUTION_SUCCESS", "start_time": "2026-08-27T02:00:00Z"},
    ]
    summary = summarize_last_execution(executions)
    assert "EXECUTION_SUCCESS" in summary
    assert "2026-08-27" in summary


def test_dependency_matrix_doc_includes_cloud_section_when_present() -> None:
    talend = {"projects": []}
    matched = [
        {
            "job": "Nightly_Load",
            "task_name": "Nightly_Load_task",
            "schedule": {"triggers": [{"type": "Cron", "expression": "0 2 * * *"}]},
            "recent_executions": [],
        }
    ]
    doc = generate_dependency_matrix_doc(talend, matched, ["Orphan_task"])
    assert "Job → Talend Cloud task" in doc
    assert "Nightly_Load" in doc
    assert "Orphan_task" in doc


def test_dependency_matrix_doc_omits_cloud_section_when_absent() -> None:
    talend = {"projects": []}
    doc = generate_dependency_matrix_doc(talend)
    assert "Job → Talend Cloud task" not in doc


def main() -> None:
    test_correlate_cloud_tasks_matches_by_artifact_name()
    test_correlate_cloud_tasks_reports_unmatched()
    test_summarize_schedule_handles_none_and_triggers()
    test_summarize_last_execution_picks_latest()
    test_dependency_matrix_doc_includes_cloud_section_when_present()
    test_dependency_matrix_doc_omits_cloud_section_when_absent()
    print("All enrich_documentation Talend Cloud linking checks passed.")


if __name__ == "__main__":
    main()
