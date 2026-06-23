class ReputationVerifier:

    @staticmethod
    def verify(state) -> bool:

        return state.score >= 0
