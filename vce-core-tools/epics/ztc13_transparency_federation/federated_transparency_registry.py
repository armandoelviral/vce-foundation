from typing import Iterable

from epics.ztc13_transparency_federation.transparency_registry import (
    TransparencyRegistry,
)


class FederatedTransparencyRegistry:

    def __init__(
        self,
        registries: Iterable[
            TransparencyRegistry
        ],
    ):

        self._registries = list(
            registries
        )

    def exists(
        self,
        anchor_id: str,
    ) -> bool:

        return any(
            registry.exists(anchor_id)
            for registry in self._registries
        )
