from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)


class RevocationAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        revocation: ReplayRevocationRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="replay_revocation",
            evidence_hash=revocation.revocation_id,
        )
