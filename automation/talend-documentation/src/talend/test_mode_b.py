"""Self-check for talend_extractor.py Mode B (archive input). Run directly: uv run src/talend/test_mode_b.py"""

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from talend_extractor import compute_sha256, unpack_archive, validate_archive


def _make_valid_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as zf:
        zf.writestr("hello.txt", b"hello world")


def _make_corrupt_zip(path: Path) -> None:
    """A zip that opens (valid central directory) but fails testzip() (bad CRC)."""
    marker = b"MARKER_PAYLOAD_FOR_CORRUPTION_TEST"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as zf:
        zf.writestr("file.txt", marker)
    raw = bytearray(path.read_bytes())
    idx = raw.find(marker)
    assert idx != -1, "test fixture setup failed: marker not found in raw zip bytes"
    raw[idx] ^= 0xFF  # flip one byte inside the stored (uncompressed) payload
    path.write_bytes(bytes(raw))


def test_validate_archive_accepts_valid_zip(tmp_dir: Path) -> None:
    zip_path = tmp_dir / "valid.zip"
    _make_valid_zip(zip_path)
    validate_archive(zip_path)  # must not raise / exit


def test_validate_archive_rejects_non_zip(tmp_dir: Path) -> None:
    not_a_zip = tmp_dir / "not_a_zip.zip"
    not_a_zip.write_bytes(b"this is not a zip file at all")
    try:
        validate_archive(not_a_zip)
        raise AssertionError("expected SystemExit for a non-zip file")
    except SystemExit as e:
        assert e.code == 1


def test_validate_archive_rejects_corrupt_zip(tmp_dir: Path) -> None:
    corrupt_path = tmp_dir / "corrupt.zip"
    _make_corrupt_zip(corrupt_path)
    try:
        validate_archive(corrupt_path)
        raise AssertionError("expected SystemExit for a corrupted zip")
    except SystemExit as e:
        assert e.code == 1


def test_compute_sha256_matches_hashlib(tmp_dir: Path) -> None:
    import hashlib

    zip_path = tmp_dir / "valid.zip"
    _make_valid_zip(zip_path)
    expected = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    assert compute_sha256(zip_path) == expected


def test_unpack_archive_extracts_and_is_rerun_safe(tmp_dir: Path) -> None:
    zip_path = tmp_dir / "myproject.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("process/marker.item", b"<x/>")
    working_dir = tmp_dir / "working"

    result_dir = unpack_archive(zip_path, working_dir)
    assert result_dir == working_dir / "myproject"
    assert (result_dir / "process" / "marker.item").is_file()

    # Rerun-safe: unpacking again over a stale leftover file must succeed and overwrite
    stale_file = result_dir / "stale_leftover.txt"
    stale_file.write_text("should be removed")
    unpack_archive(zip_path, working_dir)
    assert not stale_file.exists()
    assert (result_dir / "process" / "marker.item").is_file()


def test_job_name_from_stem_strips_version_suffix() -> None:
    from talend_extractor import job_name_from_stem

    assert job_name_from_stem("Customer_Load_0.1") == "Customer_Load"
    assert job_name_from_stem("NoVersionSuffix") == "NoVersionSuffix"


def test_detect_unsupported_artifacts(tmp_dir: Path) -> None:
    from talend_extractor import detect_unsupported_artifacts

    project_dir = tmp_dir / "proj_unsupported"
    (project_dir / "joblets").mkdir(parents=True)
    (project_dir / "metadata" / "connections").mkdir(parents=True)
    (project_dir / "metadata" / "genericSchemas").mkdir(parents=True)

    found = detect_unsupported_artifacts(project_dir)
    assert any("joblets" in f for f in found)
    assert any("genericSchemas" in f for f in found)
    assert not any("connections" in f for f in found)  # connections/ IS supported


def test_extract_project_returns_job_reports(tmp_dir: Path) -> None:
    from talend_extractor import extract_project

    project_dir = tmp_dir / "REPORT_TEST_PROJECT"
    process_dir = project_dir / "process"
    process_dir.mkdir(parents=True)
    good_item = process_dir / "GoodJob_0.1.item"
    good_item.write_text(
        '<?xml version="1.0"?><Process/>',
        encoding="utf-8",
    )
    bad_item = process_dir / "BadJob_0.1.item"
    bad_item.write_text("not valid xml <<<", encoding="utf-8")

    project_data, job_reports, unsupported = extract_project(tmp_dir, "REPORT_TEST_PROJECT")

    assert project_data["name"] == "REPORT_TEST_PROJECT"
    assert len(project_data["jobs"]) == 1  # only the good job made it into the metadata
    names_and_status = {r["name"]: r["status"] for r in job_reports}
    assert names_and_status["GoodJob"] == "SUCCESS"
    assert names_and_status["BadJob"] == "FAILED"
    assert unsupported == []  # no joblets/routes/routines folders present


def test_end_to_end_archive_mode(tmp_dir: Path) -> None:
    import hashlib
    import json
    import subprocess

    archive = (
        Path(__file__).parent.parent.parent
        / "full-documentation"
        / "project-archives"
        / "studio_test_project-2026-08-27.zip"
    )
    assert archive.is_file(), f"sample archive missing: {archive}"

    expected_sha256 = hashlib.sha256(archive.read_bytes()).hexdigest()

    metadata_out = tmp_dir / "e2e_metadata.json"
    report_out = tmp_dir / "e2e_report.json"
    working_dir = tmp_dir / "e2e_working"

    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parent / "talend_extractor.py"),
            str(archive),
            "--output",
            str(metadata_out),
            "--working-dir",
            str(working_dir),
            "--report-output",
            str(report_out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"extractor failed: {result.stderr}"

    metadata = json.loads(metadata_out.read_text(encoding="utf-8"))
    report = json.loads(report_out.read_text(encoding="utf-8"))

    assert report["mode"] == "archive"
    assert report["archive_name"] == archive.name
    assert report["archive_sha256"] == expected_sha256
    assert report["repo_url"] is None
    assert report["branch"] is None
    assert report["commit_sha"] is None
    assert len(report["jobs"]) == metadata["summary"]["total_jobs"]
    assert any(j["name"] == "OnBoardingDemoJob" and j["status"] == "SUCCESS" for j in report["jobs"])


def test_mode_a_report_has_null_archive_fields(tmp_dir: Path) -> None:
    import json
    import subprocess

    archive = (
        Path(__file__).parent.parent.parent
        / "full-documentation"
        / "project-archives"
        / "studio_test_project-2026-08-27.zip"
    )
    workspace_dir = tmp_dir / "mode_a_workspace"
    unpack_archive(archive, workspace_dir.parent)
    shutil.move(str(workspace_dir.parent / archive.stem), str(workspace_dir))

    metadata_out = tmp_dir / "mode_a_metadata.json"
    report_out = tmp_dir / "mode_a_report.json"

    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parent / "talend_extractor.py"),
            str(workspace_dir),
            "--output",
            str(metadata_out),
            "--report-output",
            str(report_out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"extractor failed: {result.stderr}"

    report = json.loads(report_out.read_text(encoding="utf-8"))
    assert report["mode"] == "workspace"
    assert report["archive_name"] is None
    assert report["archive_sha256"] is None
    assert report["repo_url"] is None
    assert report["branch"] is None
    assert report["commit_sha"] is None


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)
        test_validate_archive_accepts_valid_zip(tmp_dir)
        test_validate_archive_rejects_non_zip(tmp_dir)
        test_validate_archive_rejects_corrupt_zip(tmp_dir)
        test_compute_sha256_matches_hashlib(tmp_dir)
        test_unpack_archive_extracts_and_is_rerun_safe(tmp_dir)
        test_job_name_from_stem_strips_version_suffix()
        test_detect_unsupported_artifacts(tmp_dir)
        test_extract_project_returns_job_reports(tmp_dir)
        test_end_to_end_archive_mode(tmp_dir)
        test_mode_a_report_has_null_archive_fields(tmp_dir)
    print("All Mode B checks passed.")


if __name__ == "__main__":
    main()
