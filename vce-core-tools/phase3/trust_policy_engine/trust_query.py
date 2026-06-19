class TrustQuery:

    def __init__(
        self,
        decisions,
    ):

        self.decisions = decisions

    def by_id(
        self,
        decision_id: str,
    ):

        return self.decisions.get(
            decision_id
        )
