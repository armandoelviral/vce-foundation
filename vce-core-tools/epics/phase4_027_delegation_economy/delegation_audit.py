from epics.phase4_027_delegation_economy.delegation_registry import (
    DelegationRegistry,
)
from epics.phase4_027_delegation_economy.delegation_revocation import (
    DelegationRevocationRecord,
)


def audit_active_delegations(
    registry: DelegationRegistry,
    revocations: list[DelegationRevocationRecord],
) -> dict:

    revoked_ids = {
        revocation.delegation_id
        for revocation in revocations
    }

    active = [
        record
        for record in registry.records()
        if record.delegation_id not in revoked_ids
    ]

    return {
        "active_count": len(active),
        "active_delegations": active,
    }
