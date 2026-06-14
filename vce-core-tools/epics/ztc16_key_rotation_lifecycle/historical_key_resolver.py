from typing import Optional

from epics.ztc16_key_rotation_lifecycle.key_history_registry import (
    KeyHistoryRegistry,
)


class HistoricalKeyResolver:

    def __init__(
        self,
        registry: KeyHistoryRegistry,
    ):

        self._registry = registry

    def resolve(
        self,
        anchor_id: str,
    ) -> Optional[str]:

        anchor_value = int(
            anchor_id.split("-")[1]
        )

        for window in self._registry.all():

            start_value = int(
                window.start_anchor.split("-")[1]
            )

            end_value = int(
                window.end_anchor.split("-")[1]
            )

            if (
                start_value
                <= anchor_value
                <= end_value
            ):
                return window.key_id

        return None
