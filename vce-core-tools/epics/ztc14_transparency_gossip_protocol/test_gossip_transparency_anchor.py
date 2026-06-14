from epics.ztc14_transparency_gossip_protocol.gossip_evidence_record import (
    GossipEvidenceRecord,
)

from epics.ztc14_transparency_gossip_protocol.gossip_transparency_anchor import (
    GossipTransparencyAnchor,
)


def test_anchor_contains_anchor_id():

    record = GossipEvidenceRecord(
        registry_a="registry-a",
        registry_b="registry-b",
        verdict=True,
    )

    anchor = GossipTransparencyAnchor(
        anchor_id="anchor-001",
        evidence=record,
    )

    assert anchor.anchor_id == "anchor-001"


def test_anchor_contains_evidence():

    record = GossipEvidenceRecord(
        registry_a="registry-a",
        registry_b="registry-b",
        verdict=True,
    )

    anchor = GossipTransparencyAnchor(
        anchor_id="anchor-001",
        evidence=record,
    )

    assert anchor.evidence == record


def test_anchor_serializes():

    record = GossipEvidenceRecord(
        registry_a="registry-a",
        registry_b="registry-b",
        verdict=True,
    )

    anchor = GossipTransparencyAnchor(
        anchor_id="anchor-001",
        evidence=record,
    )

    assert anchor.to_dict() == {
        "anchor_id": "anchor-001",
        "evidence": record.to_dict(),
    }
