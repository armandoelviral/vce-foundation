import pytest

from sp001.contracts.case_authoritative_state_store import (
    CaseWriteDeadlineExceeded,
)
from sp001.models.objective import Objective
import sp001.runtime.scientific_product_runtime as runtime_module
import sp001.services.sqlite_case_authoritative_state_store as sqlite_module


def create(runtime, case_id="CASE-001"):
    return runtime.create_case(
        Objective(objective_id="OBJ-001"),
        case_id=case_id, scope="STORE-001",
    )


def test_preparation_consumes_budget_without_reset_and_retry_gets_new_budget(
    tmp_path, monkeypatch,
):
    now = [100]
    monkeypatch.setattr(runtime_module, "perf_counter_ns", lambda: now[0])
    monkeypatch.setattr(sqlite_module, "perf_counter_ns", lambda: now[0])
    store = sqlite_module.SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3",
    )
    runtime = runtime_module.ScientificProductRuntime(
        case_authoritative_state_store=store, case_write_budget_ns=100,
    )
    original = runtime._objective_to_case

    class SlowTransition:
        def execute(self, *args, **kwargs):
            result = original.execute(*args, **kwargs)
            now[0] = 200
            return result

    runtime._objective_to_case = SlowTransition()
    with pytest.raises(CaseWriteDeadlineExceeded):
        create(runtime)
    assert store.read(case_id="CASE-001") is None
    assert store.read_transitions(case_id="CASE-001") == ()

    runtime._objective_to_case = original
    result = create(runtime)
    assert result.success
    assert store.read(case_id="CASE-001").revision == 1
    assert len(store.read_transitions(case_id="CASE-001")) == 1


def test_runtime_passes_original_deadline_after_preparation(
    tmp_path, monkeypatch,
):
    now = [100]
    received = []
    monkeypatch.setattr(runtime_module, "perf_counter_ns", lambda: now[0])
    monkeypatch.setattr(sqlite_module, "perf_counter_ns", lambda: now[0])

    class RecordingStore(sqlite_module.SqliteCaseAuthoritativeStateStore):
        def create(self, *, state, transition, write_deadline_ns=None):
            received.append(write_deadline_ns)
            return super().create(
                state=state, transition=transition,
                write_deadline_ns=write_deadline_ns,
            )

    store = RecordingStore(database_path=tmp_path / "case.sqlite3")
    runtime = runtime_module.ScientificProductRuntime(
        case_authoritative_state_store=store, case_write_budget_ns=100,
    )
    original = runtime._objective_to_case

    class Transition:
        def execute(self, *args, **kwargs):
            result = original.execute(*args, **kwargs)
            now[0] = 150
            return result

    runtime._objective_to_case = Transition()
    assert create(runtime).success
    assert received == [200]


@pytest.mark.parametrize("value", [True, 1.5, "100"])
def test_invalid_budget_type(value):
    with pytest.raises(TypeError, match="integer"):
        runtime_module.ScientificProductRuntime(case_write_budget_ns=value)


@pytest.mark.parametrize("value", [0, -1])
def test_nonpositive_budget(value):
    with pytest.raises(ValueError, match="positive"):
        runtime_module.ScientificProductRuntime(case_write_budget_ns=value)


def test_budget_requires_durable_store():
    with pytest.raises(ValueError, match="durable store"):
        runtime_module.ScientificProductRuntime(case_write_budget_ns=100)
