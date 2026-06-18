from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)

from phase3.unified_evidence_graph.evidence_edge import (
    EvidenceEdge,
)

from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)

from phase3.unified_evidence_graph.graph_query import (
    GraphQuery,
)

from phase3.unified_evidence_graph.evidence_traversal import (
    EvidenceTraversal,
)

from phase3.unified_evidence_graph.graph_verifier import (
    GraphVerifier,
)

from phase3.unified_evidence_graph.evidence_report import (
    EvidenceReport,
)


def test_end_to_end_unified_evidence_graph():

    graph = EvidenceGraph()

    execution = EvidenceNode(
        node_id="execution-001",
        node_type="execution",
    )

    policy = EvidenceNode(
        node_id="policy-001",
        node_type="policy",
    )

    graph.add_node(execution)
    graph.add_node(policy)

    graph.add_edge(
        EvidenceEdge(
            source_id="execution-001",
            target_id="policy-001",
        )
    )

    query = GraphQuery(graph)

    recovered = query.node(
        "execution-001"
    )

    assert recovered == execution

    traversal = EvidenceTraversal(
        graph
    )

    neighbors = traversal.neighbors(
        "execution-001"
    )

    assert len(neighbors) == 1

    assert (
        neighbors[0].node_id
        == "policy-001"
    )

    assert (
        GraphVerifier.verify(
            graph
        )
        is True
    )

    report = EvidenceReport(
        graph
    )

    assert report.node_count() == 2
    assert report.edge_count() == 1
