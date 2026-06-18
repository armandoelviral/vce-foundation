from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)

from phase2.replay_audit_persistence.replay_audit_store import (
    ReplayAuditStore,
)

from phase2.replay_audit_persistence.replay_audit_query import (
    ReplayAuditQuery,
)


def test_query_returns_record_by_replay_id():

    store = ReplayAuditStore()

    store.add(
        ReplayAuditRecord(
            replay_id="replay-001",
            audit_result=True,
        )
    )

    query = ReplayAuditQuery(store)

    result = query.by_replay_id(
        "replay-001"
    )

    assert result.replay_id == "replay-001"


def test_query_returns_none_for_missing_replay():

    store = ReplayAuditStore()

    query = ReplayAuditQuery(store)

    assert query.by_replay_id(
        "missing"
    ) is None


def test_query_returns_correct_result():

    store = ReplayAuditStore()

    store.add(
        ReplayAuditRecord(
            replay_id="replay-001",
            audit_result=True,
        )
    )

    query = ReplayAuditQuery(store)

    result = query.by_replay_id(
        "replay-001"
    )

    assert result.audit_result is True
