from pathlib import Path


SCHEMA = Path(
    "research/specifications/TRACEABILITY_SCHEMA.md"
)


def text() -> str:
    return SCHEMA.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(text().split())


def test_schema_exists() -> None:
    assert SCHEMA.is_file()


def test_claim_is_traceability_unit() -> None:
    assert "Normative Claim" in text()


def test_runtime_is_out_of_scope() -> None:
    normalized = normalized_text()

    assert (
        "Runtime components are intentionally outside "
        "the scope of the Specification Platform."
    ) in normalized

    assert (
        "They shall be introduced by the "
        "Conformance milestone."
    ) in normalized


def test_relationship_is_defined() -> None:
    schema = text()

    relationship = (
        "Normative Claim",
        "Specification Asset",
        "Capability",
        "Executable Contract",
    )

    for item in relationship:
        assert item in schema
