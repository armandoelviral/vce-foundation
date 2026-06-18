class PolicyReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def total_policies(
        self,
    ) -> int:

        return len(
            self.records
        )

    def policy_ids(
        self,
    ):

        return [
            record.policy_id
            for record in self.records
        ]

    def to_dict(
        self,
    ):

        return {
            "total_policies":
                self.total_policies(),
            "policy_ids":
                self.policy_ids(),
        }
