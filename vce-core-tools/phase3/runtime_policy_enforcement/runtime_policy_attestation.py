from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)


class RuntimePolicyAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        policy: RuntimePolicyRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="runtime_policy",
            evidence_hash=policy.policy_id,
        )
