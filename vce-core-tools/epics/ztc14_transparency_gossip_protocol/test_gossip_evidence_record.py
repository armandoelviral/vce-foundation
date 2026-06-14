from epics.ztc14_transparency_gossip_protocol.gossip_evidence_record import (
    GossipEvidenceRecord,
)


def test_record_contains_registries():

    record = GossipEvidenceRecord(
        registry_a="registry-a",
        registry_b="registry-b",
        verdict=True,
    )

    assert record.registry_a == "registry-a"
    assert record.registry_b == "registry-b"


def test_record_contains_verdict():

    record = GossipEvidenceRecord(
        registry_a="registry-a",
        registry_b="registry-b",
        verdict=False,
    )

    assert record.verdict is False


def test_record_serializes():

    record = GossipEvidenceRecord(
        registry_a="registry-a",
        registry_b="registry-b",
        verdict=True,
    )

    assert record.to_dict() == {
        "registry_a": "registry-a",
        "registry_b": "registry-b",
        "verdict": True,
    }
