from pathlib import Path


MODEL = Path(
    "research/commerce/relationships/"
    "SEMANTIC_RELATIONSHIP_MODEL.md"
)

RELATIONSHIP_TYPES = (
    "Is A.",
    "Part Of.",
    "Contains.",
    "Uses.",
    "Used By.",
    "Sold Through.",
    "Supports.",
    "Tracked As.",
    "Applies To.",
    "Related To.",
)

RELATIONSHIP_PROPERTIES = (
    "Canonical Identifier.",
    "Source Object.",
    "Relationship Type.",
    "Target Object.",
    "Directionality.",
    "Inverse Relationship.",
    "Status.",
)

RUNTIME_INVARIANTS = (
    "Relationship Identity Preservation.",
    "Relationship Direction Preservation.",
    "Inverse Consistency.",
    "Semantic Closure.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_relationship_model_exists() -> None:
    assert MODEL.is_file()


def test_canonical_relationship_types_exist() -> None:
    content = model_text()

    for relationship_type in RELATIONSHIP_TYPES:
        assert relationship_type in content


def test_directionality_is_defined() -> None:
    content = model_text()

    for direction in (
        "Unidirectional.",
        "Bidirectional.",
        "Inverse-Paired.",
    ):
        assert direction in content


def test_inverse_relationships_are_defined() -> None:
    content = normalized_text()

    assert "Part Of is inverse to Contains." in content
    assert "Uses is inverse to Used By." in content


def test_relationship_properties_exist() -> None:
    content = model_text()

    for property_name in RELATIONSHIP_PROPERTIES:
        assert property_name in content


def test_relationship_constraints_exist() -> None:
    content = normalized_text()

    assert (
        "Every relationship shall reference registered "
        "knowledge objects."
    ) in content

    assert (
        "Every relationship type shall be canonical."
        in content
    )

    assert (
        "Ambiguous relationships shall not be used."
        in content
    )

    assert (
        "Related To shall be used only when no more "
        "specific canonical relationship applies."
    ) in content

    assert (
        "Inverse relationships shall remain "
        "semantically consistent."
    ) in content


def test_runtime_invariants_exist() -> None:
    content = model_text()

    for invariant in RUNTIME_INVARIANTS:
        assert invariant in content


def test_release_criteria_exist() -> None:
    content = normalized_text()

    for item in (
        "Canonical relationship types are defined.",
        "Directionality is defined.",
        "Inverse relationships are defined.",
        "Constraints are declared.",
        "Runtime invariants are declared.",
    ):
        assert item in content
