class TrustedExecutionGate:

    @staticmethod
    def admit(
        attestation: dict,
    ) -> bool:

        required_fields = [
            "artifact_hash",
            "execution_id",
            "result_hash",
            "binding_hash",
        ]

        return all(
            field in attestation
            and attestation[field]
            for field in required_fields
        )
