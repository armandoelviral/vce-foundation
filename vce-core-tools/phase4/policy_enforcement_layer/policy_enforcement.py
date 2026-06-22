class PolicyEnforcement:

    @staticmethod
    def enforce(
        policy,
    ) -> bool:

        return policy.active is True
