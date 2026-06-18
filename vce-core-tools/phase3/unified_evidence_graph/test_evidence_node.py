from phase3.unified_evidence_graph.evidence_node import (
    EvidenceNode,
)


def test_node_contains_id():

    node = EvidenceNode(
        node_id="execution-001",
        node_type="execution",
    )

    assert node.node_id == "execution-001"


def test_node_contains_type():

    node = EvidenceNode(
        node_id="execution-001",
        node_type="execution",
    )

    assert node.node_type == "execution"


def test_node_serializes():

    node = EvidenceNode(
        node_id="execution-001",
        node_type="execution",
    )

    assert node.to_dict() == {
        "node_id": "execution-001",
        "node_type": "execution",
    }
