from dataclasses import dataclass

from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)


@dataclass(frozen=True)
class ConsensusState:
    total_votes: int
    yes_votes: int
    no_votes: int

    @classmethod
    def from_records(cls, records: list[ConsensusRecord]):
        yes_votes = sum(1 for record in records if record.vote)
        total_votes = len(records)

        return cls(
            total_votes=total_votes,
            yes_votes=yes_votes,
            no_votes=total_votes - yes_votes,
        )
