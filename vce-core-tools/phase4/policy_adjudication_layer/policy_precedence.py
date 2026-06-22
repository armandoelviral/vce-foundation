class PolicyPrecedence:

    @staticmethod
    def resolve(
        higher_priority: str,
        lower_priority: str,
    ):

        return {
            "winning_policy":
                higher_priority,
            "losing_policy":
                lower_priority,
        }
