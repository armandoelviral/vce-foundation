import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_state_read_result import (
    BackendUnavailable,
    Found,
    InvalidResponse,
    NotFound,
    RequestRejected,
    TransportUnavailable,
)
from sp001.services.case_state_reconciliation import (
    CaseStateReconciler,
    ReadRequest,
    ViewStatus,
)


def state(revision=8, case_id="CASE-001", scope="STORE-001"):
    return CaseAuthoritativeState(
        case_id=case_id,
        objective_id="OBJ-001",
        scope=scope,
        phase=CaseLifecyclePhase.CASE_OPENED,
        revision=revision,
        resource_links=(),
    )


def deliver(consumer, result):
    request = consumer.begin_read()
    assert consumer.accept(request=request, result=result)
    return consumer.view


def populated():
    consumer = CaseStateReconciler(case_id="CASE-001")
    original = state()
    deliver(consumer, Found(original))
    return consumer, original


def test_initial_view_and_pending_read_are_unconfirmed():
    consumer = CaseStateReconciler(case_id="CASE-001")
    assert consumer.view.status is ViewStatus.UNCONFIRMED
    assert consumer.view.last_valid_state is None
    first = consumer.begin_read()
    second = consumer.begin_read()
    assert second.sequence == first.sequence + 1
    assert second.case_id == "CASE-001"


def test_newer_revision_updates_view():
    consumer, original = populated()
    incoming = state(9)
    view = deliver(consumer, Found(incoming))
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state is incoming
    assert original.revision == 8


def test_older_revision_cannot_replace_current_state():
    consumer, original = populated()
    view = deliver(consumer, Found(state(7)))
    assert view.last_valid_state is original
    assert view.status is ViewStatus.STALE_RESPONSE


def test_equal_revision_and_content_is_idempotent():
    consumer, original = populated()
    view = deliver(consumer, Found(state(8)))
    assert view.last_valid_state is original
    assert view.status is ViewStatus.CURRENT


def test_equal_revision_with_different_content_is_rejected():
    consumer, original = populated()
    view = deliver(consumer, Found(state(8, scope="OTHER")))
    assert view.last_valid_state is original
    assert view.status is ViewStatus.INVALID_RESPONSE
    assert view.reason == "same_revision_conflicting_state"


@pytest.mark.parametrize(
    "result", [Found(state(case_id="OTHER")), NotFound("OTHER")]
)
def test_wrong_case_is_rejected(result):
    consumer, original = populated()
    view = deliver(consumer, result)
    assert view.last_valid_state is original
    assert view.status is ViewStatus.INVALID_RESPONSE
    assert view.reason == "case_id_mismatch"


@pytest.mark.parametrize(
    "result",
    [
        Found(state(9)),
        NotFound("CASE-001"),
        TransportUnavailable("timeout"),
        BackendUnavailable(503),
        InvalidResponse("proxy 404"),
        RequestRejected(403, "forbidden"),
    ],
)
def test_superseded_response_cannot_change_any_view_field(result):
    consumer, original = populated()
    older_request = consumer.begin_read()
    newer_request = consumer.begin_read()
    assert consumer.accept(
        request=newer_request, result=Found(state(10))
    )
    before = consumer.view
    assert not consumer.accept(request=older_request, result=result)
    assert consumer.view is before
    assert consumer.view.last_valid_state.revision == 10


def test_latest_issued_request_supersedes_prior_even_before_completion():
    consumer, original = populated()
    older = consumer.begin_read()
    consumer.begin_read()
    before = consumer.view
    assert not consumer.accept(request=older, result=Found(state(9)))
    assert consumer.view is before
    assert consumer.view.last_valid_state is original


def test_response_token_can_only_be_consumed_once():
    consumer, original = populated()
    request = consumer.begin_read()
    assert consumer.accept(request=request, result=Found(state(9)))
    before = consumer.view
    assert not consumer.accept(
        request=request, result=NotFound("CASE-001")
    )
    assert consumer.view is before


def test_foreign_or_reconstructed_token_is_not_accepted():
    consumer, original = populated()
    request = consumer.begin_read()
    foreign = CaseStateReconciler(case_id="CASE-001").begin_read()
    copied = ReadRequest(request.case_id, request.sequence)
    for token in (foreign, copied):
        assert not consumer.accept(
            request=token, result=NotFound("CASE-001")
        )
    assert consumer.accept(request=request, result=Found(state(9)))


@pytest.mark.parametrize(
    "result,status",
    [
        (TransportUnavailable("timeout"), ViewStatus.UNAVAILABLE),
        (BackendUnavailable(429), ViewStatus.UNAVAILABLE),
        (BackendUnavailable(503), ViewStatus.UNAVAILABLE),
        (InvalidResponse("infrastructure 404"), ViewStatus.INVALID_RESPONSE),
        (RequestRejected(403, "forbidden"), ViewStatus.REQUEST_REJECTED),
        (None, ViewStatus.INVALID_RESPONSE),
        ({"status": 404}, ViewStatus.INVALID_RESPONSE),
    ],
)
def test_failure_preserves_last_state_without_claiming_absence(result, status):
    consumer, original = populated()
    view = deliver(consumer, result)
    assert view.last_valid_state is original
    assert view.status is status


def test_confirmed_absence_preserves_history_and_revision_watermark():
    consumer, original = populated()
    view = deliver(consumer, NotFound("CASE-001"))
    assert view.status is ViewStatus.NOT_FOUND
    assert view.last_valid_state is original
    view = deliver(consumer, Found(state(7)))
    assert view.last_valid_state is original
    assert view.status is ViewStatus.STALE_RESPONSE


def test_absence_without_previous_state():
    consumer = CaseStateReconciler(case_id="CASE-001")
    view = deliver(consumer, NotFound("CASE-001"))
    assert view.status is ViewStatus.NOT_FOUND
    assert view.last_valid_state is None


def test_successful_read_recovers_after_unavailability():
    consumer, original = populated()
    deliver(consumer, TransportUnavailable("timeout"))
    view = deliver(consumer, Found(state(9)))
    assert view.status is ViewStatus.CURRENT
    assert view.reason is None
    assert view.last_valid_state.revision == 9


def test_local_reader_can_feed_reconciliation(tmp_path):
    from sp001.services.local_case_state_reader import LocalCaseStateReader
    from sp001.services.case_lifecycle_application import open_case
    from sp001.services.sqlite_case_authoritative_state_store import (
        SqliteCaseAuthoritativeStateStore,
    )

    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    expected = open_case(
        store=store,
        case_id="CASE-001",
        objective_id="OBJ-001",
        scope="STORE-001",
        transition_id="TRANSITION-1",
    )
    reader = LocalCaseStateReader(store=store)
    consumer = CaseStateReconciler(case_id="CASE-001")
    request = consumer.begin_read()
    assert consumer.accept(
        request=request, result=reader.read(case_id=request.case_id)
    )
    assert consumer.view.status is ViewStatus.CURRENT
    assert consumer.view.last_valid_state == expected

    missing = CaseStateReconciler(case_id="MISSING")
    request = missing.begin_read()
    assert missing.accept(
        request=request, result=reader.read(case_id=request.case_id)
    )
    assert missing.view.status is ViewStatus.NOT_FOUND


@pytest.mark.parametrize("case_id", [None, 1, True, "", " "])
def test_invalid_case_id_is_rejected(case_id):
    with pytest.raises((TypeError, ValueError)):
        CaseStateReconciler(case_id=case_id)
