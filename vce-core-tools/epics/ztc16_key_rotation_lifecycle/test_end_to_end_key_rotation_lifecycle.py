from epics.ztc16_key_rotation_lifecycle.key_slot import (
    KeySlot,
)

from epics.ztc16_key_rotation_lifecycle.key_slot_registry import (
    KeySlotRegistry,
)

from epics.ztc16_key_rotation_lifecycle.key_rotation_record import (
    KeyRotationRecord,
)

from epics.ztc16_key_rotation_lifecycle.activation_anchor import (
    ActivationAnchor,
)

from epics.ztc16_key_rotation_lifecycle.key_validity_window import (
    KeyValidityWindow,
)

from epics.ztc16_key_rotation_lifecycle.key_history_registry import (
    KeyHistoryRegistry,
)

from epics.ztc16_key_rotation_lifecycle.historical_key_resolver import (
    HistoricalKeyResolver,
)


def test_end_to_end_key_rotation_lifecycle():

    registry = KeySlotRegistry()

    active_slot = KeySlot(
        name="ACTIVE",
        key_id="key-001",
    )

    next_slot = KeySlot(
        name="NEXT",
        key_id="key-002",
    )

    registry.add(active_slot)
    registry.add(next_slot)

    rotation = KeyRotationRecord(
        witness_id="witness-001",
        old_key_id="key-001",
        new_key_id="key-002",
        reason="scheduled_rotation",
    )

    anchor = ActivationAnchor(
        anchor_id="anchor-200",
        rotation_id="rotation-001",
    )

    history = KeyHistoryRegistry()

    history.add(
        KeyValidityWindow(
            key_id="key-001",
            start_anchor="anchor-100",
            end_anchor="anchor-199",
        )
    )

    history.add(
        KeyValidityWindow(
            key_id="key-002",
            start_anchor="anchor-200",
            end_anchor="anchor-300",
        )
    )

    resolver = HistoricalKeyResolver(
        history
    )

    assert (
        resolver.resolve("anchor-150")
        == "key-001"
    )

    assert (
        resolver.resolve("anchor-250")
        == "key-002"
    )

    assert rotation.old_key_id == "key-001"
    assert rotation.new_key_id == "key-002"

    assert anchor.anchor_id == "anchor-200"
