class ProvenanceReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def total_records(
        self,
    ) -> int:

        return len(
            self.records
        )

    def subject_ids(
        self,
    ):

        return [
            record.subject_id
            for record in self.records
        ]

    def to_dict(
        self,
    ):

        return {
            "total_records":
                self.total_records(),
            "subject_ids":
                self.subject_ids(),
        }
