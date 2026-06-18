from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)


class AttestationVerifier:

    @staticmethod
    def verify(
        record: AttestationRecord,
        expected_hash: str,
    ) -> bool:

        if not record.evidence_hash:
            return False

        return (
            record.evidence_hash
            == expected_hash
        )
