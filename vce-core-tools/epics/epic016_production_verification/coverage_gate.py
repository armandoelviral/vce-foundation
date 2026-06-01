class CoverageGate:

    def __init__(
        self,
        minimum=90
    ):

        self.minimum = minimum


    def validate(
        self,
        coverage_percent
    ):

        if coverage_percent < self.minimum:

            return {
                "passed": False,
                "required": self.minimum,
                "actual": coverage_percent
            }


        return {
            "passed": True,
            "required": self.minimum,
            "actual": coverage_percent
        }
