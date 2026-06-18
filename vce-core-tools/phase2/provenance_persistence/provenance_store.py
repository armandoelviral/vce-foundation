from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)


class ProvenanceStore:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: ProvenanceRecord,
    ) -> None:

        self._records[
            record.subject_id
        ] = record

    def get(
        self,
        subject_id: str,
    ):

        return self._records.get(
            subject_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )
