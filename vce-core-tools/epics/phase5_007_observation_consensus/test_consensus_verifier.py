from epics.phase5_007_observation_consensus.consensus_state import (
    ConsensusState,
)
from epics.phase5_007_observation_consensus.consensus_verifier import (
    verify_consensus_state,
)


def test_consensus_verification_succeeds():
    state = ConsensusState(
        total_votes=3,
        yes_votes=2,
        no_votes=1,
    )

    result = verify_consensus_state(state)

    assert result["verified"] is True


def test_consensus_verification_fails():
    state = ConsensusState(
        total_votes=3,
        yes_votes=1,
        no_votes=2,
    )

    result = verify_consensus_state(state)

    assert result["verified"] is False


def test_empty_consensus_fails():
    state = ConsensusState(
        total_votes=0,
        yes_votes=0,
        no_votes=0,
    )

    result = verify_consensus_state(state)

    assert result["verified"] is False
