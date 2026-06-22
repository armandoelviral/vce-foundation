class RightsVerifier:

    @staticmethod
    def verify(state) -> bool:

        return state.rights_state in (
            "PROTECTED",
            "RESTORED",
        )
