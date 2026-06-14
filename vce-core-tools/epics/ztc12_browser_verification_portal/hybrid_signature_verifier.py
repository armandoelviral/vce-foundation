class HybridSignatureVerifier:

    @staticmethod
    def verify(
        classical_valid: bool,
        pqc_valid: bool,
    ) -> bool:

        return (
            classical_valid
            and pqc_valid
        )
