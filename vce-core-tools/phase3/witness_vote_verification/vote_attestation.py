from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)


class VoteAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        vote: WitnessVoteRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="witness_vote",
            evidence_hash=vote.vote_id,
        )
