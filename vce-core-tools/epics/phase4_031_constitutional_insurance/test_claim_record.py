from epics.phase4_031_constitutional_insurance.claim_record import (
    ClaimRecord,
)


def test_claim_creation():
    claim = ClaimRecord(
        claim_id="claim.001",
        policy_id="policy.001",
        claim_amount=50,
        reason="credit default",
    )

    assert claim.claim_id == "claim.001"
    assert claim.policy_id == "policy.001"
    assert claim.claim_amount == 50
    assert claim.reason == "credit default"


def test_rejects_empty_claim_id():
    try:
        ClaimRecord(
            claim_id="",
            policy_id="policy.001",
            claim_amount=50,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "claim_id" in str(exc)


def test_rejects_non_positive_claim_amount():
    try:
        ClaimRecord(
            claim_id="claim.001",
            policy_id="policy.001",
            claim_amount=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "claim_amount" in str(exc)
