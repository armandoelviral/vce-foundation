class ConstitutionalVerifier:

    @staticmethod
    def verify(state) -> bool:

        return state.constitutional_state in (
            "ACTIVE",
            "UPHELD",
        )
