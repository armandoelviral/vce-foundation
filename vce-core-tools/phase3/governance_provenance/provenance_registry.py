from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)


class ProvenanceRegistry:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: GovernanceProvenanceRecord,
    ) -> None:

        self._records[
            record.provenance_id
        ] = record

    def get(
        self,
        provenance_id: str,
    ):

        return self._records.get(
            provenance_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )

    def provenance_ids(
        self,
    ):

        return list(
            self._records.keys()
        )
