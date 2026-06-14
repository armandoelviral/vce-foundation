from epics.ztc19_governance_ledger.governance_event import (
    GovernanceEvent,
)

from epics.ztc19_governance_ledger.governance_admission_policy import (
    GovernanceAdmissionPolicy,
)

from epics.ztc19_governance_ledger.governance_ledger_entry import (
    GovernanceLedgerEntry,
)

from epics.ztc19_governance_ledger.governance_ledger import (
    GovernanceLedger,
)

from epics.ztc19_governance_ledger.governance_hash_chain import (
    GovernanceHashChain,
)

from epics.ztc19_governance_ledger.governance_chain_verifier import (
    GovernanceChainVerifier,
)

from epics.ztc19_governance_ledger.governance_audit_record import (
    GovernanceAuditRecord,
)


def test_end_to_end_governance_ledger_flow():

    event = GovernanceEvent(
        event_id="event-001",
        event_type="incident_declaration",
        payload_hash="hash-001",
    )

    policy = GovernanceAdmissionPolicy()

    assert policy.accept(event)

    entry = GovernanceLedgerEntry(
        sequence=1,
        event_id=event.event_id,
    )

    ledger = GovernanceLedger()

    ledger.append(entry)

    assert ledger.count() == 1

    chain = GovernanceHashChain()

    chain.append(entry)

    verifier = GovernanceChainVerifier()

    valid = verifier.verify(
        chain._records
    )

    assert valid is True

    audit = GovernanceAuditRecord(
        audit_id="audit-001",
        ledger_valid=valid,
    )

    assert audit.ledger_valid is True
