class SP1ProverAdapter:

    def prover_type(
        self,
    ) -> str:

        return "SP1"

    def generate_proof(
        self,
        execution_request_id: str,
    ):

        return {
            "execution_request_id":
                execution_request_id,

            "prover_type":
                "SP1",

            "status":
                "PROOF_GENERATED",

            "proof_hash":
                f"sp1-proof-{execution_request_id}",
        }
