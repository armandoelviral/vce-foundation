class AttestationReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def total_attestations(
        self,
    ) -> int:

        return len(
            self.records
        )

    def subjects(
        self,
    ):

        return [
            record.subject
            for record in self.records
        ]

    def to_dict(
        self,
    ):

        return {
            "total_attestations":
                self.total_attestations(),
            "subjects":
                self.subjects(),
        }
