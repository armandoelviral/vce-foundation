from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)

from phase3.unified_evidence_graph.evidence_edge import (
    EvidenceEdge,
)

from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)

from phase3.unified_evidence_graph.evidence_traversal import (
    EvidenceTraversal,
)


def test_traversal_returns_connected_nodes():

    graph = EvidenceGraph()

    graph.add_node(
        EvidenceNode(
            node_id="execution-001",
            node_type="execution",
        )
    )

    graph.add_node(
        EvidenceNode(
            node_id="policy-001",
            node_type="policy",
        )
    )

    graph.add_edge(
        EvidenceEdge(
            source_id="execution-001",
            target_id="policy-001",
        )
    )

    traversal = EvidenceTraversal(graph)

    results = traversal.neighbors(
        "execution-001"
    )

    assert len(results) == 1
    assert results[0].node_id == "policy-001"


def test_traversal_returns_empty_for_unknown_node():

    graph = EvidenceGraph()

    traversal = EvidenceTraversal(graph)

    assert traversal.neighbors(
        "missing"
    ) == []


def test_traversal_handles_multiple_neighbors():

    graph = EvidenceGraph()

    graph.add_node(
        EvidenceNode(
            node_id="execution-001",
            node_type="execution",
        )
    )

    graph.add_node(
        EvidenceNode(
            node_id="policy-001",
            node_type="policy",
        )
    )

    graph.add_node(
        EvidenceNode(
            node_id="attestation-001",
            node_type="attestation",
        )
    )

    graph.add_edge(
        EvidenceEdge(
            source_id="execution-001",
            target_id="policy-001",
        )
    )

    graph.add_edge(
        EvidenceEdge(
            source_id="execution-001",
            target_id="attestation-001",
        )
    )

    traversal = EvidenceTraversal(graph)

    results = traversal.neighbors(
        "execution-001"
    )

    assert len(results) == 2

