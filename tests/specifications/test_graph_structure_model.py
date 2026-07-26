from pathlib import Path


MODEL = Path(
    "research/commerce/knowledge_graph/"
    "GRAPH_STRUCTURE_MODEL.md"
)

GRAPH_COMPONENTS = (
    "Graph Manifest.",
    "Graph Node.",
    "Graph Edge.",
    "Graph Path.",
    "Traversal Request.",
    "Traversal Result.",
    "Path Evidence.",
    "Graph Constraint.",
    "Graph Validation Evidence.",
)

MANIFEST_PROPERTIES = (
    "Graph Identifier.",
    "Graph Version.",
    "Lifecycle Status.",
    "Root Node Identifier.",
    "Node Count.",
    "Edge Count.",
    "Vocabulary Baseline.",
    "Ontology Baseline.",
    "Node Registry Reference.",
    "Edge Registry Reference.",
    "Graph Integrity Reference.",
)

NODE_PROPERTIES = (
    "Canonical Identifier.",
    "Knowledge Object Type.",
    "Preferred Name.",
    "Lifecycle Status.",
    "Ontology Membership.",
    "Registry Reference.",
    "Source Evidence Reference.",
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
    "Source Evidence Reference.",
)

PATH_PROPERTIES = (
    "Path Identifier.",
    "Start Node Identifier.",
    "End Node Identifier.",
    "Ordered Node Sequence.",
    "Ordered Edge Sequence.",
    "Traversal Direction.",
    "Path Length.",
    "Validation Result.",
    "Evidence Reference.",
)

TRAVERSAL_REQUEST_PROPERTIES = (
    "Request Identifier.",
    "Start Node Identifier.",
    "Traversal Type.",
    "Relationship Type Filter.",
    "Target Node Identifier.",
    "Maximum Depth.",
    "Direction.",
    "Execution Context.",
)

TRAVERSAL_RESULT_PROPERTIES = (
    "Request Identifier.",
    "Traversal Status.",
    "Visited Node Sequence.",
    "Traversed Edge Sequence.",
    "Matched Paths.",
    "Failure Reason.",
    "Path Evidence Reference.",
)

PATH_EVIDENCE_PROPERTIES = (
    "Evidence Identifier.",
    "Traversal Request Identifier.",
    "Start Node Identifier.",
    "End Node Identifier.",
    "Ordered Node Sequence.",
    "Ordered Edge Sequence.",
    "Direction Validation.",
    "Registry Validation.",
    "Relationship Validation.",
    "Result Hash.",
    "Validation Result.",
    "Failure Reason.",
)

GRAPH_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Registered Node Closure.",
    "Canonical Edge Closure.",
    "Single Root Preservation.",
    "Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Hierarchy Acyclicity.",
    "No Duplicate Nodes.",
    "No Duplicate Edges.",
    "Path Continuity.",
    "Deterministic Ordering.",
    "Deterministic Traversal.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Evidence Completeness.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_graph_structure_model_exists() -> None:
    assert MODEL.is_file()


def test_graph_components_are_declared() -> None:
    content = model_text()

    for component in GRAPH_COMPONENTS:
        assert component in content


def test_graph_manifest_structure_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Graph Manifest identifies one canonical "
        "Commerce Knowledge Graph."
    ) in content

    for property_name in MANIFEST_PROPERTIES:
        assert property_name in model_text()


def test_graph_node_structure_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Graph Node represents one registered "
        "Knowledge Object participating in the "
        "Commerce Knowledge Graph."
    ) in content

    for property_name in NODE_PROPERTIES:
        assert property_name in model_text()


def test_graph_edge_structure_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Graph Edge represents one frozen Ontology "
        "Assertion connecting two registered Graph Nodes."
    ) in content

    for property_name in EDGE_PROPERTIES:
        assert property_name in model_text()


def test_graph_path_structure_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Graph Path represents an ordered sequence "
        "of registered Graph Nodes connected by "
        "canonical Graph Edges."
    ) in content

    for property_name in PATH_PROPERTIES:
        assert property_name in model_text()


def test_traversal_request_structure_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Traversal Request defines one explicit "
        "graph navigation operation."
    ) in content

    for property_name in TRAVERSAL_REQUEST_PROPERTIES:
        assert property_name in model_text()


def test_traversal_result_structure_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Traversal Result represents the "
        "deterministic outcome of one Traversal Request."
    ) in content

    for property_name in TRAVERSAL_RESULT_PROPERTIES:
        assert property_name in model_text()


def test_path_evidence_structure_is_defined() -> None:
    content = normalized_text()

    assert (
        "Path Evidence demonstrates how a Traversal "
        "Result was produced."
    ) in content

    for property_name in PATH_EVIDENCE_PROPERTIES:
        assert property_name in model_text()


def test_graph_constraints_are_classified() -> None:
    content = model_text()

    for constraint_type in (
        "Registered Node Closure.",
        "Canonical Edge Closure.",
        "Single Root Preservation.",
        "Direction Preservation.",
        "Inverse Relationship Consistency.",
        "Hierarchy Acyclicity.",
        "No Duplicate Nodes.",
        "No Duplicate Edges.",
        "Path Continuity.",
        "Traversal Determinism.",
        "Maximum Traversal Depth.",
        "Vocabulary Compatibility.",
        "Ontology Compatibility.",
        "Semantic Closure.",
        "Traceability Closure.",
    ):
        assert constraint_type in content


def test_initial_graph_structure_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "The initial Commerce Knowledge Graph shall "
        "declare one Graph Manifest.",
        "Exactly ten Graph Nodes.",
        "Exactly twelve Graph Edges.",
        "Exactly one root Graph Node.",
        "CKP-TERM-000001 as the root Graph Node.",
        "CKP-001 Canonical Commerce Vocabulary 1.0 "
        "as the Vocabulary Baseline.",
        "CKP-002 Commerce Ontology 1.0 as the "
        "Ontology Baseline.",
    ):
        assert requirement in content


def test_node_closure_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Node shall reference one "
        "registered Knowledge Object.",
        "Every initial Graph Node shall reference one "
        "of the first ten Canonical Commerce Terms.",
        "No unregistered Knowledge Object may be "
        "represented as a Graph Node.",
    ):
        assert rule in content


def test_edge_closure_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Edge shall reference registered "
        "Source and Target Graph Nodes.",
        "Every Graph Edge shall derive from one frozen "
        "CKP-002 Ontology Assertion.",
        "Every Graph Edge shall use one canonical "
        "Relationship Type.",
        "No private or implicit edge may enter the Graph.",
    ):
        assert rule in content


def test_directionality_is_preserved() -> None:
    content = normalized_text()

    for rule in (
        "Every Graph Edge shall preserve the "
        "directionality of its source Ontology Assertion.",
        "Traversal shall respect edge direction unless "
        "the Traversal Request explicitly selects a "
        "canonical inverse relationship.",
        "Presentation order shall not redefine graph direction.",
    ):
        assert rule in content


def test_path_continuity_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every adjacent Node pair in a Graph Path "
        "shall be connected by the corresponding Graph Edge.",
        "The Target Node of one traversed edge shall "
        "equal the Source Node of the next traversed edge.",
        "A disconnected sequence shall not be treated "
        "as a valid Graph Path.",
    ):
        assert rule in content


def test_deterministic_ordering_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Graph Nodes shall use Canonical Identifier "
        "ordering when no semantic ordering is "
        "explicitly defined.",
        "Graph Edges shall use Relationship Identifier "
        "ordering when no semantic ordering is "
        "explicitly defined.",
        "Traversal Results shall preserve deterministic "
        "ordering across identical inputs.",
    ):
        assert rule in content


def test_graph_identity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Commerce Knowledge Graph shall possess "
        "one immutable Graph Identifier."
    ) in content

    assert "CKP-GRAPH-000001" in content

    assert (
        "Graph identity shall remain distinct from "
        "Graph version."
    ) in content

    assert "Graph Identifiers shall never be reused." in content


def test_graph_invariants_are_declared() -> None:
    content = model_text()

    for invariant in GRAPH_INVARIANTS:
        assert invariant in content


def test_prohibited_behavior_is_declared() -> None:
    content = normalized_text()

    for constraint in (
        "No Graph Node may exist without a registered "
        "Knowledge Object.",
        "No Graph Edge may exist without a frozen "
        "Ontology Assertion.",
        "No Graph Path may contain a disconnected "
        "Node or Edge sequence.",
        "No Graph Component may privately redefine "
        "frozen canonical Commerce semantics.",
        "No traversal may create an implicit semantic "
        "relationship.",
        "No traversal may exceed its declared Maximum Depth.",
        "No duplicate Graph Identifier may exist.",
    ):
        assert constraint in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Graph Components are explicitly defined.",
        "Graph Manifest structure is explicitly defined.",
        "Graph Node structure is explicitly defined.",
        "Graph Edge structure is explicitly defined.",
        "Graph Path structure is explicitly defined.",
        "Traversal Request and Result structures are "
        "explicitly defined.",
        "Path Evidence is explicitly defined.",
        "Graph Constraints are explicitly defined.",
        "Initial Graph Structure is declared.",
        "Node and Edge Closure are declared.",
        "Directionality and Path Continuity are declared.",
        "Deterministic Ordering is declared.",
        "Graph Identity is declared.",
        "Graph Invariants are declared.",
    ):
        assert criterion in content
