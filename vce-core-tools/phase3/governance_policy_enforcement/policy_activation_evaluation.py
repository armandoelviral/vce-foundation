class PolicyActivationEvaluation:

    @staticmethod
    def evaluate(
        consensus_outcome: str,
    ) -> bool:

        return (
            consensus_outcome
            == "APPROVED"
        )
