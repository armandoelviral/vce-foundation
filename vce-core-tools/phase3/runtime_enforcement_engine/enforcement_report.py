class EnforcementReport:

    def __init__(
        self,
        decisions,
    ):

        self.decisions = decisions

    def decision_count(
        self,
    ) -> int:

        return len(
            self.decisions
        )

    def decision_ids(
        self,
    ):

        return list(
            self.decisions.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "decision_count":
                self.decision_count(),
            "decision_ids":
                self.decision_ids(),
        }
