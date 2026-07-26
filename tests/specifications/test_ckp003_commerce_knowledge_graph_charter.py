from pathlib import Path


CHARTER = Path(
    "research/commerce/knowledge_graph/"
    "CKP003_COMMERCE_KNOWLEDGE_GRAPH_CHARTER.md"
)

REQUIRED_INPUTS = (
    "CKP-001 Canonical Commerce Vocabulary 1.0.",
    "CKP-002 Commerce Ontology 1.0.",
    "Knowledge Object Architecture.",
    "Knowledge Registry.",
    "Canonical Identifiers.",
    "Ontology Nodes.",
    "Hierarchy Assertions.",
    "Relationship Assertions.",
    "Domain Membership Assertions.",
    "Ontology Constraints.",
    "Ontology Audit Evidence.",
)

REQUIRED_OUTPUTS = (
    "Commerce Knowledge Graph.",
    "Canonical Graph Nodes.",
    "Canonical Graph Edges.",
    "Graph Manifests.",
    "Traversal Results.",
    "Path Evidence.",
    "Graph Validation Evidence.",
    "Graph Audit Report.",
)

INITIAL_TRAVERSALS = (
    "Direct Successor Traversal.",
    "Direct Predecessor Traversal.",
    "Root-to-Node Traversal.",
    "Node-to-Root Traversal.",
    "Relationship-Type Traversal.",
    "Inverse-Relationship Traversal.",
    "Registered Path Validation.",
    "Reachability Validation.",
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
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Deterministic Traversal.",
    "Path Evidence Completeness.",
    "Semantic Closure.",
    "Traceability Closure.",
)


def charter_text() -> str:
    return CHARTER.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        charter_text().split()
    )


def test_ckp003_charter_exists() -> None:
    assert CHARTER.is_file()


def test_ckp003_declares_identity() -> None:
    content = normalized_text()

    assert "CKP-003" in content
    assert "Commerce Knowledge Graph" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_ckp003_declares_vision_and_mission() -> None:
    content = normalized_text()

    assert (
        "canonical, directed, traceable, and auditable "
        "graph representation of Commerce knowledge"
    ) in content

    assert (
        "Transform registered Knowledge Objects and "
        "frozen Ontology Assertions into explicit "
        "Graph Nodes and Graph Edges."
    ) in content


def test_ckp003_declares_required_inputs() -> None:
    content = charter_text()

    for item in REQUIRED_INPUTS:
        assert item in content


def test_ckp003_declares_required_outputs() -> None:
    content = charter_text()

    for item in REQUIRED_OUTPUTS:
        assert item in content


def test_ckp003_declares_graph_model() -> None:
    content = normalized_text()

    assert (
        "Knowledge Objects shall be represented as "
        "Graph Nodes."
    ) in content

    assert (
        "Hierarchy Assertions and Semantic Relationship "
        "Assertions shall be represented as directed "
        "Graph Edges."
    ) in content

    assert (
        "Graph structure shall preserve the frozen "
        "identity and semantics of its source Knowledge "
        "Objects and Ontology Assertions."
    ) in content


def test_ckp003_declares_initial_boundary() -> None:
    content = normalized_text()

    assert (
        "The initial Commerce Knowledge Graph shall "
        "contain exactly ten Graph Nodes."
    ) in content

    assert (
        "The initial graph shall contain exactly "
        "twelve Graph Edges derived from the frozen "
        "CKP-002 relationship assertions."
    ) in content

    assert (
        "Commerce shall remain the only root Graph Node."
    ) in content

    assert (
        "No unregistered Knowledge Object may enter "
        "the initial graph."
    ) in content


def test_ckp003_declares_node_responsibilities() -> None:
    content = normalized_text()

    for responsibility in (
        "Preserve one Canonical Identifier.",
        "Reference one registered Knowledge Object.",
        "Preserve one Preferred Name.",
        "Preserve one Knowledge Object Type.",
        "Preserve one Lifecycle Status.",
        "Preserve ontology membership.",
        "Remain traceable to the Knowledge Registry.",
    ):
        assert responsibility in content


def test_ckp003_declares_edge_responsibilities() -> None:
    content = normalized_text()

    for responsibility in (
        "Possess one immutable Relationship Identifier.",
        "Reference one Source Graph Node.",
        "Use one canonical Relationship Type.",
        "Reference one Target Graph Node.",
        "Preserve explicit directionality.",
        "Preserve inverse relationship references.",
        "Preserve lifecycle status.",
        "Remain traceable to one frozen Ontology Assertion.",
    ):
        assert responsibility in content


def test_ckp003_declares_traversal_responsibilities() -> None:
    content = normalized_text()

    for responsibility in (
        "Traverse only registered Graph Nodes and "
        "canonical Graph Edges.",
        "Preserve edge direction.",
        "Return deterministic traversal order.",
        "Prevent implicit semantic inference.",
        "Produce Path Evidence for every successful "
        "or failed traversal.",
    ):
        assert responsibility in content


def test_ckp003_declares_initial_traversals() -> None:
    content = charter_text()

    for traversal in INITIAL_TRAVERSALS:
        assert traversal in content


def test_ckp003_declares_non_goals() -> None:
    content = normalized_text()

    for non_goal in (
        "modify HAS Foundation 1.0 LTS",
        "modify Specification Runtime 1.0",
        "modify CKP-001 Vocabulary 1.0",
        "modify CKP-002 Ontology 1.0",
        "create new canonical Commerce Terms",
        "redefine frozen canonical definitions",
        "infer undocumented semantic relationships",
        "implement a graph database",
        "select a graph database vendor",
        "require RDF, OWL, SPARQL, or Cypher",
        "implement application services",
        "implement commercial decision logic",
        "create user interfaces",
        "create machine-learning models",
    ):
        assert non_goal in content


def test_ckp003_declares_graph_invariants() -> None:
    content = charter_text()

    for invariant in GRAPH_INVARIANTS:
        assert invariant in content


def test_ckp003_preserves_frozen_baselines() -> None:
    content = normalized_text()

    assert "HAS Foundation 1.0 LTS remains frozen." in content

    assert (
        "Specification Runtime 1.0 remains frozen."
        in content
    )

    assert (
        "CKP-001 Canonical Commerce Vocabulary 1.0 "
        "remains frozen."
    ) in content

    assert (
        "CKP-002 Commerce Ontology 1.0 remains frozen."
        in content
    )

    assert (
        "without modifying their normative behavior, "
        "canonical identity, assertions, or semantics"
    ) in content


def test_ckp003_declares_success_criteria() -> None:
    content = normalized_text()

    for criterion in (
        "Every Graph Node references one registered "
        "Knowledge Object.",
        "Every Graph Edge references registered Graph Nodes.",
        "Every Graph Edge derives from one frozen "
        "Ontology Assertion.",
        "Every edge uses one canonical Relationship Type.",
        "Every traversal preserves directionality.",
        "Every traversal result is deterministic.",
        "Every successful or failed traversal produces "
        "Path Evidence.",
        "No graph element privately redefines frozen "
        "Commerce semantics.",
        "The initial graph remains closed over exactly "
        "ten nodes and twelve edges.",
        "Graph consistency is executable and auditable.",
    ):
        assert criterion in content


def test_ckp003_declares_deliverables() -> None:
    content = charter_text()

    for deliverable in (
        "Commerce Knowledge Graph Charter.",
        "Graph Structure Model.",
        "Graph Node Model.",
        "Graph Edge Model.",
        "Traversal Model.",
        "Initial Commerce Knowledge Graph.",
        "Graph Consistency Audit.",
        "Commerce Knowledge Graph Freeze.",
    ):
        assert deliverable in content


def test_ckp003_declares_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-003.2" in content
    assert "Graph Structure Model" in content
