from dataclasses import dataclass

from epics.phase9_005_constitutional_delegation.delegation_record import (
    DelegationRecord,
)


@dataclass(frozen=True)
class DelegationState:
    total_delegations: int
    unique_assignees: int

    @classmethod
    def from_records(
        cls,
        records: list[DelegationRecord],
    ):
        return cls(
            total_delegations=len(records),
            unique_assignees=len(
                {
                    record.assignee
                    for record in records
                }
            ),
        )
