from epics.phase4_027_delegation_economy.delegation_record import (
    DelegationRecord,
)


class DelegationRegistry:
    def __init__(self):
        self._records: list[DelegationRecord] = []
        self._delegation_ids: set[str] = set()

    def add(
        self,
        record: DelegationRecord,
    ) -> None:

        if record.delegation_id in self._delegation_ids:
            raise ValueError("duplicate delegation")

        self._records.append(record)
        self._delegation_ids.add(record.delegation_id)

    def records(self) -> list[DelegationRecord]:
        return list(self._records)

    def by_delegator(
        self,
        delegator_id: str,
    ) -> list[DelegationRecord]:

        return [
            record
            for record in self._records
            if record.delegator_id == delegator_id
        ]
