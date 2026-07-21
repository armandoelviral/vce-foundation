from pathlib import Path

AUDIT = Path(
    "research/audits/SR_CLOSE_001.md"
)


def text() -> str:
    return AUDIT.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(
        text().split()
    )


def test_audit_exists() -> None:
    assert AUDIT.is_file()


def test_scope_exists() -> None:
    content = text()

    for item in (
        "SR-001",
        "SR-002",
        "SR-003",
    ):
        assert item in content


def test_verification_items_exist() -> None:
    content = normalized()

    for item in (
        "Runtime Charter",
        "Execution Model",
        "Runtime Model",
        "Execution Unit",
        "Runtime Executor",
        "Runtime Orchestration",
        "First Executable Specification",
    ):
        assert item in content


def test_acceptance_criteria_exist() -> None:
    content = normalized()

    for item in (
        "All Runtime contracts pass.",
        "Foundation remains green.",
        "Specification execution is deterministic.",
        "Runtime preserves Specification identity.",
        "Evidence is preserved.",
        "Behavior is unchanged after orchestration refactoring.",
    ):
        assert item in content


def test_next_milestone_exists() -> None:
    content = normalized()

    assert "SP001" in content
    assert "Retail Vocabulary" in content
