class PolicyVerifier:

    @staticmethod
    def verify(
        state,
    ) -> bool:

        return (
            state.policy_state
            in (
                "ACTIVE",
                "ENFORCED",
            )
        )
