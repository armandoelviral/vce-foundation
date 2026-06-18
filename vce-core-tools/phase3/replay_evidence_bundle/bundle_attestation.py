from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


class BundleAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        bundle: ReplayEvidenceBundle,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="replay_bundle",
            evidence_hash=str(
                bundle.count()
            ),
        )
