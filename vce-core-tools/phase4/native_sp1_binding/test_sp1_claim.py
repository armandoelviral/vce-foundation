from phase4.native_sp1_binding.sp1_claim import (
    SP1Claim,
)


def test_contains_claim_id():

    claim = SP1Claim(
        claim_id="claim-001",
        citizen_did="did:tcn:test:01",
        statement="fibonacci(1)=(1,1)",
        proof_digest="proof-001",
    )

    assert claim.claim_id == "claim-001"


def test_contains_citizen():

    claim = SP1Claim(
        claim_id="claim-001",
        citizen_did="did:tcn:test:01",
        statement="fibonacci(1)=(1,1)",
        proof_digest="proof-001",
    )

    assert claim.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_statement():

    claim = SP1Claim(
        claim_id="claim-001",
        citizen_did="did:tcn:test:01",
        statement="fibonacci(1)=(1,1)",
        proof_digest="proof-001",
    )

    assert claim.statement == (
        "fibonacci(1)=(1,1)"
    )


def test_serializes():

    claim = SP1Claim(
        claim_id="claim-001",
        citizen_did="did:tcn:test:01",
        statement="fibonacci(1)=(1,1)",
        proof_digest="proof-001",
    )

    assert claim.to_dict() == {
        "claim_id": "claim-001",
        "citizen_did": "did:tcn:test:01",
        "statement": "fibonacci(1)=(1,1)",
        "proof_digest": "proof-001",
    }
