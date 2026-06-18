from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)

from phase3.unified_evidence_graph.evidence_edge import (
    EvidenceEdge,
)

from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)


def test_graph_starts_empty():

    graph = EvidenceGraph()

    assert graph.node_count() == 0
    assert graph.edge_count() == 0


def test_graph_accepts_node():

    graph = EvidenceGraph()

    graph.add_node(
        EvidenceNode(
            node_id="execution-001",
            node_type="execution",
        )
    )

    assert graph.node_count() == 1


def test_graph_accepts_edge():

    graph = EvidenceGraph()

    graph.add_edge(
        EvidenceEdge(
            source_id="execution-001",
            target_id="policy-001",
        )
    )

    assert graph.edge_count() == 1


def test_graph_returns_node():

    graph = EvidenceGraph()

    node = EvidenceNode(
        node_id="execution-001",
        node_type="execution",
    )

    graph.add_node(node)

    recovered = graph.get_node(
        "execution-001"
    )

    assert recovered == node


def test_graph_returns_edges():

    graph = EvidenceGraph()

    edge = EvidenceEdge(
        source_id="execution-001",
        target_id="policy-001",
    )

    graph.add_edge(edge)

    edges = graph.edges()

    assert len(edges) == 1
