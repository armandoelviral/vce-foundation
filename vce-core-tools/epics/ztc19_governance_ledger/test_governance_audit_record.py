from epics.ztc19_governance_ledger.governance_audit_record import (
    GovernanceAuditRecord,
)


def test_audit_record_contains_audit_id():

    record = GovernanceAuditRecord(
        audit_id="audit-001",
        ledger_valid=True,
    )

    assert record.audit_id == "audit-001"


def test_audit_record_contains_validity_status():

    record = GovernanceAuditRecord(
        audit_id="audit-001",
        ledger_valid=True,
    )

    assert record.ledger_valid is True


def test_audit_record_serializes():

    record = GovernanceAuditRecord(
        audit_id="audit-001",
        ledger_valid=False,
    )

    assert record.to_dict() == {
        "audit_id": "audit-001",
        "ledger_valid": False,
    }
