"""Self-check for talend_cloud_extractor.py. Run directly: uv run src/talend/test_talend_cloud_extractor.py"""

import sys
from pathlib import Path
from types import SimpleNamespace

import requests

sys.path.insert(0, str(Path(__file__).parent))

from talend_cloud_extractor import (
    TalendCloudClient,
    extract_all,
    sanitize_task_parameters,
)


def test_sanitize_task_parameters_redacts_matched_keys() -> None:
    params = {
        "db_password": "hunter2",
        "target_table": "CUSTOMERS",
        "api_key": "abc123",
    }
    safe = sanitize_task_parameters(params)
    assert safe["db_password"] == "***REDACTED***"
    assert safe["api_key"] == "***REDACTED***"
    assert safe["target_table"] == "CUSTOMERS"


def _fake_get(status_code: int, json_data=None, headers=None):
    """Build a stand-in for requests.Session.get returning one canned response."""

    def raise_for_status():
        if status_code >= 400:
            raise requests.exceptions.HTTPError(f"{status_code} error")

    response = SimpleNamespace(
        status_code=status_code,
        headers=headers or {},
        json=lambda: json_data,
        raise_for_status=raise_for_status,
    )

    def fake_get(url, params=None, timeout=None):
        return response

    return fake_get


def test_get_exits_on_auth_failure() -> None:
    client = TalendCloudClient("https://api.eu.cloud.talend.com", "bad-token")
    client.session.get = _fake_get(401)
    try:
        client._get("/orchestration/workspaces")
        raise AssertionError("expected SystemExit on 401")
    except SystemExit as e:
        assert e.code == 1


def test_get_tolerates_404_when_asked() -> None:
    client = TalendCloudClient("https://api.eu.cloud.talend.com", "token")
    client.session.get = _fake_get(404)
    assert client._get("/processing/executables/tasks/xyz/schedule", tolerate_404=True) is None


def test_get_returns_json_on_success() -> None:
    client = TalendCloudClient("https://api.eu.cloud.talend.com", "token")
    client.session.get = _fake_get(200, json_data={"items": [{"id": "1"}]})
    assert client._get("/orchestration/workspaces") == {"items": [{"id": "1"}]}


class _FakeClient:
    """Duck-typed stand-in for TalendCloudClient — no network involved.

    Field shapes here match the real TMC API (confirmed against a live
    tenant), not the shapes suggested by public docs: workspaces nest their
    environment under "environment": {"id": ...}; the task list endpoint
    only returns an "executable" id (name/workspace/artifact/parameters live
    on the per-task detail endpoint, i.e. get_task()); executions use
    executionId/executionStatus/startTimestamp/finishTimestamp.
    """

    def __init__(self):
        self.base_url = "https://api.eu.cloud.talend.com/"

    def list_workspaces(self):
        return [{"id": "ws1", "name": "Default", "environment": {"id": "env1"}}]

    def list_tasks(self, workspace_id):
        assert workspace_id == "ws1"
        return [{"executable": "task1"}, {"executable": "task2"}, {"executable": "task3"}]

    def get_task(self, task_id):
        if task_id == "task1":
            return {
                "id": "task1",
                "name": "Nightly_Load",
                "workspace": {"id": "ws1", "environment": {"id": "env1"}},
                "artifact": {"id": "art1", "name": "Nightly_Load", "version": "0.1.0.1"},
                "parameters": {"db_password": "hunter2", "target_table": "CUSTOMERS"},
            }
        if task_id == "task2":
            return {
                "id": "task2",
                "name": "Manual_Task",
                "workspace": {"id": "ws1", "environment": {"id": "env1"}},
                "artifact": {"id": "art2", "name": "Manual_Task", "version": "0.1.0.1"},
                "parameters": {},
            }
        return None  # task3: detail 404s (e.g. deleted between list and detail call)

    def get_task_schedule(self, task_id):
        if task_id == "task1":
            return {
                "triggers": [
                    {"type": "Cron", "expression": "0 2 * * *", "enabled": True}
                ]
            }
        return None  # task2 has no schedule

    def get_task_executions(self, task_id, last_days):
        assert last_days == 7
        if task_id == "task1":
            return [
                {
                    "executionId": "exec1",
                    "executionStatus": "EXECUTION_SUCCESS",
                    "startTimestamp": "2026-08-27T02:00:00Z",
                    "finishTimestamp": "2026-08-27T02:05:00Z",
                }
            ]
        return []


def test_extract_all_assembles_metadata_and_redacts() -> None:
    metadata = extract_all(_FakeClient(), execution_days=7)

    assert metadata["summary"]["total_workspaces"] == 1
    # task3's detail 404s and is skipped — only task1 and task2 make it in
    assert metadata["summary"]["total_tasks"] == 2
    assert metadata["summary"]["total_scheduled_tasks"] == 1

    task1 = next(t for t in metadata["tasks"] if t["id"] == "task1")
    assert task1["workspace_id"] == "ws1"
    assert task1["environment_id"] == "env1"
    assert task1["artifact_name"] == "Nightly_Load"
    assert task1["artifact_version"] == "0.1.0.1"
    assert task1["parameters"]["db_password"] == "***REDACTED***"
    assert task1["parameters"]["target_table"] == "CUSTOMERS"
    assert task1["schedule"]["triggers"][0]["expression"] == "0 2 * * *"
    assert task1["recent_executions"][0]["status"] == "EXECUTION_SUCCESS"
    assert task1["recent_executions"][0]["execution_id"] == "exec1"

    task2 = next(t for t in metadata["tasks"] if t["id"] == "task2")
    assert task2["schedule"] is None
    assert task2["recent_executions"] == []

    assert not any(t["id"] == "task3" for t in metadata["tasks"])


def main() -> None:
    test_sanitize_task_parameters_redacts_matched_keys()
    test_get_exits_on_auth_failure()
    test_get_tolerates_404_when_asked()
    test_get_returns_json_on_success()
    test_extract_all_assembles_metadata_and_redacts()
    print("All Talend Cloud extractor checks passed.")


if __name__ == "__main__":
    main()
