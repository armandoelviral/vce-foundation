from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)
from epics.phase5_006_reality_verification.reality_verifier import (
    verify_reality,
)


def test_verifies_single_claim():
    claim = RealityClaim(
        "claim.001",
        "obs.001",
        "package_delivered",
    )

    result = verify_reality([claim])

    assert result["verified"] is True


def test_empty_claims_not_verified():
    result = verify_reality([])

    assert result["verified"] is False


def test_reports_claim_count():
    claims = [
        RealityClaim("c1", "o1", "v1"),
        RealityClaim("c2", "o2", "v2"),
    ]

    result = verify_reality(claims)

    assert result["claim_count"] == 2
