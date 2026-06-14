from epics.ztc14_transparency_gossip_protocol.gossip_consistency_report import (
    GossipConsistencyReport,
)


class GossipAuditor:

    @staticmethod
    def audit(
        report: GossipConsistencyReport,
    ) -> bool:

        return report.consistent
