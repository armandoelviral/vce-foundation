from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)


def test_reality_claim_creation():
    claim = RealityClaim(
        claim_id="claim.001",
        observation_id="obs.001",
        claim_value="package_delivered",
    )

    assert claim.claim_id == "claim.001"


def test_rejects_empty_claim_id():
    try:
        RealityClaim("", "obs.001", "value")
        assert False
    except ValueError as exc:
        assert "claim_id" in str(exc)


def test_rejects_empty_claim_value():
    try:
        RealityClaim("claim.001", "obs.001", "")
        assert False
    except ValueError as exc:
        assert "claim_value" in str(exc)
