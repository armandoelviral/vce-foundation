from phase3.unified_evidence_graph.evidence_edge import (
    EvidenceEdge,
)


def test_edge_contains_source():

    edge = EvidenceEdge(
        source_id="execution-001",
        target_id="policy-001",
    )

    assert edge.source_id == "execution-001"


def test_edge_contains_target():

    edge = EvidenceEdge(
        source_id="execution-001",
        target_id="policy-001",
    )

    assert edge.target_id == "policy-001"


def test_edge_serializes():

    edge = EvidenceEdge(
        source_id="execution-001",
        target_id="policy-001",
    )

    assert edge.to_dict() == {
        "source_id": "execution-001",
        "target_id": "policy-001",
    }
