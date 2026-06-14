from epics.ztc14_transparency_gossip_protocol.gossip_consistency_report import (
    GossipConsistencyReport,
)

from epics.ztc14_transparency_gossip_protocol.gossip_auditor import (
    GossipAuditor,
)


def test_accepts_consistent_report():

    report = GossipConsistencyReport(
        registry_a="registry-a",
        registry_b="registry-b",
        consistent=True,
    )

    assert GossipAuditor.audit(report)


def test_rejects_inconsistent_report():

    report = GossipConsistencyReport(
        registry_a="registry-a",
        registry_b="registry-b",
        consistent=False,
    )

    assert not GossipAuditor.audit(report)
