from phase4.governance_voting_layer.governance_proposal import (
    GovernanceProposal,
)


def test_contains_proposal_id():

    proposal = GovernanceProposal(
        proposal_id="proposal-001",
        title="Increase minimum reputation requirement",
    )

    assert proposal.proposal_id == (
        "proposal-001"
    )


def test_contains_title():

    proposal = GovernanceProposal(
        proposal_id="proposal-001",
        title="Increase minimum reputation requirement",
    )

    assert proposal.title == (
        "Increase minimum reputation requirement"
    )


def test_serializes():

    proposal = GovernanceProposal(
        proposal_id="proposal-001",
        title="Increase minimum reputation requirement",
    )

    assert proposal.to_dict() == {
        "proposal_id":
            "proposal-001",
        "title":
            "Increase minimum reputation requirement",
    }
