from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)
from epics.phase5_006_reality_verification.reality_state import (
    RealityState,
)


def test_builds_state():
    state = RealityState.from_records(
        [
            RealityClaim(
                "claim.001",
                "obs.001",
                "package_delivered",
            )
        ]
    )

    assert state.total_claims == 1


def test_empty_state():
    state = RealityState.from_records([])

    assert state.total_claims == 0
