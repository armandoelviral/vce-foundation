from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)
from epics.phase5_006_reality_verification.reality_registry import (
    RealityRegistry,
)
from epics.phase5_006_reality_verification.reality_verifier import (
    verify_reality,
)


def test_end_to_end_reality_flow():
    registry = RealityRegistry()

    registry.add(
        RealityClaim(
            claim_id="claim.001",
            observation_id="obs.001",
            claim_value="package_delivered",
        )
    )

    result = verify_reality(
        registry.records()
    )

    assert result["verified"] is True
    assert result["claim_count"] == 1
