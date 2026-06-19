from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)


class ProofEvaluation:

    @staticmethod
    def evaluate(
        proof: InclusionProofRecord,
    ) -> bool:

        if not proof.leaf_id:
            return False

        if not proof.root_id:
            return False

        if not proof.proof_hash:
            return False

        return True
