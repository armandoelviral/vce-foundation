class ConstitutionVerifier:

    @staticmethod
    def verify(state) -> bool:

        return state.constitution_state in (
            "ACTIVE",
            "AMENDED",
        )
