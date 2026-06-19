from phase3.witness_did_identity.did_registry import (
    DidRegistry,
)


class DidResolver:

    def __init__(
        self,
        registry: DidRegistry,
    ):

        self.registry = registry

    def resolve(
        self,
        did: str,
    ):

        return self.registry.get(
            did
        )
