from pathlib import Path

MODEL = Path(
    "research/commerce/"
    "KNOWLEDGE_REGISTRY_MODEL.md"
)


def text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized() -> str:
    return " ".join(text().split())


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_registered_object_types_exist() -> None:
    content = text()

    for item in (
        "Canonical Terms",
        "Semantic Relationships",
        "Normative Claims",
        "Business Rules",
        "Capabilities",
    ):
        assert item in content


def test_registry_responsibilities_exist() -> None:
    content = normalized()

    for item in (
        "Assign immutable identifiers.",
        "Preserve canonical definitions.",
        "Track lifecycle state.",
        "Maintain semantic traceability.",
        "Prevent duplicate concepts.",
    ):
        assert item in content


def test_registry_properties_exist() -> None:
    content = text()

    for item in (
        "Canonical",
        "Deterministic",
        "Traceable",
        "Versioned",
        "Auditable",
        "Immutable Identity",
    ):
        assert item in content


def test_registry_constraints_exist() -> None:
    content = normalized()

    assert (
        "Every registered object shall have one Canonical Identifier."
        in content
    )

    assert (
        "No registered object may exist outside the Registry."
        in content
    )

    assert (
        "Identifiers shall never be reused."
        in content
    )


def test_release_criteria_exist() -> None:
    content = normalized()

    for item in (
        "Object types defined.",
        "Responsibilities declared.",
        "Lifecycle declared.",
        "Constraints declared.",
    ):
        assert item in content
