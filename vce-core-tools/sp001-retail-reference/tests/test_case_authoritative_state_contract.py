from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_resource_link import CaseResourceLink


def link(
    relationship: str = "evidence",
    resource_type: str = "operational_evidence",
    resource_id: str = "EVIDENCE-001",
) -> CaseResourceLink:
    return CaseResourceLink(
        relationship=relationship,
        resource_type=resource_type,
        resource_id=resource_id,
    )


def state(
    *,
    phase: CaseLifecyclePhase = CaseLifecyclePhase.CASE_OPENED,
    revision: int = 1,
    resource_links: tuple[CaseResourceLink, ...] = (),
) -> CaseAuthoritativeState:
    return CaseAuthoritativeState(
        case_id="CASE-001",
        objective_id="OBJ-001",
        scope="STORE-MX-014",
        phase=phase,
        revision=revision,
        resource_links=resource_links,
    )


def test_phase_vocabulary_has_exactly_six_operational_phases() -> None:
    assert tuple(phase.value for phase in CaseLifecyclePhase) == (
        "CASE_OPENED",
        "RECOMMENDATION_AVAILABLE",
        "AWAITING_EXPERT_DECISION",
        "EXPERT_DECISION_RECORDED",
        "EXECUTION_RECORDED",
        "OPERATIONAL_EVIDENCE_RECORDED",
    )


def test_case_state_has_exact_fields() -> None:
    assert tuple(field.name for field in fields(CaseAuthoritativeState)) == (
        "case_id",
        "objective_id",
        "scope",
        "phase",
        "revision",
        "resource_links",
    )


def test_case_state_preserves_exact_values() -> None:
    links = (link(),)
    value = state(
        phase=CaseLifecyclePhase.OPERATIONAL_EVIDENCE_RECORDED,
        revision=6,
        resource_links=links,
    )
    assert value.case_id == "CASE-001"
    assert value.objective_id == "OBJ-001"
    assert value.scope == "STORE-MX-014"
    assert value.phase is CaseLifecyclePhase.OPERATIONAL_EVIDENCE_RECORDED
    assert value.revision == 6
    assert value.resource_links is links


def test_case_state_is_frozen_and_slotted() -> None:
    value = state()
    with pytest.raises(FrozenInstanceError):
        value.phase = CaseLifecyclePhase.EXECUTION_RECORDED
    assert not hasattr(value, "__dict__")


@pytest.mark.parametrize("value", [0, -1, 1 << 64])
def test_revision_rejects_out_of_range_values(value: int) -> None:
    with pytest.raises(ValueError, match="positive uint64"):
        state(revision=value)


@pytest.mark.parametrize("value", [True, 1.0, "1"])
def test_revision_rejects_non_integer_values(value: object) -> None:
    with pytest.raises(TypeError, match="revision"):
        state(revision=value)  # type: ignore[arg-type]


def test_case_state_requires_nominal_phase() -> None:
    with pytest.raises(TypeError, match="CaseLifecyclePhase"):
        state(phase="CASE_OPENED")  # type: ignore[arg-type]


def test_resource_links_require_canonical_order() -> None:
    links = (
        link(relationship="z"),
        link(relationship="a", resource_id="EVIDENCE-002"),
    )
    with pytest.raises(ValueError, match="canonical order"):
        state(resource_links=links)


def test_resource_links_reject_duplicates() -> None:
    with pytest.raises(ValueError, match="unique"):
        state(resource_links=(link(), link()))


def test_resource_link_vocabulary_stays_open() -> None:
    value = link(
        relationship="retail_context",
        resource_type="future_observation_kind",
        resource_id="OBS-009",
    )
    assert value.resource_type == "future_observation_kind"
