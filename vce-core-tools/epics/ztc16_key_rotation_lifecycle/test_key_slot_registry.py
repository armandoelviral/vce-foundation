from epics.ztc16_key_rotation_lifecycle.key_slot import (
    KeySlot,
)

from epics.ztc16_key_rotation_lifecycle.key_slot_registry import (
    KeySlotRegistry,
)


def test_registry_stores_slot():

    registry = KeySlotRegistry()

    slot = KeySlot(
        name="ACTIVE",
        key_id="key-001",
    )

    registry.add(slot)

    assert registry.exists("ACTIVE")


def test_registry_returns_slot():

    registry = KeySlotRegistry()

    slot = KeySlot(
        name="ACTIVE",
        key_id="key-001",
    )

    registry.add(slot)

    stored = registry.get("ACTIVE")

    assert stored.key_id == "key-001"


def test_registry_returns_none_for_unknown_slot():

    registry = KeySlotRegistry()

    assert registry.get("missing") is None
