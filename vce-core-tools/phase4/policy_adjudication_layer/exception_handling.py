class ExceptionHandling:

    @staticmethod
    def evaluate(
        policy_id: str,
        exception_requested: bool,
    ):

        return {
            "policy_id":
                policy_id,
            "exception_granted":
                exception_requested,
        }
