from phase4.trusted_compute_network_governance.admission_proposal import (
    AdmissionProposal,
)


def test_contains_proposal_id():

    proposal = AdmissionProposal(
        proposal_id="proposal-001",
        candidate_did="did:tcn:new-node-01",
        sponsor_did="did:tcn:test:01",
    )

    assert proposal.proposal_id == "proposal-001"


def test_contains_candidate():

    proposal = AdmissionProposal(
        proposal_id="proposal-001",
        candidate_did="did:tcn:new-node-01",
        sponsor_did="did:tcn:test:01",
    )

    assert proposal.candidate_did == (
        "did:tcn:new-node-01"
    )


def test_contains_sponsor():

    proposal = AdmissionProposal(
        proposal_id="proposal-001",
        candidate_did="did:tcn:new-node-01",
        sponsor_did="did:tcn:test:01",
    )

    assert proposal.sponsor_did == (
        "did:tcn:test:01"
    )


def test_serializes():

    proposal = AdmissionProposal(
        proposal_id="proposal-001",
        candidate_did="did:tcn:new-node-01",
        sponsor_did="did:tcn:test:01",
    )

    assert proposal.to_dict() == {
        "proposal_id": "proposal-001",
        "candidate_did":
            "did:tcn:new-node-01",
        "sponsor_did":
            "did:tcn:test:01",
        "proposal_type":
            "ADMISSION",
    }
