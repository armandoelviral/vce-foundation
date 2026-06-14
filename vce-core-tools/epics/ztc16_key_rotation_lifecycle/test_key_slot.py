from epics.ztc16_key_rotation_lifecycle.key_slot import (
    KeySlot,
)


def test_key_slot_contains_name():

    slot = KeySlot(
        name="ACTIVE",
        key_id="key-001",
    )

    assert slot.name == "ACTIVE"


def test_key_slot_contains_key_id():

    slot = KeySlot(
        name="ACTIVE",
        key_id="key-001",
    )

    assert slot.key_id == "key-001"


def test_key_slot_serializes():

    slot = KeySlot(
        name="ACTIVE",
        key_id="key-001",
    )

    assert slot.to_dict() == {
        "name": "ACTIVE",
        "key_id": "key-001",
    }
