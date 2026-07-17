from pathlib import Path


CHARTER = Path(
    "research/charters/SP_CHARTER_001.md"
)


def charter_text() -> str:
    return CHARTER.read_text(
        encoding="utf-8",
    )


def test_charter_exists() -> None:
    assert CHARTER.is_file()


def test_declares_active_milestone() -> None:
    text = charter_text()

    assert "Specification Platform" in text
    assert "Status" in text
    assert "Active" in text


def test_declares_deliverables() -> None:
    text = charter_text()

    for item in (
        "SP-001",
        "SP-002",
        "SP-003",
        "SP-004",
        "SP-005",
        "SP-006",
    ):
        assert item in text


def test_declares_exit_criteria() -> None:
    text = charter_text()

    assert "Exit Criteria" in text
    assert "Executable Contract" in text
    assert "Implementation" in text
