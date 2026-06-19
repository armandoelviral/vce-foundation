from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)


class PolicyVersionAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        policy_version: PolicyVersionRecord,
    ) -> AttestationRecord:

        version_id = (
            f"{policy_version.policy_id}:"
            f"{policy_version.version}"
        )

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="policy_version",
            evidence_hash=version_id,
        )
