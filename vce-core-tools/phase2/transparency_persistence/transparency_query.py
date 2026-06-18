from phase2.transparency_persistence.transparency_log_store import (
    TransparencyLogStore,
)


class TransparencyQuery:

    def __init__(
        self,
        store: TransparencyLogStore,
    ):

        self.store = store

    def by_hash(
        self,
        entry_hash: str,
    ):

        return [
            entry
            for entry
            in self.store.all()
            if entry.entry_hash == entry_hash
        ]
