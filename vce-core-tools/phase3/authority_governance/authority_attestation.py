from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)


class AuthorityAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        authority: AuthorityRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="authority_record",
            evidence_hash=(
                authority.authority_id
            ),
        )
