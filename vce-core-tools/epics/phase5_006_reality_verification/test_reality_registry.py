from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)
from epics.phase5_006_reality_verification.reality_registry import (
    RealityRegistry,
)


def test_registry_stores_claim():
    registry = RealityRegistry()

    registry.add(
        RealityClaim(
            "claim.001",
            "obs.001",
            "package_delivered",
        )
    )

    assert len(registry.records()) == 1


def test_rejects_duplicate_claim():
    registry = RealityRegistry()

    claim = RealityClaim(
        "claim.001",
        "obs.001",
        "package_delivered",
    )

    registry.add(claim)

    try:
        registry.add(claim)
        assert False
    except ValueError:
        assert True


def test_returns_copy():
    registry = RealityRegistry()

    registry.add(
        RealityClaim(
            "claim.001",
            "obs.001",
            "package_delivered",
        )
    )

    records = registry.records()

    records.clear()

    assert len(registry.records()) == 1
