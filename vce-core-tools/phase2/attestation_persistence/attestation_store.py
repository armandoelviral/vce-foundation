from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)


class AttestationStore:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: AttestationRecord,
    ) -> None:

        self._records[record.attestation_id] = record

    def get(
        self,
        attestation_id: str,
    ):

        return self._records.get(attestation_id)

    def all(self):

        return list(self._records.values())

    def count(self) -> int:

        return len(self._records)
