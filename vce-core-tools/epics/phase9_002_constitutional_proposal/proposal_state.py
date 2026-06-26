from dataclasses import dataclass

from epics.phase9_002_constitutional_proposal.proposal_record import (
    ProposalRecord,
)


@dataclass(frozen=True)
class ProposalState:
    total_proposals: int

    @classmethod
    def from_records(
        cls,
        proposals: list[ProposalRecord],
    ):
        return cls(
            total_proposals=len(proposals),
        )
