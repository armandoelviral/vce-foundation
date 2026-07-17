from pathlib import Path


AUDIT = Path(
    "research/audits/SP_AUDIT_001.md"
)


def audit_text() -> str:
    return AUDIT.read_text(
        encoding="utf-8",
    )


def test_audit_exists() -> None:
    assert AUDIT.is_file()


def test_lists_all_sp_deliverables() -> None:
    text = audit_text()

    for deliverable in (
        "SP-001",
        "SP-002",
        "SP-003",
        "SP-004",
        "SP-005",
        "SP-006",
    ):
        assert deliverable in text


def test_defines_audit_rule() -> None:
    text = audit_text()

    assert "Audit Rule" in text
    assert "the normative document exists" in text
    assert "its executable contract exists" in text
    assert "the executable contract passes" in text
