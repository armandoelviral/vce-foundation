from pathlib import Path


SCHEMA = Path(
    "research/specifications/TRACEABILITY_SCHEMA.md"
)


def schema_text() -> str:
    return SCHEMA.read_text(
        encoding="utf-8",
    )


def test_schema_exists() -> None:
    assert SCHEMA.is_file()


def test_schema_declares_traceability_unit() -> None:
    text = schema_text()

    assert "Normative Claim" in text
    assert "stable identifier" in text


def test_schema_declares_required_fields() -> None:
    text = schema_text()

    required = (
        "Claim ID",
        "Specification Asset",
        "Capability",
        "Executable Contracts",
        "Runtime Components",
    )

    for field in required:
        assert field in text


def test_schema_declares_relationship() -> None:
    text = schema_text()

    relationship = (
        "Normative Claim",
        "Specification Asset",
        "Capability",
        "Executable Contract",
        "Runtime Component",
    )

    for item in relationship:
        assert item in text


def test_schema_declares_constraints() -> None:
    text = schema_text()

    assert "Constraints" in text
    assert "Every Claim shall reference exactly one" in text
    assert "Every Capability shall reference at least one" in text
