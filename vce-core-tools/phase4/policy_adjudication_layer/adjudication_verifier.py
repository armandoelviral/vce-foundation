class AdjudicationVerifier:

    @staticmethod
    def verify(
        state,
    ) -> bool:

        return (
            state.adjudication_state
            == "RESOLVED"
        )

