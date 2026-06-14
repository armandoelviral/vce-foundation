from typing import List

from epics.ztc21_hardware_trust_anchors.hardware_trust_anchor import (
    HardwareTrustAnchor,
)


class HardwareAnchorRegistry:

    def __init__(self):

        self._anchors: List[
            HardwareTrustAnchor
        ] = []

    def add(
        self,
        anchor: HardwareTrustAnchor,
    ) -> None:

        self._anchors.append(
            anchor
        )

    def all(
        self,
    ) -> List[HardwareTrustAnchor]:

        return list(
            self._anchors
        )

    def count(
        self,
    ) -> int:

        return len(
            self._anchors
        )
