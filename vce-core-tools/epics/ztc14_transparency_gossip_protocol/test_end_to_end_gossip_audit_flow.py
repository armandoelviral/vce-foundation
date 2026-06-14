from epics.ztc14_transparency_gossip_protocol.gossip_message import (
    GossipMessage,
)

from epics.ztc14_transparency_gossip_protocol.gossip_registry import (
    GossipRegistry,
)

from epics.ztc14_transparency_gossip_protocol.gossip_divergence_detector import (
    GossipDivergenceDetector,
)

from epics.ztc14_transparency_gossip_protocol.gossip_consistency_report import (
    GossipConsistencyReport,
)

from epics.ztc14_transparency_gossip_protocol.gossip_auditor import (
    GossipAuditor,
)

from epics.ztc14_transparency_gossip_protocol.gossip_evidence_record import (
    GossipEvidenceRecord,
)

from epics.ztc14_transparency_gossip_protocol.gossip_transparency_anchor import (
    GossipTransparencyAnchor,
)


def test_end_to_end_gossip_audit_flow():

    registry = GossipRegistry()

    message_a = GossipMessage(
        registry_id="registry-a",
        transparency_root="root-001",
        sequence_number=1,
    )

    message_b = GossipMessage(
        registry_id="registry-b",
        transparency_root="root-001",
        sequence_number=1,
    )

    registry.add(message_a)
    registry.add(message_b)

    divergent = GossipDivergenceDetector.detect(
        root_a=message_a.transparency_root,
        root_b=message_b.transparency_root,
    )

    report = GossipConsistencyReport(
        registry_a="registry-a",
        registry_b="registry-b",
        consistent=not divergent,
    )

    verdict = GossipAuditor.audit(
        report
    )

    evidence = GossipEvidenceRecord(
        registry_a="registry-a",
        registry_b="registry-b",
        verdict=verdict,
    )

    anchor = GossipTransparencyAnchor(
        anchor_id="anchor-001",
        evidence=evidence,
    )

    assert verdict is True
    assert anchor.anchor_id == "anchor-001"
    assert anchor.evidence.verdict is True
