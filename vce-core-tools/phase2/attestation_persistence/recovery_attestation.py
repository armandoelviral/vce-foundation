from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.runtime_state_recovery.recovery_report import (
    RecoveryReport,
)


class RecoveryAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        report: RecoveryReport,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="recovery",
            evidence_hash=report.recovery_id,
        )
