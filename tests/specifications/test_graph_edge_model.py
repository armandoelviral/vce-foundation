from pathlib import Path


MODEL = Path(
    "research/commerce/knowledge_graph/"
    "GRAPH_EDGE_MODEL.md"
)

EDGE_PROPERTIES = (
    "Relationship Identifier.",
    "Source Node Identifier.",
    "Canonical Relationship Type.",
    "Target Node Identifier.",
    "Directionality.",
    "Inverse Relationship Reference.",
    "Lifecycle Status.",
    "Ontology Assertion Reference.",
    "Vocabulary Baseline Reference.",
    "Ontology Baseline Reference.",
    "Source Evidence Reference.",
    "Edge Integrity Reference.",
)

INITIAL_EDGES = (
    ("CKP-REL-000001", "Retail Is A Commerce."),
    ("CKP-REL-000002", "Wholesale Is A Commerce."),
    ("CKP-REL-000003", "Ecommerce Is A Commerce."),
    (
        "CKP-REL-000004",
        "Informal Commerce Is A Commerce.",
    ),
    ("CKP-REL-000005", "SKU Part Of Product."),
    ("CKP-REL-000006", "Product Contains SKU."),
    ("CKP-REL-000007", "Product Tracked As SKU."),
    ("CKP-REL-000008", "Retail Uses Channel."),
    ("CKP-REL-000009", "Channel Used By Retail."),
    (
        "CKP-REL-000010",
        "Product Sold Through Channel.",
    ),
    (
        "CKP-REL-000011",
        "Inventory Applies To SKU.",
    ),
    ("CKP-REL-000012", "Customer Uses Channel."),
)

EDGE_INVARIANTS = (
    "Relationship Identity Preservation.",
    "Ontology Assertion Closure.",
    "Registered Source Node Closure.",
    "Registered Target Node Closure.",
    "Canonical Relationship Type Preservation.",
    "Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Lifecycle Compatibility.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "No Duplicate Edges.",
    "No Orphan Edges.",
    "No Implicit Edges.",
    "No Initial Reflexivity.",
    "Deterministic Ordering.",
    "Normative Equality.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Edge Evidence Completeness.",
)

VALIDATION_EVIDENCE_FIELDS = (
    "Evidence Identifier.",
    "Relationship Identifier.",
    "Ontology Assertion Resolution Result.",
    "Source Node Resolution Result.",
    "Target Node Resolution Result.",
    "Relationship Type Validation.",
    "Directionality Validation.",
    "Inverse Relationship Validation.",
    "Lifecycle Validation.",
    "Vocabulary Baseline Validation.",
    "Ontology Baseline Validation.",
    "Edge Integrity Result.",
    "Duplicate Detection Result.",
    "Reflexivity Validation.",
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


def test_graph_edge_model_exists() -> None:
    assert MODEL.is_file()


def test_graph_edge_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Edge shall represent exactly one "
        "frozen CKP-002 Ontology Assertion."
    ) in content

    assert (
        "A Graph Edge is a directed graph "
        "representation of an existing semantic assertion."
    ) in content

    assert (
        "A Graph Edge shall not become an independent "
        "source of canonical meaning."
    ) in content


def test_graph_edge_properties_are_declared() -> None:
    content = model_text()

    for property_name in EDGE_PROPERTIES:
        assert property_name in content


def test_relationship_identity_is_preserved() -> None:
    content = normalized_text()

    for rule in (
        "A Graph Edge shall inherit the Relationship "
        "Identifier of its frozen Ontology Assertion.",
        "Graph representation shall not allocate a "
        "second semantic identifier for the same "
        "Ontology Assertion.",
        "The Relationship Identifier shall remain immutable.",
        "Relationship Identifiers shall never be reused.",
    ):
        assert rule in content


def test_ontology_assertion_reference_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Edge shall reference exactly one "
        "frozen CKP-002 Ontology Assertion."
    ) in content

    for property_name in (
        "Relationship Identifier.",
        "Source Node Identifier.",
        "Canonical Relationship Type.",
        "Target Node Identifier.",
        "Directionality.",
        "Inverse Relationship Reference.",
    ):
        assert property_name in model_text()

    assert (
        "No Graph Edge may exist without a resolvable "
        "Ontology Assertion Reference."
    ) in content


def test_source_graph_node_resolution_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Edge shall reference one "
        "registered Source Graph Node.",
        "The Source Node Identifier shall resolve to "
        "one Graph Node in the same Graph Manifest.",
        "The Source Graph Node shall preserve its "
        "Canonical Identifier.",
        "No private Source Node Identifier may be introduced.",
    ):
        assert rule in content


def test_target_graph_node_resolution_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Edge shall reference one "
        "registered Target Graph Node.",
        "The Target Node Identifier shall resolve to "
        "one Graph Node in the same Graph Manifest.",
        "The Target Graph Node shall preserve its "
        "Canonical Identifier.",
        "No private Target Node Identifier may be introduced.",
    ):
        assert rule in content


def test_canonical_relationship_types_are_preserved() -> None:
    content = normalized_text()

    assert (
        "Every Graph Edge shall preserve the canonical "
        "Relationship Type declared by its frozen "
        "Ontology Assertion."
    ) in content

    for relationship_type in (
        "Is A.",
        "Part Of.",
        "Contains.",
        "Tracked As.",
        "Uses.",
        "Used By.",
        "Sold Through.",
        "Applies To.",
    ):
        assert relationship_type in model_text()

    assert (
        "A Graph Edge shall not replace a specific "
        "canonical Relationship Type with Related To."
    ) in content

    assert (
        "A Graph Edge shall not introduce a private "
        "Relationship Type."
    ) in content


def test_directionality_is_preserved() -> None:
    content = normalized_text()

    assert (
        "Every Graph Edge shall preserve the explicit "
        "directionality of its frozen Ontology Assertion."
    ) in content

    for directionality in (
        "Unidirectional.",
        "Bidirectional.",
        "Inverse-Paired.",
    ):
        assert directionality in model_text()

    assert (
        "Source and Target presentation order shall "
        "not redefine edge direction."
    ) in content

    assert (
        "A reverse traversal shall not mutate the "
        "original Graph Edge."
    ) in content


def test_inverse_relationship_behavior_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Inverse-Paired Graph Edge shall "
        "reference its canonical inverse Graph Edge."
    ) in content

    for rule in (
        "Reference the same participating Graph Nodes.",
        "Reverse Source and Target Node identifiers.",
        "Use the canonical inverse Relationship Type.",
        "Reference the original Graph Edge as its inverse.",
        "Preserve compatible Lifecycle Status.",
    ):
        assert rule in content

    assert (
        "A Unidirectional Graph Edge shall declare: "
        "None as its Inverse Relationship Reference."
    ) in content


def test_canonical_inverse_pairs_are_declared() -> None:
    content = normalized_text()

    assert "Part Of is inverse to Contains." in content
    assert "Uses is inverse to Used By." in content

    assert (
        "CKP-REL-000005 as inverse-paired with "
        "CKP-REL-000006."
    ) in content

    assert (
        "CKP-REL-000008 as inverse-paired with "
        "CKP-REL-000009."
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
        "Graph Edge lifecycle shall remain compatible "
        "with the lifecycle of its source Ontology Assertion."
    ) in content

    assert (
        "A Graph Edge shall not remain active after "
        "its source Ontology Assertion is Retired."
    ) in content

    assert (
        "Inverse-paired Graph Edges shall preserve "
        "compatible lifecycle states."
    ) in content


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
        "Baseline references shall remain explicit, "
        "resolvable, and auditable."
    ) in content


def test_edge_integrity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Edge shall possess one "
        "deterministic Edge Integrity Reference."
    ) in content

    for bound_property in (
        "Relationship Identifier.",
        "Source Node Identifier.",
        "Canonical Relationship Type.",
        "Target Node Identifier.",
        "Directionality.",
        "Inverse Relationship Reference.",
        "Lifecycle Status.",
        "Ontology Assertion Reference.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
    ):
        assert bound_property in model_text()


def test_initial_graph_edges_are_declared() -> None:
    content = model_text()

    for identifier, assertion in INITIAL_EDGES:
        assert identifier in content
        assert assertion in content

    assert (
        "No additional Graph Edge may enter the "
        "initial graph."
    ) in normalized_text()


def test_hierarchy_edges_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "CKP-REL-000001 through CKP-REL-000004 are "
        "canonical hierarchy Graph Edges.",
        "Every hierarchy Graph Edge shall use the "
        "canonical Is A Relationship Type.",
        "Hierarchy Graph Edges shall be directed from "
        "the specialized Source Graph Node to the "
        "broader Target Graph Node.",
        "Hierarchy Graph Edges shall preserve acyclicity.",
        "No Graph Node may become its own ancestor.",
    ):
        assert rule in content


def test_semantic_edges_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "CKP-REL-000005 through CKP-REL-000012 are "
        "canonical semantic Graph Edges.",
        "Semantic Graph Edges shall preserve the "
        "Relationship Type, directionality, and "
        "inverse references declared by CKP-002.",
        "Semantic Graph Edges shall not create "
        "undocumented meaning.",
    ):
        assert rule in content


def test_edge_uniqueness_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Graph Edge is uniquely identified by its "
        "Relationship Identifier.",
        "No duplicate Relationship Identifier shall "
        "exist inside one Commerce Knowledge Graph.",
        "Two Graph Edges shall not represent the same "
        "normative assertion under different "
        "Relationship Identifiers.",
        "Source Node Identifier. Canonical Relationship "
        "Type. Target Node Identifier. shall not be "
        "duplicated unless the ontology explicitly "
        "distinguishes the assertions.",
    ):
        assert rule in content


def test_edge_equality_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Two Graph Edge representations are equal "
        "when all normative Graph Edge Properties are equal.",
        "Display-only presentation properties shall "
        "not affect normative Graph Edge equality.",
        "Different Relationship Identifiers shall not "
        "be treated as the same Graph Edge.",
    ):
        assert rule in content


def test_deterministic_ordering_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Graph Edges shall be ordered by Relationship "
        "Identifier when no explicit semantic order is "
        "defined.",
        "Identical Graph Edge sets shall produce the "
        "same deterministic ordering.",
        "Presentation order shall not alter semantic "
        "identity or directionality.",
    ):
        assert rule in content


def test_self_reference_is_prohibited_initially() -> None:
    content = normalized_text()

    assert (
        "A Graph Edge shall not connect a Graph Node "
        "to itself unless its canonical Relationship "
        "Type explicitly permits reflexivity."
    ) in content

    assert (
        "No initial Graph Edge permits reflexivity."
    ) in content


def test_edge_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Graph Edge shall reference one frozen "
        "Ontology Assertion.",
        "Every Graph Edge shall reference registered "
        "Source and Target Graph Nodes.",
        "Every Graph Edge shall preserve one immutable "
        "Relationship Identifier.",
        "Every Graph Edge shall use one canonical "
        "Relationship Type.",
        "Every Graph Edge shall preserve explicit directionality.",
        "Every Inverse-Paired Graph Edge shall "
        "reference a consistent inverse Graph Edge.",
        "Every Graph Edge shall reference the frozen "
        "Vocabulary and Ontology baselines.",
        "No Graph Edge shall privately redefine "
        "canonical Commerce semantics.",
        "No duplicate Graph Edge shall exist.",
        "No orphan Graph Edge shall exist.",
        "No implicit Graph Edge shall exist.",
        "No initial Graph Edge shall be reflexive.",
    ):
        assert constraint in content


def test_edge_invariants_are_declared() -> None:
    content = model_text()

    for invariant in EDGE_INVARIANTS:
        assert invariant in content


def test_edge_validation_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Graph Edge validation shall produce "
        "deterministic Edge Validation Evidence."
    ) in content

    for field_name in VALIDATION_EVIDENCE_FIELDS:
        assert field_name in model_text()


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Graph Edge is explicitly defined.",
        "Graph Edge Properties are explicitly defined.",
        "Relationship Identity behavior is defined.",
        "Ontology Assertion resolution is defined.",
        "Source and Target Graph Node resolution is defined.",
        "Canonical Relationship Type preservation is defined.",
        "Directionality behavior is defined.",
        "Inverse Relationship behavior is defined.",
        "Lifecycle behavior is defined.",
        "Baseline References are defined.",
        "Edge Integrity is defined.",
        "Initial Graph Edges are declared.",
        "Hierarchy and Semantic Edges are distinguished.",
        "Edge Uniqueness is defined.",
        "Edge Equality is defined.",
        "Deterministic Ordering is defined.",
        "Self-Reference behavior is defined.",
        "Edge Constraints are declared.",
        "Edge Invariants are declared.",
        "Edge Validation Evidence is defined.",
    ):
        assert criterion in content
