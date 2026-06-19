class EscalationReport:

    def __init__(
        self,
        escalations,
    ):

        self.escalations = escalations

    def escalation_count(
        self,
    ) -> int:

        return len(
            self.escalations
        )

    def escalation_ids(
        self,
    ):

        return list(
            self.escalations.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "escalation_count":
                self.escalation_count(),
            "escalation_ids":
                self.escalation_ids(),
        }
