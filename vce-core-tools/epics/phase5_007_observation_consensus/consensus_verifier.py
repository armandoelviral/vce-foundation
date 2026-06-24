from epics.phase5_007_observation_consensus.consensus_state import (
    ConsensusState,
)


def verify_consensus_state(state: ConsensusState):
    return {
        "verified": state.total_votes > 0 and state.yes_votes > state.total_votes / 2,
        "total_votes": state.total_votes,
        "yes_votes": state.yes_votes,
        "no_votes": state.no_votes,
    }
