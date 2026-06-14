from dataclasses import dataclass
from typing import Dict
from typing import Any

from epics.ztc14_transparency_gossip_protocol.gossip_evidence_record import (
    GossipEvidenceRecord,
)


@dataclass(frozen=True)
class GossipTransparencyAnchor:

    anchor_id: str
    evidence: GossipEvidenceRecord

    def to_dict(
        self,
    ) -> Dict[str, Any]:

        return {
            "anchor_id": self.anchor_id,
            "evidence": self.evidence.to_dict(),
        }
