from epics.phase9_002_constitutional_proposal.proposal_record import (
    ProposalRecord,
)
from epics.phase9_002_constitutional_proposal.proposal_registry import (
    ProposalRegistry,
)


def test_registry_adds_proposal():
    registry = ProposalRegistry()

    proposal = ProposalRecord(
        "proposal.001",
        "intent.001",
        "Preserve Historical Evidence",
    )

    registry.add(proposal)

    assert registry.records() == [proposal]
