from phase4.native_sp1_binding.sp1_proof_digest_binding import (
    SP1ProofDigestBinding,
)


def test_contains_did():

    binding = SP1ProofDigestBinding(
        tcu_did="did:tcn:test:01",
        proof_digest="proof-digest-001",
    )

    assert binding.tcu_did == "did:tcn:test:01"


def test_contains_proof_digest():

    binding = SP1ProofDigestBinding(
        tcu_did="did:tcn:test:01",
        proof_digest="proof-digest-001",
    )

    assert binding.proof_digest == "proof-digest-001"


def test_serializes():

    binding = SP1ProofDigestBinding(
        tcu_did="did:tcn:test:01",
        proof_digest="proof-digest-001",
    )

    assert binding.to_dict() == {
        "tcu_did": "did:tcn:test:01",
        "proof_digest": "proof-digest-001",
    }
