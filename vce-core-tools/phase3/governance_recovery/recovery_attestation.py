from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)


class RecoveryAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        recovery: RecoveryRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_recovery",
            evidence_hash=(
                recovery.recovery_id
            ),
        )
