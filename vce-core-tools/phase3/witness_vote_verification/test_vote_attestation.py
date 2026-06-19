from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)

from phase3.witness_vote_verification.vote_attestation import (
    VoteAttestation,
)


def test_attestation_subject():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    attestation = VoteAttestation.attest(
        attestation_id="att-001",
        vote=vote,
    )

    assert attestation.subject == "witness_vote"


def test_attestation_uses_vote_id():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    attestation = VoteAttestation.attest(
        attestation_id="att-001",
        vote=vote,
    )

    assert attestation.evidence_hash == "vote-001"


def test_attestation_preserves_id():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    attestation = VoteAttestation.attest(
        attestation_id="att-001",
        vote=vote,
    )

    assert attestation.attestation_id == "att-001"
