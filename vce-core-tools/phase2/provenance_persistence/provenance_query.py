from phase2.provenance_persistence.provenance_store import (
    ProvenanceStore,
)


class ProvenanceQuery:

    def __init__(
        self,
        store: ProvenanceStore,
    ):

        self.store = store

    def by_subject(
        self,
        subject_id: str,
    ):

        return self.store.get(
            subject_id
        )
