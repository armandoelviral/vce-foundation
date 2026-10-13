import sqlite3

import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.models.objective import Objective
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime
from sp001.services.case_lifecycle_application import (
    apply_case_lifecycle_transition,
)
from sp001.services.case_state_reconciliation import (
    CaseStateReconciler,
    ViewStatus,
)
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def state(revision=8, case_id="CASE-001"):
    return CaseAuthoritativeState(
        case_id=case_id,
        objective_id="OBJ-001",
        scope="",
        phase=Phase.CASE_OPENED,
        revision=revision,
        resource_links=(),
    )


class ControlledStore:
    def __init__(self):
        self.result = state()
        self.error = None
        self.read_count = 0

    def read(self, *, case_id):
        self.read_count += 1
        if self.error is not None:
            raise self.error
        return self.result

    def create(self, *, state, transition):
        raise AssertionError("refresh must not create")

    def compare_and_swap(self, *, expected_revision, next_state, transition):
        raise AssertionError("refresh must not mutate")

    def read_transitions(self, *, case_id):
        raise AssertionError("refresh must not read history")


def subscribed():
    store = ControlledStore()
    runtime = ScientificProductRuntime(case_authoritative_state_store=store)
    subscription = runtime.subscribe_case_state(case_id="CASE-001")
    original = subscription.refresh().last_valid_state
    return store, subscription, original


def test_runtime_creation_and_refresh_share_durable_store(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    runtime = ScientificProductRuntime(case_authoritative_state_store=store)
    subscription = runtime.subscribe_case_state(case_id="CASE-001")

    assert subscription.refresh().status is ViewStatus.NOT_FOUND
    created = runtime.create_case(
        Objective(objective_id="OBJ-001", title="Retail objective"),
        case_id="CASE-001",
        scope="STORE-001",
    )
    assert created.success
    view = subscription.refresh()
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state.revision == 1

    updated = apply_case_lifecycle_transition(
        store=store,
        case_id="CASE-001",
        expected_revision=1,
        transition_id="TRANSITION-2",
        to_phase=Phase.RECOMMENDATION_AVAILABLE,
    )
    view = subscription.refresh()
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state == updated
    assert view.last_valid_state.revision == 2
    assert len(store.read_transitions(case_id="CASE-001")) == 2


def test_runtime_requires_configured_store():
    with pytest.raises(RuntimeError, match="store is not configured"):
        ScientificProductRuntime().subscribe_case_state(case_id="CASE-001")


def test_session_creation_does_not_read_store():
    store = ControlledStore()
    runtime = ScientificProductRuntime(case_authoritative_state_store=store)
    subscription = runtime.subscribe_case_state(case_id="CASE-001")
    assert store.read_count == 0
    assert subscription.view.status is ViewStatus.UNCONFIRMED


@pytest.mark.parametrize("case_id", [None, 1, True, "", " "])
def test_invalid_case_id_does_not_read_store(case_id):
    store = ControlledStore()
    runtime = ScientificProductRuntime(case_authoritative_state_store=store)
    with pytest.raises((TypeError, ValueError)):
        runtime.subscribe_case_state(case_id=case_id)
    assert store.read_count == 0


def test_session_retains_revision_across_refreshes():
    store, subscription, original = subscribed()
    store.result = state(7)
    view = subscription.refresh()
    assert view.status is ViewStatus.STALE_RESPONSE
    assert view.last_valid_state is original
    store.result = state(9)
    assert subscription.refresh().last_valid_state.revision == 9


@pytest.mark.parametrize(
    "error",
    [
        sqlite3.OperationalError("database locked"),
        TimeoutError("local reader timeout"),
        RuntimeError("unexpected reader failure"),
    ],
)
def test_exception_closes_read_preserves_state_and_propagates(error):
    store, subscription, original = subscribed()
    count = store.read_count
    store.error = error
    with pytest.raises(type(error)) as caught:
        subscription.refresh()
    assert caught.value is error
    assert store.read_count == count + 1
    assert subscription.view.status is ViewStatus.READ_FAILED
    assert subscription.view.last_valid_state is original

    store.error = None
    store.result = state(9)
    assert subscription.refresh().status is ViewStatus.CURRENT
    assert subscription.view.last_valid_state.revision == 9


def test_wrong_case_from_local_store_is_not_absence():
    store, subscription, original = subscribed()
    store.result = state(case_id="OTHER")
    with pytest.raises(ValueError, match="different case_id"):
        subscription.refresh()
    assert subscription.view.status is ViewStatus.READ_FAILED
    assert subscription.view.last_valid_state is original


def test_invalid_local_response_is_not_absence():
    store, subscription, original = subscribed()
    store.result = {}
    with pytest.raises(TypeError, match="store.read must return"):
        subscription.refresh()
    assert subscription.view.status is ViewStatus.READ_FAILED
    assert subscription.view.last_valid_state is original


def test_confirmed_absence_preserves_historical_state():
    store, subscription, original = subscribed()
    store.result = None
    assert subscription.refresh().status is ViewStatus.NOT_FOUND
    assert subscription.view.last_valid_state is original


def test_failed_request_is_consumed_and_superseded_failure_is_ignored():
    reconciler = CaseStateReconciler(case_id="CASE-001")
    older = reconciler.begin_read()
    latest = reconciler.begin_read()
    before = reconciler.view
    assert not reconciler.fail_read(request=older)
    assert reconciler.view is before
    assert reconciler.fail_read(request=latest)
    assert reconciler.view.status is ViewStatus.READ_FAILED
    before = reconciler.view
    assert not reconciler.fail_read(request=latest)
    assert reconciler.view is before
