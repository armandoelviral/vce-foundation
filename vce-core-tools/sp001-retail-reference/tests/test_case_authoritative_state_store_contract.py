from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_authoritative_state_store import (
    CaseAuthoritativeStateStore,
)
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)
from sp001.contracts.case_resource_link import CaseResourceLink


def transition(
    *,
    revision: int = 1,
    from_phase: CaseLifecyclePhase | None = None,
    to_phase: CaseLifecyclePhase = CaseLifecyclePhase.CASE_OPENED,
    resource_links: tuple[CaseResourceLink, ...] = (),
) -> CaseLifecycleTransitionRecord:
    return CaseLifecycleTransitionRecord(
        case_id="CASE-001",
        transition_id=f"TRANSITION-{revision}",
        revision=revision,
        from_phase=from_phase,
        to_phase=to_phase,
        resource_links=resource_links,
    )


def test_transition_record_has_exact_fields() -> None:
    assert tuple(
        field.name for field in fields(CaseLifecycleTransitionRecord)
    ) == (
        "case_id",
        "transition_id",
        "revision",
        "from_phase",
        "to_phase",
        "resource_links",
    )


def test_initial_transition_preserves_creation_values() -> None:
    value = transition()
    assert value.case_id == "CASE-001"
    assert value.revision == 1
    assert value.from_phase is None
    assert value.to_phase is CaseLifecyclePhase.CASE_OPENED


def test_transition_record_is_frozen_and_slotted() -> None:
    value = transition()
    with pytest.raises(FrozenInstanceError):
        value.revision = 2
    assert not hasattr(value, "__dict__")


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("case_id", "", ValueError),
        ("transition_id", "", ValueError),
        ("revision", True, TypeError),
        ("revision", 0, ValueError),
        ("from_phase", "CASE_OPENED", TypeError),
        ("to_phase", "CASE_OPENED", TypeError),
        ("resource_links", [], TypeError),
    ],
)
def test_transition_record_rejects_invalid_values(
    field: str,
    value: object,
    error: type[Exception],
) -> None:
    values = {
        "case_id": "CASE-001",
        "transition_id": "TRANSITION-001",
        "revision": 1,
        "from_phase": None,
        "to_phase": CaseLifecyclePhase.CASE_OPENED,
        "resource_links": (),
    }
    values[field] = value
    with pytest.raises(error):
        CaseLifecycleTransitionRecord(**values)  # type: ignore[arg-type]


def test_store_port_is_runtime_checkable() -> None:
    class CompleteStore:
        def read(self, *, case_id: str) -> CaseAuthoritativeState | None:
            return None

        def create(
            self,
            *,
            state: CaseAuthoritativeState,
            transition: CaseLifecycleTransitionRecord,
        ) -> bool:
            return True

        def compare_and_swap(
            self,
            *,
            expected_revision: int,
            next_state: CaseAuthoritativeState,
            transition: CaseLifecycleTransitionRecord,
        ) -> bool:
            return True

        def read_transitions(
            self,
            *,
            case_id: str,
        ) -> tuple[CaseLifecycleTransitionRecord, ...]:
            return ()

    assert isinstance(CompleteStore(), CaseAuthoritativeStateStore)
    assert not isinstance(object(), CaseAuthoritativeStateStore)
