class RuntimePolicyReport:

    def __init__(
        self,
        policies,
    ):

        self.policies = policies

    def policy_count(
        self,
    ) -> int:

        return len(
            self.policies
        )

    def policy_ids(
        self,
    ):

        return list(
            self.policies.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "policy_count":
                self.policy_count(),

            "policy_ids":
                self.policy_ids(),
        }
