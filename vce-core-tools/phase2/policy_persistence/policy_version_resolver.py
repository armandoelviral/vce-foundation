from phase2.policy_persistence.policy_store import (
    PolicyStore,
)


class PolicyVersionResolver:

    def __init__(
        self,
        store: PolicyStore,
    ):

        self.store = store

    def latest(
        self,
        policy_id: str,
    ):

        candidates = [
            record
            for record
            in self.store.all()
            if record.policy_id == policy_id
        ]

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda r: r.version,
        )
