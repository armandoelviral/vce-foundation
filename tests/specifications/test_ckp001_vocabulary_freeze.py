from pathlib import Path


FREEZE = Path(
    "research/commerce/releases/"
    "CKP_001_VOCABULARY_FREEZE.md"
)

FROZEN_MILESTONES = (
    "CKP-001.1",
    "CKP-001.2",
    "CKP-001.3",
    "CKP-001.4",
    "CKP-001.5",
    "CKP-001.6",
    "CKP-001.7",
    "CKP-AUDIT-001",
    "ADR-004",
)

FROZEN_PROPERTIES = (
    "Canonical Identifier Stability.",
    "Preferred Name Uniqueness.",
    "Canonical Definition Presence.",
    "Mandatory Section Completeness.",
    "Registry Membership.",
    "Semantic Relationship Canonicality.",
    "Knowledge Object Identity.",
    "Semantic Traceability.",
    "Domain Separation.",
)

MODIFICATION_REQUIREMENTS = (
    "Architectural justification.",
    "Explicit ADR.",
    "Semantic impact analysis.",
    "Compatibility verification.",
    "Successful regression suite.",
    "Vocabulary audit.",
)


def freeze_text() -> str:
    return FREEZE.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        freeze_text().split()
    )


def test_freeze_contract_exists() -> None:
    assert FREEZE.is_file()


def test_freeze_status_is_frozen() -> None:
    content = normalized_text()

    assert "Status Frozen" in content
    assert "Version 1.0" in content


def test_freeze_declares_complete_scope() -> None:
    content = freeze_text()

    for milestone in FROZEN_MILESTONES:
        assert milestone in content


def test_freeze_declares_frozen_properties() -> None:
    content = freeze_text()

    for property_name in FROZEN_PROPERTIES:
        assert property_name in content


def test_freeze_declares_modification_requirements() -> None:
    content = normalized_text()

    for requirement in MODIFICATION_REQUIREMENTS:
        assert requirement in content


def test_freeze_preserves_identifier_immutability() -> None:
    content = normalized_text()

    assert (
        "Existing Canonical Identifiers shall never be reused."
        in content
    )


def test_freeze_preserves_canonical_semantics() -> None:
    content = normalized_text()

    assert (
        "New Knowledge Objects may extend the frozen baseline "
        "without redefining existing canonical semantics."
    ) in content

    assert (
        "Domain-specific vocabularies shall consume canonical "
        "Commerce Knowledge Objects without private redefinition."
    ) in content


def test_freeze_requires_regression_verification() -> None:
    content = normalized_text()

    assert (
        "All CKP-001 executable contracts shall pass."
        in content
    )

    assert (
        "The complete Foundation regression suite shall remain green."
        in content
    )

    assert (
        "The Specification Runtime regression suite shall remain green."
        in content
    )


def test_freeze_declares_result() -> None:
    content = normalized_text()

    assert "CKP-001 Canonical Commerce Vocabulary" in content
    assert "Status Frozen" in content
    assert "Version 1.0" in content


def test_freeze_declares_next_milestone() -> None:
    content = normalized_text()

    assert "CKP-002" in content
    assert "Commerce Ontology" in content
