from phase2.policy_persistence.policy_store import (
    PolicyStore,
)


class PolicyQuery:

    def __init__(
        self,
        store: PolicyStore,
    ):

        self.store = store

    def by_id(
        self,
        policy_id: str,
        version: int,
    ):

        return self.store.get(
            policy_id,
            version,
        )
