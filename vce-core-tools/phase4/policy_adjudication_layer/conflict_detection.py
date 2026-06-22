class ConflictDetection:

    @staticmethod
    def detect(
        policy_a: str,
        policy_b: str,
    ):

        return {
            "policy_a": policy_a,
            "policy_b": policy_b,
            "conflict": policy_a != policy_b,
        }
