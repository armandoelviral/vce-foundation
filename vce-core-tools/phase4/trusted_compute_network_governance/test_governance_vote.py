from phase4.trusted_compute_network_governance.governance_vote import (
    GovernanceVote,
)


def test_contains_proposal_id():

    vote = GovernanceVote(
        proposal_id="proposal-001",
        tcu_did="did:tcn:test:01",
        vote="APPROVE",
    )

    assert vote.proposal_id == "proposal-001"


def test_contains_tcu_did():

    vote = GovernanceVote(
        proposal_id="proposal-001",
        tcu_did="did:tcn:test:01",
        vote="APPROVE",
    )

    assert vote.tcu_did == "did:tcn:test:01"


def test_contains_vote():

    vote = GovernanceVote(
        proposal_id="proposal-001",
        tcu_did="did:tcn:test:01",
        vote="APPROVE",
    )

    assert vote.vote == "APPROVE"


def test_serializes():

    vote = GovernanceVote(
        proposal_id="proposal-001",
        tcu_did="did:tcn:test:01",
        vote="APPROVE",
    )

    assert vote.to_dict() == {
        "proposal_id": "proposal-001",
        "tcu_did": "did:tcn:test:01",
        "vote": "APPROVE",
    }
