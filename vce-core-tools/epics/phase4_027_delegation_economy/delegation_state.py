from dataclasses import dataclass

from epics.phase4_027_delegation_economy.delegation_registry import (
    DelegationRegistry,
)
from epics.phase4_027_delegation_economy.delegation_revocation import (
    DelegationRevocationRecord,
)


@dataclass(frozen=True)
class DelegationState:
    delegator_id: str
    active_delegations: int
    total_delegated_capacity: int

    @classmethod
    def from_records(
        cls,
        registry: DelegationRegistry,
        revocations: list[DelegationRevocationRecord],
        delegator_id: str,
    ):
        revoked_ids = {
            revocation.delegation_id
            for revocation in revocations
        }

        active = [
            record
            for record in registry.by_delegator(delegator_id)
            if record.delegation_id not in revoked_ids
        ]

        return cls(
            delegator_id=delegator_id,
            active_delegations=len(active),
            total_delegated_capacity=sum(
                record.delegated_capacity
                for record in active
            ),
        )
