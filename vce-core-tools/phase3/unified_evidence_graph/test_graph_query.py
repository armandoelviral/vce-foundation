from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)

from phase3.unified_evidence_graph.evidence_graph import (
    EvidenceGraph,
)

from phase3.unified_evidence_graph.graph_query import (
    GraphQuery,
)


def test_query_returns_node():

    graph = EvidenceGraph()

    node = EvidenceNode(
        node_id="execution-001",
        node_type="execution",
    )

    graph.add_node(node)

    query = GraphQuery(graph)

    result = query.node(
        "execution-001"
    )

    assert result == node


def test_query_returns_none_for_missing_node():

    graph = EvidenceGraph()

    query = GraphQuery(graph)

    assert query.node(
        "missing"
    ) is None


def test_query_returns_node_type():

    graph = EvidenceGraph()

    node = EvidenceNode(
        node_id="policy-001",
        node_type="policy",
    )

    graph.add_node(node)

    query = GraphQuery(graph)

    result = query.node(
        "policy-001"
    )

    assert result.node_type == "policy"
