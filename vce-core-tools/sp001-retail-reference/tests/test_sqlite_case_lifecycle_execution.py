import sqlite3
from dataclasses import replace

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.contracts.case_lifecycle_execution_store import (
    CaseLifecycleExecutionStore, CaseLifecycleRequestConflict,
)
from sp001.infrastructure.sqlite_case_lifecycle_execution import (
    SqliteCaseLifecycleExecutionStore,
)


def adapter(tmp_path):
    return SqliteCaseLifecycleExecutionStore(
        database_path=tmp_path / "case.sqlite3",
    )


def test_opening_and_transition_persist_exact_results_across_reopen(tmp_path):
    store = adapter(tmp_path)
    assert isinstance(store, CaseLifecycleExecutionStore)
    first = store.execute(request=opening().request)
    second = store.execute(request=completion().request)
    assert first == opening()
    assert second == completion()
    reopened = adapter(tmp_path)
    assert reopened.recover(request=first.request) == first
    assert reopened.execute(request=first.request) == first
    assert reopened.recover(request=second.request) == second
    assert reopened.read(case_id="CASE-1") == second.state
    assert len(reopened.read_transitions(case_id="CASE-1")) == 2


@pytest.mark.parametrize("field,value", [
    ("objective_id", "OTHER"),
    ("scope", "OTHER"),
    ("case_id", "OTHER"),
    ("resource_links", ()),
])
def test_reused_identity_with_changed_content_is_rejected(tmp_path, field, value):
    store = adapter(tmp_path)
    original = store.execute(request=opening().request)
    changed = replace(original.request, **{field: value})
    for method in (store.execute, store.recover):
        with pytest.raises(CaseLifecycleRequestConflict):
            method(request=changed)
    assert store.recover(request=original.request) == original
    assert len(store.read_transitions(case_id="CASE-1")) == 1


def test_absence_and_stale_revision_do_not_create_receipts(tmp_path):
    store = adapter(tmp_path)
    assert store.recover(request=opening().request) is None
    store.execute(request=opening().request)
    stale = replace(completion().request, expected_revision=7)
    assert store.execute(request=stale) is None
    assert store.recover(request=stale) is None
    assert store.read(case_id="CASE-1").revision == 1


def test_completion_insert_failure_rolls_back_state_history_and_receipt(tmp_path):
    store = adapter(tmp_path)
    path = tmp_path / "case.sqlite3"
    connection = sqlite3.connect(path)
    try:
        connection.execute("""
            CREATE TRIGGER fail_completion BEFORE INSERT
            ON case_lifecycle_completions BEGIN
                SELECT RAISE(ABORT, 'controlled completion failure');
            END
        """)
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(sqlite3.IntegrityError):
        store.execute(request=opening().request)
    assert store.read(case_id="CASE-1") is None
    assert store.read_transitions(case_id="CASE-1") == ()
    assert store.recover(request=opening().request) is None

    connection = sqlite3.connect(path)
    try:
        connection.execute("DROP TRIGGER fail_completion")
        connection.commit()
    finally:
        connection.close()
    assert store.execute(request=opening().request) == opening()


def test_legacy_transition_is_not_reconstructed_as_an_exact_request(tmp_path):
    store = adapter(tmp_path)
    original = opening()
    assert store.create(state=original.state, transition=original.transition)
    assert store.recover(request=original.request) is None
    with pytest.raises(ValueError, match="without a recoverable"):
        store.execute(request=original.request)
    assert store.read_transitions(case_id="CASE-1") == (original.transition,)


def test_lifecycle_policy_still_rejects_phase_skip(tmp_path):
    from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
    store = adapter(tmp_path)
    store.execute(request=opening().request)
    invalid = replace(
        completion().request, to_phase=Phase.AWAITING_EXPERT_DECISION,
    )
    with pytest.raises(ValueError, match="not allowed"):
        store.execute(request=invalid)
    assert store.recover(request=invalid) is None
    assert store.read(case_id="CASE-1").revision == 1
