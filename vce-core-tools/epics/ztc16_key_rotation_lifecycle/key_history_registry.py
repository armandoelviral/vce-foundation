from typing import List

from epics.ztc16_key_rotation_lifecycle.key_validity_window import (
    KeyValidityWindow,
)


class KeyHistoryRegistry:

    def __init__(self):

        self._windows: List[
            KeyValidityWindow
        ] = []

    def add(
        self,
        window: KeyValidityWindow,
    ) -> None:

        self._windows.append(
            window
        )

    def all(
        self,
    ) -> List[KeyValidityWindow]:

        return list(
            self._windows
        )

    def count(
        self,
    ) -> int:

        return len(
            self._windows
        )
