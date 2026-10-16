from dataclasses import replace

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.contracts.case_authoritative_state_store import CaseWriteDeadlineExceeded
from sp001.contracts.case_lifecycle_execution_store import (
    CaseLifecycleRequestConflict,
)
from sp001.infrastructure.sqlite_case_lifecycle_execution import (
    SqliteCaseLifecycleExecutionStore,
)
import sp001.runtime.scientific_product_runtime as runtime_module
import sp001.services.sqlite_case_authoritative_state_store as state_module


def test_runtime_recovers_original_result_after_case_advances_and_reopen(tmp_path):
    path = tmp_path / "case.sqlite3"
    store = SqliteCaseLifecycleExecutionStore(database_path=path)
    runtime = runtime_module.ScientificProductRuntime(
        case_authoritative_state_store=store,
        case_lifecycle_execution_store=store,
        case_write_budget_ns=2_000_000_000,
    )
    assert runtime.execute_case_lifecycle(request=opening().request) == opening()
    assert runtime.execute_case_lifecycle(request=completion().request) == completion()

    reopened = SqliteCaseLifecycleExecutionStore(database_path=path)
    recovered_runtime = runtime_module.ScientificProductRuntime(
        case_authoritative_state_store=reopened,
        case_lifecycle_execution_store=reopened,
    )
    assert recovered_runtime.recover_case_lifecycle(
        request=opening().request,
    ) == opening()
    assert recovered_runtime.execute_case_lifecycle(
        request=opening().request,
    ) == opening()
    assert recovered_runtime.read_case_authoritative_state(
        case_id="CASE-1",
    ) == completion().state
    assert len(reopened.read_transitions(case_id="CASE-1")) == 2


def test_runtime_preserves_original_deadline_and_request_reference(monkeypatch):
    now = [100]
    received = []

    class Backend:
        def execute(self, *, request, write_deadline_ns=None):
            now[0] = 150
            received.append((request, write_deadline_ns))
            return opening()

        def recover(self, *, request):
            return opening()

    monkeypatch.setattr(runtime_module, "perf_counter_ns", lambda: now[0])
    runtime = runtime_module.ScientificProductRuntime(
        case_lifecycle_execution_store=Backend(), case_write_budget_ns=100,
    )
    request_value = opening().request
    assert runtime.execute_case_lifecycle(request=request_value) == opening()
    assert received[0][0] is request_value
    assert received[0][1] == 200


def test_expiry_before_storage_does_not_create_partial_result(tmp_path, monkeypatch):
    now = [100]
    monkeypatch.setattr(runtime_module, "perf_counter_ns", lambda: now[0])
    monkeypatch.setattr(state_module, "perf_counter_ns", lambda: now[0])

    class DelayedStore(SqliteCaseLifecycleExecutionStore):
        def execute(self, *, request, write_deadline_ns=None):
            now[0] = 200
            return super().execute(
                request=request, write_deadline_ns=write_deadline_ns,
            )

    store = DelayedStore(database_path=tmp_path / "case.sqlite3")
    runtime = runtime_module.ScientificProductRuntime(
        case_lifecycle_execution_store=store, case_write_budget_ns=100,
    )
    with pytest.raises(CaseWriteDeadlineExceeded):
        runtime.execute_case_lifecycle(request=opening().request)
    assert store.read(case_id="CASE-1") is None
    assert store.read_transitions(case_id="CASE-1") == ()
    assert runtime.recover_case_lifecycle(request=opening().request) is None


def test_contradiction_is_not_converted_to_generic_failure(tmp_path):
    store = SqliteCaseLifecycleExecutionStore(
        database_path=tmp_path / "case.sqlite3",
    )
    runtime = runtime_module.ScientificProductRuntime(
        case_lifecycle_execution_store=store,
    )
    runtime.execute_case_lifecycle(request=opening().request)
    changed = replace(opening().request, scope="OTHER")
    for method in (
        runtime.execute_case_lifecycle, runtime.recover_case_lifecycle,
    ):
        with pytest.raises(CaseLifecycleRequestConflict):
            method(request=changed)


@pytest.mark.parametrize("method", [
    "execute_case_lifecycle", "recover_case_lifecycle",
])
def test_missing_backend_is_explicit(method):
    runtime = runtime_module.ScientificProductRuntime()
    with pytest.raises(RuntimeError, match="not configured"):
        getattr(runtime, method)(request=opening().request)


def test_invalid_backend_is_rejected():
    with pytest.raises(TypeError, match="CaseLifecycleExecutionStore"):
        runtime_module.ScientificProductRuntime(
            case_lifecycle_execution_store=object(),
        )


def test_wrong_backend_result_is_rejected():
    class Backend:
        def execute(self, *, request, write_deadline_ns=None):
            return completion()

        def recover(self, *, request):
            return completion()

    runtime = runtime_module.ScientificProductRuntime(
        case_lifecycle_execution_store=Backend(),
    )
    for method in (
        runtime.execute_case_lifecycle, runtime.recover_case_lifecycle,
    ):
        with pytest.raises(ValueError, match="different transition identity"):
            method(request=opening().request)
