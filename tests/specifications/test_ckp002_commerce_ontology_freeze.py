from pathlib import Path


FREEZE = Path(
    "research/commerce/ontology/releases/"
    "CKP_002_COMMERCE_ONTOLOGY_FREEZE.md"
)

FROZEN_MILESTONES = (
    "CKP-002.1",
    "CKP-002.2",
    "CKP-002.3",
    "CKP-002.4",
    "CKP-002.5",
    "CKP-002.6",
    "CKP-002.7",
)

FROZEN_PROPERTIES = (
    "Canonical Identity Preservation.",
    "Vocabulary Compatibility.",
    "Registered Object Closure.",
    "Single Root Preservation.",
    "Hierarchy Acyclicity.",
    "Relationship Direction Preservation.",
    "Inverse Relationship Consistency.",
    "No Duplicate Assertions.",
    "Domain Separation.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Deterministic Audit Evidence.",
)

FROZEN_HIERARCHY = (
    "Retail Is A Commerce.",
    "Wholesale Is A Commerce.",
    "Ecommerce Is A Commerce.",
    "Informal Commerce Is A Commerce.",
)

FROZEN_RELATIONSHIPS = (
    "SKU Part Of Product.",
    "Product Contains SKU.",
    "Product Tracked As SKU.",
    "Retail Uses Channel.",
    "Channel Used By Retail.",
    "Product Sold Through Channel.",
    "Inventory Applies To SKU.",
    "Customer Uses Channel.",
)

MODIFICATION_REQUIREMENTS = (
    "Architectural justification.",
    "Explicit ADR.",
    "Ontology impact analysis.",
    "Vocabulary compatibility verification.",
    "Relationship consistency verification.",
    "Hierarchy consistency verification.",
    "Successful regression suite.",
    "Ontology consistency audit.",
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


def test_freeze_declares_identity() -> None:
    content = normalized_text()

    assert "CKP-002 Commerce Ontology Freeze" in content
    assert "Version 1.0" in content
    assert "Status Frozen" in content


def test_freeze_declares_complete_scope() -> None:
    content = freeze_text()

    for milestone in FROZEN_MILESTONES:
        assert milestone in content


def test_freeze_declares_frozen_assets() -> None:
    content = freeze_text()

    for asset in (
        "Commerce Ontology Charter.",
        "Ontology Structure Model.",
        "Ontology Class Model.",
        "Ontology Hierarchy Model.",
        "Relationship Assertion Model.",
        "Initial Commerce Ontology.",
        "Ontology Consistency Audit.",
    ):
        assert asset in content


def test_freeze_declares_exact_boundary() -> None:
    content = normalized_text()

    assert (
        "The frozen ontology contains exactly ten "
        "Ontology Nodes."
    ) in content

    assert (
        "The frozen ontology references exactly the "
        "first ten registered Canonical Commerce Terms."
    ) in content

    assert (
        "Commerce remains the only root Ontology Node."
    ) in content

    assert (
        "No unregistered Knowledge Object belongs to "
        "the frozen ontology."
    ) in content


def test_freeze_declares_frozen_properties() -> None:
    content = freeze_text()

    for property_name in FROZEN_PROPERTIES:
        assert property_name in content


def test_freeze_declares_hierarchy() -> None:
    content = normalized_text()

    for assertion in FROZEN_HIERARCHY:
        assert assertion in content


def test_freeze_declares_semantic_relationships() -> None:
    content = normalized_text()

    for assertion in FROZEN_RELATIONSHIPS:
        assert assertion in content


def test_freeze_declares_modification_requirements() -> None:
    content = normalized_text()

    for requirement in MODIFICATION_REQUIREMENTS:
        assert requirement in content


def test_freeze_declares_extension_policy() -> None:
    content = normalized_text()

    for rule in (
        "New Ontology Nodes may extend the frozen "
        "baseline only after registration in the "
        "Knowledge Registry.",
        "New hierarchy assertions shall use canonical "
        "relationship types.",
        "New semantic assertions shall reference "
        "registered Ontology Nodes.",
        "New domain specializations shall not redefine "
        "frozen canonical Commerce semantics.",
        "Existing Canonical Identifiers shall never "
        "be reused.",
        "Existing frozen assertions may evolve only "
        "through governed versioning.",
    ):
        assert rule in content


def test_freeze_requires_complete_verification() -> None:
    content = normalized_text()

    for requirement in (
        "All CKP-002 executable contracts shall pass.",
        "All CKP-001 executable contracts shall remain green.",
        "The complete Foundation regression suite shall remain green.",
        "The Specification Runtime regression suite shall remain green.",
        "Exactly ten Ontology Nodes shall remain in the "
        "frozen initial ontology.",
        "Commerce shall remain the only root Ontology Node.",
        "Every relationship assertion shall use a "
        "canonical Relationship Type.",
        "Every inverse-paired relationship shall remain consistent.",
        "No open semantic, structural, registry, or "
        "traceability violation shall remain.",
    ):
        assert requirement in content


def test_freeze_declares_result() -> None:
    content = normalized_text()

    assert "CKP-002 Commerce Ontology" in content
    assert "Status Frozen" in content
    assert "Version 1.0" in content


def test_freeze_declares_next_milestone() -> None:
    content = normalized_text()

    assert "CKP-003" in content
    assert "Commerce Knowledge Graph" in content
