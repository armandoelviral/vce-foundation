from phase4.constitutional_evolution_layer.constitution_amendment import (
    ConstitutionAmendment,
)


def test_contains_amendment_id():

    amendment = ConstitutionAmendment(
        amendment_id="amendment-001",
        proposal_id="const-proposal-001",
    )

    assert amendment.amendment_id == (
        "amendment-001"
    )


def test_contains_proposal_id():

    amendment = ConstitutionAmendment(
        amendment_id="amendment-001",
        proposal_id="const-proposal-001",
    )

    assert amendment.proposal_id == (
        "const-proposal-001"
    )


def test_serializes():

    amendment = ConstitutionAmendment(
        amendment_id="amendment-001",
        proposal_id="const-proposal-001",
    )

    assert amendment.to_dict() == {
        "amendment_id":
            "amendment-001",
        "proposal_id":
            "const-proposal-001",
    }
