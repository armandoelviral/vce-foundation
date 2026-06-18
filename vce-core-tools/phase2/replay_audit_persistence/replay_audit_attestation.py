from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)


class ReplayAuditAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        replay_audit: ReplayAuditRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="replay_audit",
            evidence_hash=replay_audit.replay_id,
        )
