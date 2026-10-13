import pytest

from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.contracts.case_resource_link import CaseResourceLink
from sp001.services.case_authoritative_state_reading import (
    read_case_authoritative_state,
)
from sp001.services.case_lifecycle_application import (
    apply_case_lifecycle_transition,
    open_case,
)
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def link(relationship: str, resource_id: str) -> CaseResourceLink:
    return CaseResourceLink(
        relationship=relationship,
        resource_type=relationship,
        resource_id=resource_id,
    )


def opened(store):
    return open_case(
        store=store,
        case_id="CASE-001",
        objective_id="OBJ-001",
        scope="STORE-MX-014",
        transition_id="TRANSITION-1",
    )


def advance(store, revision, phase, transition_id, links=()):
    return apply_case_lifecycle_transition(
        store=store,
        case_id="CASE-001",
        expected_revision=revision,
        transition_id=transition_id,
        to_phase=phase,
        resource_links=links,
    )


def test_open_case_persists_initial_state_and_transition(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )

    state = opened(store)

    assert state is not None
    assert state.phase is Phase.CASE_OPENED
    assert state.revision == 1
    assert store.read_transitions(case_id="CASE-001")[0].from_phase is None


def test_duplicate_case_creation_does_not_replace_original(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    original = opened(store)

    duplicate = open_case(
        store=store,
        case_id="CASE-001",
        objective_id="OBJ-OTHER",
        scope="OTHER",
        transition_id="TRANSITION-DUPLICATE",
    )

    assert duplicate is None
    assert store.read(case_id="CASE-001") == original
    assert len(store.read_transitions(case_id="CASE-001")) == 1


def test_stale_revision_does_not_mutate_case(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    opened(store)

    result = advance(
        store, 9, Phase.RECOMMENDATION_AVAILABLE, "TRANSITION-2"
    )

    assert result is None
    assert store.read(case_id="CASE-001").revision == 1
    assert len(store.read_transitions(case_id="CASE-001")) == 1


def test_invalid_phase_skip_is_rejected_without_mutation(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    opened(store)

    with pytest.raises(ValueError, match="not allowed"):
        advance(
            store, 1, Phase.AWAITING_EXPERT_DECISION, "TRANSITION-2"
        )

    assert store.read(case_id="CASE-001").revision == 1


def test_same_phase_requires_a_new_link(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    opened(store)

    with pytest.raises(ValueError, match="must add"):
        advance(store, 1, Phase.CASE_OPENED, "TRANSITION-2")

    assert store.read(case_id="CASE-001").revision == 1


def test_rework_stays_in_same_case_and_preserves_every_attempt(tmp_path):
    path = tmp_path / "case.sqlite3"
    store = SqliteCaseAuthoritativeStateStore(database_path=path)
    opened(store)

    phases_and_links = (
        (Phase.RECOMMENDATION_AVAILABLE, link("recommendation", "REC-1")),
        (Phase.AWAITING_EXPERT_DECISION, None),
        (Phase.EXPERT_DECISION_RECORDED, link("decision", "DEC-1")),
        (Phase.EXECUTION_RECORDED, link("execution", "EXE-1")),
        (Phase.OPERATIONAL_EVIDENCE_RECORDED, link("evidence", "EVD-1")),
        (Phase.RECOMMENDATION_AVAILABLE, link("recommendation", "REC-2")),
    )
    revision = 1
    for index, (phase, new_link) in enumerate(phases_and_links, start=2):
        result = advance(
            store,
            revision,
            phase,
            f"TRANSITION-{index}",
            () if new_link is None else (new_link,),
        )
        assert result is not None
        revision += 1

    store = SqliteCaseAuthoritativeStateStore(database_path=path)
    state = read_case_authoritative_state(store=store, case_id="CASE-001")
    history = store.read_transitions(case_id="CASE-001")

    assert state is not None
    assert state.case_id == "CASE-001"
    assert state.phase is Phase.RECOMMENDATION_AVAILABLE
    assert state.revision == 7
    assert {item.resource_id for item in state.resource_links} == {
        "REC-1", "DEC-1", "EXE-1", "EVD-1", "REC-2",
    }
    assert tuple(item.revision for item in history) == tuple(range(1, 8))
    assert history[5].from_phase is Phase.EXECUTION_RECORDED
    assert history[5].to_phase is Phase.OPERATIONAL_EVIDENCE_RECORDED
    assert history[6].from_phase is Phase.OPERATIONAL_EVIDENCE_RECORDED
    assert history[6].to_phase is Phase.RECOMMENDATION_AVAILABLE
    assert history[1].resource_links == (
        link("recommendation", "REC-1"),
    )


def test_same_phase_link_addition_advances_revision(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )
    opened(store)

    result = advance(
        store,
        1,
        Phase.CASE_OPENED,
        "TRANSITION-2",
        (link("audit", "AUD-1"),),
    )

    assert result is not None
    assert result.revision == 2
    assert result.phase is Phase.CASE_OPENED
    assert result.resource_links == (link("audit", "AUD-1"),)


def test_authoritative_read_returns_none_for_missing_case(tmp_path):
    store = SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3"
    )

    assert read_case_authoritative_state(
        store=store, case_id="MISSING"
    ) is None
