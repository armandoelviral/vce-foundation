from epics.phase9_002_constitutional_proposal.proposal_record import (
    ProposalRecord,
)
from epics.phase9_002_constitutional_proposal.proposal_state import (
    ProposalState,
)


def test_builds_proposal_state():
    proposals = [
        ProposalRecord(
            "proposal.001",
            "intent.001",
            "Preserve Historical Evidence",
        ),
        ProposalRecord(
            "proposal.002",
            "intent.002",
            "Expand Observation Network",
        ),
    ]

    state = ProposalState.from_records(proposals)

    assert state.total_proposals == 2


def test_empty_proposal_state():
    state = ProposalState.from_records([])

    assert state.total_proposals == 0
