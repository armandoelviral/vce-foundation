from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)


def test_record_contains_replay_id():

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    assert record.replay_id == "replay-001"


def test_record_contains_audit_result():

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    assert record.audit_result is True


def test_record_serializes():

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    assert record.to_dict() == {
        "replay_id": "replay-001",
        "audit_result": True,
    }
