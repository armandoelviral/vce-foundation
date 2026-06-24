from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)


def verify_reality(
    claims: list[RealityClaim],
):
    return {
        "verified": len(claims) > 0,
        "claim_count": len(claims),
    }
