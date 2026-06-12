from epics.epic082_external_ledger_root_anchoring.anchor_target_registry import (
    AnchorTarget,
    AnchorTargetRegistry,
)


def build_registry():

    registry = AnchorTargetRegistry()

    registry.register(
        AnchorTarget(
            target_id="rekor",
            target_type="TRANSPARENCY_LOG",
            active=True,
        )
    )

    registry.register(
        AnchorTarget(
            target_id="private-log",
            target_type="PRIVATE_TRANSPARENCY_LOG",
            active=False,
        )
    )

    return registry


def test_registry_registers_target():

    registry = build_registry()

    target = registry.get(
        "rekor"
    )

    assert target is not None


def test_registry_returns_target_metadata():

    registry = build_registry()

    target = registry.get(
        "rekor"
    )

    assert (
        target.target_type
        == "TRANSPARENCY_LOG"
    )


def test_registry_returns_active_targets_only():

    registry = build_registry()

    active_targets = (
        registry.active_targets()
    )

    assert len(
        active_targets
    ) == 1

    assert (
        active_targets[0].target_id
        == "rekor"
    )


def test_registry_returns_inactive_target():

    registry = build_registry()

    target = registry.get(
        "private-log"
    )

    assert target.active is False
