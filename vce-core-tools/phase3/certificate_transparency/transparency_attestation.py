from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.certificate_transparency.transparency_certificate_record import (
    TransparencyCertificateRecord,
)


class TransparencyAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        entry: TransparencyCertificateRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="transparency_entry",
            evidence_hash=entry.entry_id,
        )
