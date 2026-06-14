from typing import Optional

from epics.ztc13_transparency_federation.transparency_anchor import (
    TransparencyAnchor,
)


class TransparencyRegistry:

    def __init__(self):

        self._anchors = {}

    def add(
        self,
        anchor: TransparencyAnchor,
    ) -> None:

        self._anchors[anchor.anchor_id] = anchor

    def exists(
        self,
        anchor_id: str,
    ) -> bool:

        return anchor_id in self._anchors

    def get(
        self,
        anchor_id: str,
    ) -> Optional[TransparencyAnchor]:

        return self._anchors.get(anchor_id)
