class GovernanceVerifier:

    @staticmethod
    def verify(state) -> bool:

        return state.governance_state in (
            "STABLE",
            "UPDATED",
        )
