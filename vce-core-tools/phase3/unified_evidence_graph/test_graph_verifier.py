from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)

from phase3.unified_evidence_graph.evidence_edge import (
    EvidenceEdge,
)

from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)

from phase3.unified_evidence_graph.graph_verifier import (
    GraphVerifier,
)


def test_valid_graph_passes():

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

    assert (
        GraphVerifier.verify(
            graph
        )
        is True
    )


def test_missing_target_fails():

    graph = EvidenceGraph()

    graph.add_node(
        EvidenceNode(
            node_id="execution-001",
            node_type="execution",
        )
    )

    graph.add_edge(
        EvidenceEdge(
            source_id="execution-001",
            target_id="missing",
        )
    )

    assert (
        GraphVerifier.verify(
            graph
        )
        is False
    )


def test_missing_source_fails():

    graph = EvidenceGraph()

    graph.add_node(
        EvidenceNode(
            node_id="policy-001",
            node_type="policy",
        )
    )

    graph.add_edge(
        EvidenceEdge(
            source_id="missing",
            target_id="policy-001",
        )
    )

    assert (
        GraphVerifier.verify(
            graph
        )
        is False
    )
