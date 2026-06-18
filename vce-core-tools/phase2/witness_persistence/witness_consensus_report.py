class WitnessConsensusReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def total_decisions(
        self,
    ) -> int:

        return len(
            self.records
        )

    def decision_ids(
        self,
    ):

        return [
            record.decision_id
            for record in self.records
        ]

    def to_dict(
        self,
    ):

        return {
            "total_decisions":
                self.total_decisions(),
            "decision_ids":
                self.decision_ids(),
        }
