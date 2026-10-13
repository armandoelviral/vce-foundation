import pytest

from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.models.objective import Objective
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def test_runtime_persists_and_reads_opened_case(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    runtime = ScientificProductRuntime(
        case_authoritative_state_store=store
    )
    objective = Objective(
        objective_id="OBJ-001",
        title="Improve retail presentation",
    )

    result = runtime.create_case(
        objective,
        case_id="CASE-001",
        scope="STORE-MX-014",
    )
    state = runtime.read_case_authoritative_state(
        case_id="CASE-001"
    )

    assert result.success is True
    assert result.output.case_id == "CASE-001"
    assert state is not None
    assert state.case_id == "CASE-001"
    assert state.objective_id == "OBJ-001"
    assert state.scope == "STORE-MX-014"
    assert state.phase is CaseLifecyclePhase.CASE_OPENED
    assert state.revision == 1
    assert len(store.read_transitions(case_id="CASE-001")) == 1


def test_duplicate_runtime_creation_reports_failure_and_preserves_state(
    tmp_path,
):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    runtime = ScientificProductRuntime(
        case_authoritative_state_store=store
    )
    first = runtime.create_case(
        Objective(objective_id="OBJ-001"),
        case_id="CASE-001",
        scope="STORE-MX-014",
    )

    duplicate = runtime.create_case(
        Objective(objective_id="OBJ-OTHER"),
        case_id="CASE-001",
        scope="OTHER",
    )

    assert first.success is True
    assert duplicate.success is False
    assert duplicate.output is None
    state = runtime.read_case_authoritative_state(
        case_id="CASE-001"
    )
    assert state is not None
    assert state.objective_id == "OBJ-001"
    assert state.revision == 1


def test_durable_runtime_rejects_missing_case_id(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    runtime = ScientificProductRuntime(
        case_authoritative_state_store=store
    )

    result = runtime.create_case(
        Objective(objective_id="OBJ-001"),
        scope="STORE-MX-014",
    )

    assert result.success is False
    assert result.output is None


def test_runtime_read_requires_configured_store():
    runtime = ScientificProductRuntime()

    with pytest.raises(RuntimeError, match="store is not configured"):
        runtime.read_case_authoritative_state(case_id="CASE-001")
