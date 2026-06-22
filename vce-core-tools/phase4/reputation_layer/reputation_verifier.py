class ReputationVerifier:

    @staticmethod
    def verify(
        state,
    ) -> bool:

        return (
            state.reputation_state
            in (
                "TRUSTED",
                "RECOVERING",
            )
        )
