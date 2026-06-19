from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ConsensusRecord:

    consensus_id: str
    proposal_id: str
    outcome: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "consensus_id":
                self.consensus_id,

            "proposal_id":
                self.proposal_id,

            "outcome":
                self.outcome,
        }
