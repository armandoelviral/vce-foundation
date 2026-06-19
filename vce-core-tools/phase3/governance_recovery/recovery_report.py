class RecoveryReport:

    def __init__(
        self,
        recoveries,
    ):

        self.recoveries = recoveries

    def recovery_count(
        self,
    ) -> int:

        return len(
            self.recoveries
        )

    def recovery_ids(
        self,
    ):

        return list(
            self.recoveries.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "recovery_count":
                self.recovery_count(),
            "recovery_ids":
                self.recovery_ids(),
        }
