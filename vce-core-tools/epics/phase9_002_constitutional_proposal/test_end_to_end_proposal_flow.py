from epics.phase9_002_constitutional_proposal.proposal_record import (
    ProposalRecord,
)
from epics.phase9_002_constitutional_proposal.proposal_registry import (
    ProposalRegistry,
)
from epics.phase9_002_constitutional_proposal.proposal_state import (
    ProposalState,
)
from epics.phase9_002_constitutional_proposal.proposal_verifier import (
    verify_proposals,
)


def test_end_to_end_proposal_flow():
    registry = ProposalRegistry()

    registry.add(
        ProposalRecord(
            "proposal.001",
            "intent.001",
            "Preserve Historical Evidence",
        )
    )

    registry.add(
        ProposalRecord(
            "proposal.002",
            "intent.002",
            "Expand Observation Network",
        )
    )

    state = ProposalState.from_records(
        registry.records()
    )

    verification = verify_proposals(state)

    assert verification["verified"] is True
    assert verification["total_proposals"] == 2
