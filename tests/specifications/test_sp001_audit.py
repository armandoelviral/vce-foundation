from pathlib import Path

AUDIT = Path(
    "research/audits/specification_platform/SP001_AUDIT.md"
)

def test_sp001_audit_exists() -> None:
    assert AUDIT.is_file()

def test_sp001_audit_contains_definition_of_done() -> None:
    text = AUDIT.read_text(encoding="utf-8")

    required = (
        "Runtime specification exists",
        "Executable contract exists",
        "Executable contract passes",
        "Referenced by runtime manifest",
        "Referenced by specifications README",
        "Mandatory sections present",
    )

    for item in required:
        assert item in text
