from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)


class EscalationAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        escalation: EscalationRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_escalation",
            evidence_hash=(
                escalation.escalation_id
            ),
        )
