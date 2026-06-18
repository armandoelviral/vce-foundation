class ReplayAuditReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def total_audits(
        self,
    ) -> int:

        return len(
            self.records
        )

    def replay_ids(
        self,
    ):

        return [
            record.replay_id
            for record in self.records
        ]

    def to_dict(
        self,
    ):

        return {
            "total_audits":
                self.total_audits(),
            "replay_ids":
                self.replay_ids(),
        }
