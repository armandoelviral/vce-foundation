from typing import Optional

from epics.ztc16_key_rotation_lifecycle.key_slot import (
    KeySlot,
)


class KeySlotRegistry:

    def __init__(self):

        self._slots = {}

    def add(
        self,
        slot: KeySlot,
    ) -> None:

        self._slots[slot.name] = slot

    def exists(
        self,
        slot_name: str,
    ) -> bool:

        return slot_name in self._slots

    def get(
        self,
        slot_name: str,
    ) -> Optional[KeySlot]:

        return self._slots.get(slot_name)
