from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)


def calculate_consensus(records: list[ConsensusRecord]):
    yes_votes = sum(1 for record in records if record.vote)
    total_votes = len(records)

    return {
        "accepted": total_votes > 0 and yes_votes > total_votes / 2,
        "yes_votes": yes_votes,
        "total_votes": total_votes,
    }
