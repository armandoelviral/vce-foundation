from phase3.replay_revocation.revocation_registry import (
    RevocationRegistry,
)


class RevocationReport:

    def __init__(
        self,
        registry: RevocationRegistry,
    ):

        self.registry = registry

    def revocation_count(
        self,
    ) -> int:

        return self.registry.count()

    def revocation_ids(
        self,
    ):

        return [
            revocation.revocation_id
            for revocation in self.registry.revocations()
        ]

    def to_dict(
        self,
    ):

        return {
            "revocation_count":
                self.revocation_count(),
            "revocation_ids":
                self.revocation_ids(),
        }
