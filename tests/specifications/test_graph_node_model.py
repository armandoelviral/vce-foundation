from pathlib import Path


MODEL = Path(
    "research/commerce/knowledge_graph/"
    "GRAPH_NODE_MODEL.md"
)

NODE_PROPERTIES = (
    "Canonical Identifier.",
    "Knowledge Object Type.",
    "Preferred Name.",
    "Canonical Definition Reference.",
    "Lifecycle Status.",
    "Ontology Membership.",
    "Domain Membership.",
    "Registry Reference.",
    "Vocabulary Baseline Reference.",
    "Ontology Baseline Reference.",
    "Source Evidence Reference.",
    "Node Integrity Reference.",
)

INITIAL_NODES = (
    "CKP-TERM-000001 Commerce.",
    "CKP-TERM-000002 Retail.",
    "CKP-TERM-000003 Wholesale.",
    "CKP-TERM-000004 Ecommerce.",
    "CKP-TERM-000005 Informal Commerce.",
    "CKP-TERM-000006 Product.",
    "CKP-TERM-000007 SKU.",
    "CKP-TERM-000008 Inventory.",
    "CKP-TERM-000009 Customer.",
    "CKP-TERM-000010 Channel.",
)

NODE_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Registered Object Closure.",
    "Preferred Name Preservation.",
    "Knowledge Object Type Preservation.",
    "Lifecycle Compatibility.",
    "Ontology Membership Preservation.",
    "Domain Membership Preservation.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "No Duplicate Nodes.",
    "No Orphan Nodes.",
    "Deterministic Ordering.",
    "Normative Equality.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Node Evidence Completeness.",
)

VALIDATION_EVIDENCE_FIELDS = (
    "Evidence Identifier.",
    "Canonical Identifier.",
    "Registry Resolution Result.",
    "Preferred Name Validation.",
    "Knowledge Object Type Validation.",
    "Lifecycle Validation.",
    "Ontology Membership Validation.",
    "Domain Membership Validation.",
    "Vocabulary Baseline Validation.",
    "Ontology Baseline Validation.",
    "Node Integrity Result.",
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


def test_graph_node_model_exists() -> None:
    assert MODEL.is_file()


def test_graph_node_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Node shall represent exactly one "
        "registered Knowledge Object."
    ) in content

    assert (
        "A Graph Node is a graph representation of "
        "source knowledge."
    ) in content

    assert (
        "A Graph Node shall not become an independent "
        "source of canonical meaning."
    ) in content


def test_graph_node_properties_are_declared() -> None:
    content = model_text()

    for property_name in NODE_PROPERTIES:
        assert property_name in content


def test_canonical_identity_is_preserved() -> None:
    content = normalized_text()

    for rule in (
        "A Graph Node shall inherit the Canonical "
        "Identifier of its registered Knowledge Object.",
        "Graph representation shall not allocate a "
        "second semantic identifier for the same "
        "Knowledge Object.",
        "The Canonical Identifier shall remain immutable.",
        "The Canonical Identifier shall remain the "
        "primary identity of the Graph Node.",
    ):
        assert rule in content


def test_knowledge_object_reference_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Node shall reference one object "
        "registered in the Knowledge Registry.",
        "The Registry Reference shall resolve to the "
        "same Canonical Identifier declared by the "
        "Graph Node.",
        "No unregistered object may be represented as "
        "a Graph Node.",
    ):
        assert rule in content


def test_preferred_name_is_preserved() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Node shall preserve the Preferred "
        "Name of its registered Knowledge Object.",
        "A display label may differ only as a "
        "non-normative presentation property.",
        "A display label shall not replace the "
        "Preferred Name.",
    ):
        assert rule in content


def test_canonical_definition_is_not_redefined() -> None:
    content = normalized_text()

    assert (
        "A Graph Node shall not copy, rewrite, shorten, "
        "extend, or privately redefine a frozen "
        "Canonical Definition."
    ) in content

    assert (
        "The Canonical Definition Reference shall "
        "resolve to the definition maintained by the "
        "Knowledge Registry."
    ) in content


def test_knowledge_object_type_is_preserved() -> None:
    content = normalized_text()

    assert (
        "Every Graph Node shall preserve the canonical "
        "Knowledge Object Type of its registered "
        "source object."
    ) in content

    assert (
        "Initial Graph Nodes use the TERM Knowledge "
        "Object Type."
    ) in content

    assert (
        "Future Graph Nodes may use other object types "
        "only after those objects are registered."
    ) in content


def test_lifecycle_behavior_is_defined() -> None:
    content = normalized_text()

    for lifecycle_status in (
        "Draft.",
        "Approved.",
        "Deprecated.",
        "Retired.",
    ):
        assert lifecycle_status in model_text()

    assert (
        "Graph Node lifecycle shall remain compatible "
        "with the lifecycle of its source Knowledge Object."
    ) in content

    assert (
        "A Graph Node shall not remain active after "
        "its source Knowledge Object is Retired."
    ) in content


def test_ontology_membership_is_preserved() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Node shall reference its frozen "
        "CKP-002 Ontology membership.",
        "Ontology membership shall not be inferred by "
        "the Graph.",
        "The Graph shall preserve the Ontology Class "
        "and assertions already established by CKP-002.",
    ):
        assert rule in content


def test_domain_membership_is_preserved() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Node shall preserve one or more "
        "canonical Domain Membership assertions.",
        "Domain Membership shall derive from the "
        "frozen Commerce Ontology.",
        "Domain-specific presentation shall not "
        "redefine canonical domain membership.",
    ):
        assert rule in content


def test_registry_resolution_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Node shall maintain a resolvable "
        "reference to its source Knowledge Registry record."
    ) in content

    for field_name in (
        "Canonical Identifier.",
        "Preferred Name.",
        "Knowledge Object Type.",
        "Lifecycle Status.",
    ):
        assert field_name in model_text()


def test_frozen_baseline_references_are_required() -> None:
    content = normalized_text()

    assert (
        "CKP-001 Canonical Commerce Vocabulary 1.0."
        in model_text()
    )

    assert (
        "CKP-002 Commerce Ontology 1.0."
        in model_text()
    )

    assert (
        "Baseline references shall remain explicit "
        "and auditable."
    ) in content


def test_node_integrity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Node shall possess one "
        "deterministic Node Integrity Reference."
    ) in content

    for bound_property in (
        "Canonical Identifier.",
        "Knowledge Object Type.",
        "Preferred Name.",
        "Lifecycle Status.",
        "Ontology Membership.",
        "Domain Membership.",
        "Registry Reference.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
    ):
        assert bound_property in model_text()


def test_root_graph_node_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "CKP-TERM-000001 is the root Graph Node of "
        "the initial Commerce Knowledge Graph.",
        "Its Preferred Name is Commerce.",
        "The root Graph Node shall not declare an "
        "incoming canonical Is A edge inside the "
        "initial graph.",
        "Exactly one root Graph Node shall exist.",
    ):
        assert rule in content


def test_initial_graph_nodes_are_declared() -> None:
    content = model_text()

    for node in INITIAL_NODES:
        assert node in content

    assert (
        "No additional Graph Node may enter the "
        "initial graph."
    ) in normalized_text()


def test_deterministic_ordering_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Graph Nodes shall be ordered by Canonical "
        "Identifier when no explicit semantic order is "
        "defined.",
        "Identical Graph Node sets shall produce the "
        "same deterministic ordering.",
        "Presentation order shall not alter semantic identity.",
    ):
        assert rule in content


def test_node_equality_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Two Graph Node representations are equal "
        "when all normative Graph Node Properties are equal.",
        "Display-only presentation properties shall "
        "not affect normative Graph Node equality.",
        "Two different Canonical Identifiers shall "
        "never represent the same Graph Node.",
    ):
        assert rule in content


def test_node_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Graph Node shall reference one "
        "registered Knowledge Object.",
        "Every Graph Node shall preserve one immutable "
        "Canonical Identifier.",
        "Every Graph Node shall preserve its Preferred Name.",
        "Every Graph Node shall preserve its Knowledge "
        "Object Type.",
        "Every Graph Node shall reference the frozen "
        "Vocabulary and Ontology baselines.",
        "No Graph Node shall privately redefine "
        "canonical Commerce semantics.",
        "No duplicate Canonical Identifier shall exist "
        "inside one Commerce Knowledge Graph.",
        "No orphan Graph Node shall exist.",
        "No Graph Node shall represent more than one "
        "Knowledge Object.",
    ):
        assert constraint in content


def test_node_invariants_are_declared() -> None:
    content = model_text()

    for invariant in NODE_INVARIANTS:
        assert invariant in content


def test_node_validation_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Node validation shall produce "
        "deterministic Node Validation Evidence."
    ) in content

    for field_name in VALIDATION_EVIDENCE_FIELDS:
        assert field_name in model_text()


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Graph Node is explicitly defined.",
        "Graph Node Properties are explicitly defined.",
        "Canonical Identity behavior is defined.",
        "Knowledge Registry resolution is defined.",
        "Preferred Name preservation is defined.",
        "Canonical Definition behavior is defined.",
        "Knowledge Object Type preservation is defined.",
        "Lifecycle behavior is defined.",
        "Ontology and Domain Membership are defined.",
        "Baseline References are defined.",
        "Node Integrity is defined.",
        "Root Graph Node is declared.",
        "Initial Graph Nodes are declared.",
        "Deterministic Ordering is defined.",
        "Node Equality is defined.",
        "Node Constraints are declared.",
        "Node Invariants are declared.",
        "Node Validation Evidence is defined.",
    ):
        assert criterion in content
