from phase4.trusted_compute_network_governance.suspension_decision import (
    SuspensionDecision,
)


def test_contains_target():

    decision = SuspensionDecision(
        proposal_id="proposal-002",
        target_did="did:tcn:test:02",
        approved=True,
        vote_count=4,
    )

    assert decision.target_did == (
        "did:tcn:test:02"
    )


def test_contains_decision():

    decision = SuspensionDecision(
        proposal_id="proposal-002",
        target_did="did:tcn:test:02",
        approved=True,
        vote_count=4,
    )

    assert decision.approved is True


def test_contains_vote_count():

    decision = SuspensionDecision(
        proposal_id="proposal-002",
        target_did="did:tcn:test:02",
        approved=True,
        vote_count=4,
    )

    assert decision.vote_count == 4


def test_serializes():

    decision = SuspensionDecision(
        proposal_id="proposal-002",
        target_did="did:tcn:test:02",
        approved=True,
        vote_count=4,
    )

    assert decision.to_dict() == {
        "proposal_id": "proposal-002",
        "target_did": "did:tcn:test:02",
        "approved": True,
        "vote_count": 4,
    }
