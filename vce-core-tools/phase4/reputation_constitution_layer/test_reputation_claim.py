from phase4.reputation_constitution_layer.reputation_claim import (
    ReputationClaim,
)


def test_contains_identity_id():
    claim = ReputationClaim(
        identity_id="identity-001",
        claim_type="duty_compliance",
    )

    assert claim.identity_id == "identity-001"


def test_contains_claim_type():
    claim = ReputationClaim(
        identity_id="identity-001",
        claim_type="duty_compliance",
    )

    assert claim.claim_type == "duty_compliance"


def test_serializes():
    claim = ReputationClaim(
        identity_id="identity-001",
        claim_type="duty_compliance",
    )

    assert claim.to_dict() == {
        "identity_id": "identity-001",
        "claim_type": "duty_compliance",
    }
