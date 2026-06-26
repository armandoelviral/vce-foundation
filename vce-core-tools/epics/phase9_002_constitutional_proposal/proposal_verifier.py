from epics.phase9_002_constitutional_proposal.proposal_state import (
    ProposalState,
)


def verify_proposals(
    state: ProposalState,
):
    return {
        "verified": state.total_proposals > 0,
        "total_proposals": state.total_proposals,
    }
