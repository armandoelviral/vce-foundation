from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)


class ConsensusAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        consensus: ConsensusRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_consensus",
            evidence_hash=consensus.consensus_id,
        )
