from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)


class CertificateAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        certificate: ReplayCertificateRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="replay_certificate",
            evidence_hash=certificate.certificate_id,
        )
