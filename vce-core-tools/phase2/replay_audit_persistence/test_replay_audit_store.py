from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)

from phase2.replay_audit_persistence.replay_audit_store import (
    ReplayAuditStore,
)


def test_store_starts_empty():

    store = ReplayAuditStore()

    assert store.count() == 0


def test_store_accepts_record():

    store = ReplayAuditStore()

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    store.add(record)

    assert store.count() == 1


def test_store_returns_record():

    store = ReplayAuditStore()

    record = ReplayAuditRecord(
        replay_id="replay-001",
        audit_result=True,
    )

    store.add(record)

    recovered = store.get(
        "replay-001"
    )

    assert recovered == record


def test_unknown_record_returns_none():

    store = ReplayAuditStore()

    assert store.get(
        "missing"
    ) is None
