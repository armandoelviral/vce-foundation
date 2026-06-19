class ProvenanceReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def record_count(
        self,
    ) -> int:

        return len(
            self.records
        )

    def provenance_ids(
        self,
    ):

        return list(
            self.records.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "record_count":
                self.record_count(),

            "provenance_ids":
                self.provenance_ids(),
        }
