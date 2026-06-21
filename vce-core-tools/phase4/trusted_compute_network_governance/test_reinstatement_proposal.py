from phase4.trusted_compute_network_governance.reinstatement_proposal import (
    ReinstatementProposal,
)


def test_contains_target():

    proposal = ReinstatementProposal(
        proposal_id="proposal-003",
        target_did="did:tcn:test:02",
        sponsor_did="did:tcn:test:01",
        evidence="response_capability_restored",
    )

    assert proposal.target_did == (
        "did:tcn:test:02"
    )


def test_contains_evidence():

    proposal = ReinstatementProposal(
        proposal_id="proposal-003",
        target_did="did:tcn:test:02",
        sponsor_did="did:tcn:test:01",
        evidence="response_capability_restored",
    )

    assert proposal.evidence == (
        "response_capability_restored"
    )


def test_serializes():

    proposal = ReinstatementProposal(
        proposal_id="proposal-003",
        target_did="did:tcn:test:02",
        sponsor_did="did:tcn:test:01",
        evidence="response_capability_restored",
    )

    assert proposal.to_dict() == {
        "proposal_id": "proposal-003",
        "target_did": "did:tcn:test:02",
        "sponsor_did": "did:tcn:test:01",
        "evidence":
            "response_capability_restored",
        "proposal_type":
            "REINSTATEMENT",
    }
