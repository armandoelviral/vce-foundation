from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_authoritative_state_store import CaseAuthoritativeStateStore
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)
from sp001.contracts.case_resource_link import CaseResourceLink


_UINT64_MAX = (1 << 64) - 1
_ALLOWED = {
    Phase.CASE_OPENED: {Phase.RECOMMENDATION_AVAILABLE},
    Phase.RECOMMENDATION_AVAILABLE: {Phase.AWAITING_EXPERT_DECISION},
    Phase.AWAITING_EXPERT_DECISION: {Phase.EXPERT_DECISION_RECORDED},
    Phase.EXPERT_DECISION_RECORDED: {Phase.EXECUTION_RECORDED},
    Phase.EXECUTION_RECORDED: {Phase.OPERATIONAL_EVIDENCE_RECORDED},
    Phase.OPERATIONAL_EVIDENCE_RECORDED: {Phase.RECOMMENDATION_AVAILABLE},
}


def _validate_store(store: object) -> None:
    if not isinstance(store, CaseAuthoritativeStateStore):
        raise TypeError("store must implement CaseAuthoritativeStateStore")


def _validate_text(value: object, field: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    if not value.strip():
        raise ValueError(f"{field} must not be empty")


def _canonical_links(
    links: object,
) -> tuple[CaseResourceLink, ...]:
    if not isinstance(links, tuple):
        raise TypeError("resource_links must be a tuple")
    if any(not isinstance(link, CaseResourceLink) for link in links):
        raise TypeError(
            "resource_links must contain only CaseResourceLink values"
        )
    keys = tuple(
        (link.relationship, link.resource_type, link.resource_id)
        for link in links
    )
    if len(set(keys)) != len(keys):
        raise ValueError("resource_links must be unique")
    return tuple(sorted(links, key=lambda link: (
        link.relationship, link.resource_type, link.resource_id
    )))


def open_case(
    *,
    store: CaseAuthoritativeStateStore,
    case_id: str,
    objective_id: str,
    scope: str,
    transition_id: str,
    resource_links: tuple[CaseResourceLink, ...] = (),
) -> CaseAuthoritativeState | None:
    _validate_store(store)
    _validate_text(case_id, "case_id")
    _validate_text(objective_id, "objective_id")
    if not isinstance(scope, str):
        raise TypeError("scope must be a string")
    _validate_text(transition_id, "transition_id")
    links = _canonical_links(resource_links)

    state = CaseAuthoritativeState(
        case_id=case_id,
        objective_id=objective_id,
        scope=scope,
        phase=Phase.CASE_OPENED,
        revision=1,
        resource_links=links,
    )
    transition = CaseLifecycleTransitionRecord(
        case_id=case_id,
        transition_id=transition_id,
        revision=1,
        from_phase=None,
        to_phase=Phase.CASE_OPENED,
        resource_links=links,
    )
    return state if store.create(state=state, transition=transition) else None


def apply_case_lifecycle_transition(
    *,
    store: CaseAuthoritativeStateStore,
    case_id: str,
    expected_revision: int,
    transition_id: str,
    to_phase: Phase,
    resource_links: tuple[CaseResourceLink, ...] = (),
) -> CaseAuthoritativeState | None:
    _validate_store(store)
    _validate_text(case_id, "case_id")
    _validate_text(transition_id, "transition_id")
    if (
        isinstance(expected_revision, bool)
        or not isinstance(expected_revision, int)
    ):
        raise TypeError("expected_revision must be an integer")
    if expected_revision < 1 or expected_revision > _UINT64_MAX:
        raise ValueError("expected_revision must be a positive uint64")
    if not isinstance(to_phase, Phase):
        raise TypeError("to_phase must be a CaseLifecyclePhase")
    additions = _canonical_links(resource_links)

    current = store.read(case_id=case_id)
    if current is None or current.revision != expected_revision:
        return None
    if current.revision == _UINT64_MAX:
        raise OverflowError("case revision cannot exceed uint64")

    if to_phase == current.phase:
        if not additions:
            raise ValueError(
                "same-phase mutation must add at least one resource link"
            )
    elif to_phase not in _ALLOWED[current.phase]:
        raise ValueError(
            f"transition from {current.phase.value} to "
            f"{to_phase.value} is not allowed"
        )

    existing = {
        (link.relationship, link.resource_type, link.resource_id)
        for link in current.resource_links
    }
    added = {
        (link.relationship, link.resource_type, link.resource_id)
        for link in additions
    }
    if existing.intersection(added):
        raise ValueError("resource link is already present")

    links = _canonical_links(current.resource_links + additions)
    next_state = CaseAuthoritativeState(
        case_id=current.case_id,
        objective_id=current.objective_id,
        scope=current.scope,
        phase=to_phase,
        revision=current.revision + 1,
        resource_links=links,
    )
    transition = CaseLifecycleTransitionRecord(
        case_id=current.case_id,
        transition_id=transition_id,
        revision=next_state.revision,
        from_phase=current.phase,
        to_phase=to_phase,
        resource_links=links,
    )
    accepted = store.compare_and_swap(
        expected_revision=expected_revision,
        next_state=next_state,
        transition=transition,
    )
    return next_state if accepted else None
