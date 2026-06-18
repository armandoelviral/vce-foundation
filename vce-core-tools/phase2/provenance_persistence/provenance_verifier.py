from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)


class ProvenanceVerifier:

    @staticmethod
    def verify(
        record: ProvenanceRecord,
        expected_hash: str,
    ) -> bool:

        if not record.provenance_hash:
            return False

        return (
            record.provenance_hash
            == expected_hash
        )
