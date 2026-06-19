class ProofReport:

    def __init__(
        self,
        proofs,
    ):

        self.proofs = proofs

    def proof_count(
        self,
    ) -> int:

        return len(
            self.proofs
        )

    def proof_ids(
        self,
    ):

        return list(
            self.proofs.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "proof_count":
                self.proof_count(),

            "proof_ids":
                self.proof_ids(),
        }
