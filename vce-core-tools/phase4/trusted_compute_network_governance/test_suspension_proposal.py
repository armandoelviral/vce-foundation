from phase4.trusted_compute_network_governance.suspension_proposal import (
    SuspensionProposal,
)


def test_contains_target():

    proposal = SuspensionProposal(
        proposal_id="proposal-002",
        target_did="did:tcn:test:02",
        sponsor_did="did:tcn:test:01",
        reason="response_invalidity",
    )

    assert proposal.target_did == (
        "did:tcn:test:02"
    )


def test_contains_reason():

    proposal = SuspensionProposal(
        proposal_id="proposal-002",
        target_did="did:tcn:test:02",
        sponsor_did="did:tcn:test:01",
        reason="response_invalidity",
    )

    assert proposal.reason == (
        "response_invalidity"
    )


def test_serializes():

    proposal = SuspensionProposal(
        proposal_id="proposal-002",
        target_did="did:tcn:test:02",
        sponsor_did="did:tcn:test:01",
        reason="response_invalidity",
    )

    assert proposal.to_dict() == {
        "proposal_id": "proposal-002",
        "target_did": "did:tcn:test:02",
        "sponsor_did": "did:tcn:test:01",
        "reason": "response_invalidity",
        "proposal_type": "SUSPENSION",
    }
