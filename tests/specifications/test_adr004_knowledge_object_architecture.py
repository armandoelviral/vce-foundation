from pathlib import Path


ADR = Path(
    "research/adr/"
    "ADR-004_KNOWLEDGE_OBJECT_ARCHITECTURE.md"
)

KNOWLEDGE_OBJECT_TYPES = (
    "TERM",
    "RELATIONSHIP",
    "CLAIM",
    "RULE",
    "CAPABILITY",
    "POLICY",
    "ROLE",
    "PROCESS",
    "EVENT",
    "METRIC",
    "DOCUMENT",
    "DECISION",
    "CONSTRAINT",
)

KNOWLEDGE_OBJECT_PROPERTIES = (
    "Canonical Identifier.",
    "Object Type.",
    "Preferred Name.",
    "Canonical Definition.",
    "Lifecycle Status.",
    "Version.",
    "Relationships.",
    "Traceability References.",
)

IDENTIFIER_EXAMPLES = (
    "CKP-TERM-000001",
    "CKP-REL-000001",
    "CKP-CLAIM-000001",
    "CKP-RULE-000001",
    "CKP-CAP-000001",
    "CKP-POLICY-000001",
    "CKP-ROLE-000001",
    "CKP-PROCESS-000001",
    "CKP-EVENT-000001",
    "CKP-METRIC-000001",
    "CKP-DOC-000001",
    "CKP-DECISION-000001",
    "CKP-CONSTRAINT-000001",
)


def adr_text() -> str:
    return ADR.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        adr_text().split()
    )


def test_adr_exists() -> None:
    assert ADR.is_file()


def test_adr_is_accepted() -> None:
    assert "Status Accepted" in normalized_text()


def test_adr_declares_knowledge_object_decision() -> None:
    content = normalized_text()

    assert (
        "The fundamental registered unit of the "
        "Commerce Knowledge Platform shall be the "
        "Knowledge Object."
    ) in content

    assert (
        "Every canonical semantic asset shall be "
        "represented as one typed Knowledge Object."
    ) in content


def test_adr_declares_knowledge_object_types() -> None:
    content = adr_text()

    for object_type in KNOWLEDGE_OBJECT_TYPES:
        assert object_type in content


def test_adr_declares_knowledge_object_properties() -> None:
    content = adr_text()

    for property_name in KNOWLEDGE_OBJECT_PROPERTIES:
        assert property_name in content


def test_adr_declares_typed_identifier_namespaces() -> None:
    content = adr_text()

    for identifier in IDENTIFIER_EXAMPLES:
        assert identifier in content


def test_adr_declares_registry_architecture() -> None:
    content = normalized_text()

    assert (
        "The Knowledge Registry shall manage all "
        "Knowledge Objects."
    ) in content

    assert (
        "No canonical Knowledge Object may exist "
        "outside the Registry."
    ) in content


def test_adr_declares_relationships_as_objects() -> None:
    content = normalized_text()

    assert (
        "Semantic Relationships are Knowledge Objects."
        in content
    )

    for property_name in (
        "Canonical Identifier.",
        "Source Knowledge Object.",
        "Canonical Relationship Type.",
        "Target Knowledge Object.",
        "Directionality.",
        "Inverse Relationship Reference.",
        "Lifecycle Status.",
    ):
        assert property_name in adr_text()


def test_adr_declares_knowledge_graph() -> None:
    content = normalized_text()

    assert "Knowledge Objects as Nodes." in content
    assert "Semantic Relationships as Edges." in content

    for property_name in (
        "Canonical.",
        "Directed.",
        "Traceable.",
        "Auditable.",
        "Versioned.",
        "Semantically closed.",
    ):
        assert property_name in adr_text()


def test_adr_declares_traceability_chain() -> None:
    content = adr_text()

    for node in (
        "Knowledge Object",
        "Normative Claim",
        "Specification",
        "Implementation",
        "Decision",
        "Evidence",
    ):
        assert node in content


def test_adr_preserves_domain_separation() -> None:
    content = normalized_text()

    assert (
        "Commerce shall remain the root business domain."
        in content
    )

    assert (
        "Domain-specific knowledge shall not redefine "
        "canonical Commerce semantics."
    ) in content


def test_adr_declares_constraints() -> None:
    content = normalized_text()

    for constraint in (
        "Every canonical semantic asset shall be a "
        "registered Knowledge Object.",
        "Every Knowledge Object shall declare one "
        "canonical type.",
        "Every Knowledge Object shall have one "
        "immutable identifier.",
        "No object-type namespace shall reuse an "
        "identifier.",
        "No domain shall redefine an existing "
        "canonical Knowledge Object privately.",
    ):
        assert constraint in content


def test_adr_rejects_inadequate_alternatives() -> None:
    content = adr_text()

    for alternative in (
        "Term-only Registry.",
        "Document-only Architecture.",
        "Relationship-without-Identity Model.",
    ):
        assert alternative in content


def test_adr_declares_resulting_architecture() -> None:
    content = adr_text()

    for layer in (
        "Knowledge Objects",
        "Knowledge Registry",
        "Knowledge Graph",
        "Commerce Ontology",
        "Executable Specifications",
        "Specification Runtime",
        "Decision Services",
        "Commerce Applications",
    ):
        assert layer in content
