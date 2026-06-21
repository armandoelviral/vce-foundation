class RiscZeroProverAdapter:

    def prover_type(
        self,
    ) -> str:

        return "RISC_ZERO"

    def generate_proof(
        self,
        execution_request_id: str,
    ):

        return {
            "execution_request_id":
                execution_request_id,

            "prover_type":
                "RISC_ZERO",

            "status":
                "PROOF_GENERATED",

            "proof_hash":
                f"risc-zero-proof-{execution_request_id}",
        }
