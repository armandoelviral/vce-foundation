from phase3.governance_recovery.recovery_registry import (
    RecoveryRegistry,
)


class RecoveryQuery:

    def __init__(
        self,
        registry: RecoveryRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        recovery_id: str,
    ):

        return self.registry.get(
            recovery_id
        )
