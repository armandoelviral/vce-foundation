from pathlib import Path

MODEL = Path(
    "research/commerce/"
    "CANONICAL_IDENTIFIER_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(
        text().split()
    )


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_identifier_format_exists() -> None:
    content = normalized()

    assert "CKP-TERM-000001" in content


def test_identifier_components_exist() -> None:
    content = text()

    for item in (
        "CKP",
        "TERM",
        "000001",
    ):
        assert item in content


def test_identifier_properties_exist() -> None:
    content = text()

    for item in (
        "Globally Unique",
        "Immutable",
        "Never Reused",
        "Language Independent",
        "Implementation Independent",
        "Human Readable",
        "Machine Readable",
    ):
        assert item in content


def test_identifier_lifecycle_exists() -> None:
    content = text()

    for item in (
        "Allocated",
        "Approved",
        "Deprecated",
        "Retired",
    ):
        assert item in content


def test_constraints_exist() -> None:
    content = normalized()

    for item in (
        "Identifiers shall never change.",
        "Names may change.",
        "Definitions may evolve.",
        "Identifiers remain permanent.",
    ):
        assert item in content


def test_release_criteria_exist() -> None:
    content = normalized()

    for item in (
        "Canonical format defined.",
        "Lifecycle defined.",
        "Properties declared.",
        "Constraints declared.",
    ):
        assert item in content
