from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)

from phase3.unified_evidence_graph.evidence_edge import (
    EvidenceEdge,
)

from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)

from phase3.unified_evidence_graph.evidence_report import (
    EvidenceReport,
)


def test_report_contains_node_count():

    graph = EvidenceGraph()

    graph.add_node(
        EvidenceNode(
            node_id="execution-001",
            node_type="execution",
        )
    )

    report = EvidenceReport(graph)

    assert report.node_count() == 1


def test_report_contains_edge_count():

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

    report = EvidenceReport(graph)

    assert report.edge_count() == 1


def test_report_serializes():

    graph = EvidenceGraph()

    graph.add_node(
        EvidenceNode(
            node_id="execution-001",
            node_type="execution",
        )
    )

    report = EvidenceReport(graph)

    assert report.to_dict() == {
        "node_count": 1,
        "edge_count": 0,
    }
