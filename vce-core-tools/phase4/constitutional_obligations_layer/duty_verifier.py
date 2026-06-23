class DutyVerifier:

    @staticmethod
    def verify(state) -> bool:

        return state.duty_state in (
            "COMPLIANT",
            "RESTORED",
        )
