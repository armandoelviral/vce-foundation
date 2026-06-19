class ConsensusReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def consensus_count(
        self,
    ) -> int:

        return len(
            self.records
        )

    def consensus_ids(
        self,
    ):

        return list(
            self.records.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "consensus_count":
                self.consensus_count(),

            "consensus_ids":
                self.consensus_ids(),
        }
