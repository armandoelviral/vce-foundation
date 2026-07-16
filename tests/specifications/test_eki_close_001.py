from pathlib import Path


REPORT = Path(
    "research/milestones/EKI_CLOSE_001.md"
)


def report_text() -> str:
    return REPORT.read_text(
        encoding="utf-8",
    )


def test_report_exists() -> None:
    assert REPORT.is_file()


def test_status_closed() -> None:
    assert "Status" in report_text()
    assert "CLOSED" in report_text()


def test_contains_release_gates() -> None:
    text = report_text()

    assert "tests/runtime/invariants -q" in text
    assert "tests/runtime -q" in text


def test_contains_completion_evidence() -> None:
    text = report_text()

    assert "14 passed" in text
    assert "118 passed" in text


def test_declares_invariant_infrastructure_frozen() -> None:
    assert "Invariant infrastructure is frozen." in report_text()
