from epics.phase9_002_constitutional_proposal.proposal_state import (
    ProposalState,
)
from epics.phase9_002_constitutional_proposal.proposal_verifier import (
    verify_proposals,
)


def test_proposals_verified():
    state = ProposalState(
        total_proposals=2,
    )

    result = verify_proposals(state)

    assert result["verified"] is True


def test_empty_proposals_not_verified():
    state = ProposalState(
        total_proposals=0,
    )

    result = verify_proposals(state)

    assert result["verified"] is False
