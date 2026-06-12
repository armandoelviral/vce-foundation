class CPSThresholdRule:

    def is_satisfied(
        self,
        artifact_cps: int,
        required_cps: int,
    ):

        return (
            artifact_cps
            >=
            required_cps
        )
