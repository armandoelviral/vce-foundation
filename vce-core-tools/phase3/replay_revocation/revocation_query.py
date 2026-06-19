from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)


class RevocationQuery:

    def __init__(
        self,
        registry: RevocationRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        revocation_id: str,
    ):

        return self.registry.get(
            revocation_id
        )
