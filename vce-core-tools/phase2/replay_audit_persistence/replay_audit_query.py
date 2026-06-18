from phase2.replay_audit_persistence.replay_audit_store import (
    ReplayAuditStore,
)


class ReplayAuditQuery:

    def __init__(
        self,
        store: ReplayAuditStore,
    ):

        self.store = store

    def by_replay_id(
        self,
        replay_id: str,
    ):

        return self.store.get(
            replay_id
        )
