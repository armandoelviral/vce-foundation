from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)


class PolicyStore:

    def __init__(
        self,
    ):

        self._records = {}

    def add(
        self,
        record: PolicyRecord,
    ) -> None:

        key = (
            record.policy_id,
            record.version,
        )

        self._records[key] = record

    def get(
        self,
        policy_id: str,
        version: int,
    ):

        return self._records.get(
            (
                policy_id,
                version,
            )
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )

    def all(self):

        return list(
            self._records.values()
        )
