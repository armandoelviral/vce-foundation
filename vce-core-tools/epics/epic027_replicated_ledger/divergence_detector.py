class DivergenceDetector:

    def evaluate(
        self,
        verification_result
    ):

        if verification_result[
            "replicated"
        ]:

            return {
                "status": "HEALTHY",
                "recovery": None
            }

        return {
            "status": "DIVERGED",
            "recovery":
                "CATCH_UP_REQUIRED"
        }
