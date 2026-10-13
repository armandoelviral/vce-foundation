from typing import Protocol, runtime_checkable

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)


@runtime_checkable
class CaseAuthoritativeStateStore(Protocol):
    """Atomic persistence port for current state and transition history."""

    def read(
        self,
        *,
        case_id: str,
    ) -> CaseAuthoritativeState | None:
        """Read the authoritative current state for one case."""
        ...

    def create(
        self,
        *,
        state: CaseAuthoritativeState,
        transition: CaseLifecycleTransitionRecord,
    ) -> bool:
        """Atomically create revision one and its initial transition."""
        ...

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: CaseAuthoritativeState,
        transition: CaseLifecycleTransitionRecord,
    ) -> bool:
        """Atomically append one transition and replace the current state.

        Return False when the case is missing or its revision is stale.
        """
        ...

    def read_transitions(
        self,
        *,
        case_id: str,
    ) -> tuple[CaseLifecycleTransitionRecord, ...]:
        """Read the immutable transition history in revision order."""
        ...
