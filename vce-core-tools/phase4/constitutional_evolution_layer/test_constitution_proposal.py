from phase4.constitutional_evolution_layer.constitution_proposal import (
    ConstitutionProposal,
)


def test_contains_proposal_id():

    proposal = ConstitutionProposal(
        proposal_id="const-proposal-001",
        title="Ratify Principle #7",
        status="PROPOSED",
    )

    assert (
        proposal.proposal_id
        == "const-proposal-001"
    )


def test_contains_title():

    proposal = ConstitutionProposal(
        proposal_id="const-proposal-001",
        title="Ratify Principle #7",
        status="PROPOSED",
    )

    assert (
        proposal.title
        == "Ratify Principle #7"
    )


def test_contains_status():

    proposal = ConstitutionProposal(
        proposal_id="const-proposal-001",
        title="Ratify Principle #7",
        status="PROPOSED",
    )

    assert (
        proposal.status
        == "PROPOSED"
    )


def test_serializes():

    proposal = ConstitutionProposal(
        proposal_id="const-proposal-001",
        title="Ratify Principle #7",
        status="PROPOSED",
    )

    assert proposal.to_dict() == {
        "proposal_id":
            "const-proposal-001",
        "title":
            "Ratify Principle #7",
        "status":
            "PROPOSED",
    }
