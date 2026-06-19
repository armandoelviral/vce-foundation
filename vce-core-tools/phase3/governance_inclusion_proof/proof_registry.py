from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)


class ProofRegistry:

    def __init__(self):

        self._proofs = {}

    def add(
        self,
        proof_id: str,
        proof: InclusionProofRecord,
    ) -> None:

        self._proofs[
            proof_id
        ] = proof

    def get(
        self,
        proof_id: str,
    ):

        return self._proofs.get(
            proof_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._proofs
        )

    def proof_ids(
        self,
    ):

        return list(
            self._proofs.keys()
        )
