from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)


class PolicyActivationAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        activation: PolicyActivationRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="policy_activation",
            evidence_hash=(
                activation.activation_id
            ),
        )
