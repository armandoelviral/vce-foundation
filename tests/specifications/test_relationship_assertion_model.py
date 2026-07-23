from pathlib import Path


MODEL = Path(
    "research/commerce/ontology/"
    "RELATIONSHIP_ASSERTION_MODEL.md"
)

ASSERTION_PROPERTIES = (
    "Canonical Identifier.",
    "Source Node.",
    "Canonical Relationship Type.",
    "Target Node.",
    "Directionality.",
    "Inverse Relationship Reference.",
    "Lifecycle Status.",
    "Evidence Reference.",
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

RELATIONSHIP_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Source Identity Preservation.",
    "Target Identity Preservation.",
    "Direction Preservation.",
    "Inverse Consistency.",
    "Relationship Type Canonicality.",
    "No Duplicate Assertions.",
    "Registered Node Closure.",
    "Semantic Closure.",
    "Traceability Closure.",
)

AUDIT_EVIDENCE_FIELDS = (
    "Relationship Assertion Identifier.",
    "Source Node Identifier.",
    "Relationship Type.",
    "Target Node Identifier.",
    "Directionality.",
    "Inverse Relationship Identifier.",
    "Validation Result.",
    "Failure Reason.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_relationship_assertion_model_exists() -> None:
    assert MODEL.is_file()


def test_relationship_assertion_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Relationship Assertion connects one Source "
        "Node to one Target Node through one canonical "
        "Relationship Type."
    ) in content

    for property_name in ASSERTION_PROPERTIES:
        assert property_name in model_text()


def test_source_and_target_nodes_are_defined() -> None:
    content = normalized_text()

    assert (
        "The Source Node is the registered Ontology "
        "Node from which the Relationship Assertion "
        "originates."
    ) in content

    assert (
        "The Target Node is the registered Ontology "
        "Node to which the Relationship Assertion is "
        "directed."
    ) in content

    assert (
        "The Source Node shall preserve its Canonical "
        "Identifier."
    ) in content

    assert (
        "The Target Node shall preserve its Canonical "
        "Identifier."
    ) in content


def test_canonical_relationship_types_are_declared() -> None:
    content = model_text()

    for relationship_type in RELATIONSHIP_TYPES:
        assert relationship_type in content


def test_directionality_is_defined() -> None:
    content = normalized_text()

    for direction in (
        "Unidirectional.",
        "Bidirectional.",
        "Inverse-Paired.",
    ):
        assert direction in model_text()

    assert (
        "Directionality shall not be inferred from "
        "presentation order."
    ) in content


def test_inverse_relationships_are_defined() -> None:
    content = normalized_text()

    assert "Part Of is inverse to Contains." in content
    assert "Uses is inverse to Used By." in content

    assert (
        "An inverse relationship shall preserve the "
        "same participating Ontology Nodes in reversed "
        "semantic direction."
    ) in content


def test_relationship_identity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Relationship Assertion shall possess "
        "one immutable Canonical Identifier."
    ) in content

    assert "CKP-REL-000001" in content

    assert (
        "Relationship identifiers shall never be reused."
    ) in content


def test_initial_relationship_assertions_are_declared() -> None:
    content = normalized_text()

    for assertion in (
        "Retail Is A Commerce.",
        "Wholesale Is A Commerce.",
        "Ecommerce Is A Commerce.",
        "Informal Commerce Is A Commerce.",
        "SKU Part Of Product.",
        "Product Contains SKU.",
        "Product Tracked As SKU.",
        "Retail Uses Channel.",
        "Channel Used By Retail.",
        "Product Sold Through Channel.",
        "Inventory Applies To SKU.",
        "Customer Uses Channel.",
    ):
        assert assertion in content


def test_relationship_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Source Node shall be registered.",
        "Every Target Node shall be registered.",
        "Every Relationship Type shall be canonical.",
        "Every Relationship Assertion shall declare directionality.",
        "Every inverse-paired assertion shall reference its inverse assertion.",
        "Relationship identifiers shall be unique.",
        "Duplicate semantic assertions shall be prohibited.",
        "A Relationship Assertion shall not connect an Ontology Node "
        "to itself unless the canonical relationship explicitly "
        "permits reflexivity.",
        "Related To shall be used only when no more specific canonical "
        "Relationship Type applies.",
        "No domain-specific assertion may redefine frozen canonical "
        "Commerce semantics.",
    ):
        assert constraint in content


def test_relationship_invariants_are_declared() -> None:
    content = model_text()

    for invariant in RELATIONSHIP_INVARIANTS:
        assert invariant in content


def test_audit_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Relationship Assertion shall produce "
        "deterministic audit evidence."
    ) in content

    for field_name in AUDIT_EVIDENCE_FIELDS:
        assert field_name in model_text()


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Relationship Assertion is explicitly defined.",
        "Source and Target Nodes are explicitly defined.",
        "Canonical Relationship Types are declared.",
        "Directionality is declared.",
        "Inverse relationships are constrained.",
        "Relationship identity is defined.",
        "Initial Relationship Assertions are declared.",
        "Relationship constraints are declared.",
        "Relationship invariants are declared.",
        "Audit Evidence is defined.",
    ):
        assert criterion in content
