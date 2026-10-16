from dataclasses import dataclass

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)


@dataclass(frozen=True, slots=True)
class CaseLifecycleCompletion:
    """Coherent request/result binding.

    Construction validates coherence, not commit, authorization, signature
    or admissibility under a lifecycle policy.
    """

    request: CaseOpeningRequest | CaseTransitionRequest
    state: CaseAuthoritativeState
    transition: CaseLifecycleTransitionRecord
    previous_state: CaseAuthoritativeState | None = None

    def __post_init__(self):
        request = self.request
        state = self.state
        transition = self.transition
        previous = self.previous_state

        if not isinstance(request, (CaseOpeningRequest, CaseTransitionRequest)):
            raise TypeError("request must be a lifecycle request")
        if not isinstance(state, CaseAuthoritativeState):
            raise TypeError("state must be a CaseAuthoritativeState")
        if not isinstance(transition, CaseLifecycleTransitionRecord):
            raise TypeError("transition must be a CaseLifecycleTransitionRecord")
        if previous is not None and not isinstance(previous, CaseAuthoritativeState):
            raise TypeError("previous_state must be a CaseAuthoritativeState or None")

        if not request.case_id == state.case_id == transition.case_id:
            raise ValueError("case identities must match")
        if request.transition_id != transition.transition_id:
            raise ValueError("transition identity must match the request")
        if transition.revision != state.revision:
            raise ValueError("result revisions must match")
        if transition.to_phase is not state.phase:
            raise ValueError("result phases must match")
        if transition.resource_links != state.resource_links:
            raise ValueError("result resource links must match")

        if isinstance(request, CaseOpeningRequest):
            if previous is not None:
                raise ValueError("opening must not have a previous state")
            if state.revision != 1 or state.phase is not Phase.CASE_OPENED:
                raise ValueError("opening must produce CASE_OPENED revision one")
            if transition.from_phase is not None:
                raise ValueError("opening must not have a source phase")
            if (
                state.objective_id != request.objective_id
                or state.scope != request.scope
                or state.resource_links != request.resource_links
            ):
                raise ValueError("opening result must preserve the exact request")
            return

        if previous is None:
            raise ValueError("transition requires its previous state")
        if previous.case_id != request.case_id:
            raise ValueError("previous case identity must match")
        if previous.revision != request.expected_revision:
            raise ValueError("previous revision must match the request")
        if state.revision != request.expected_revision + 1:
            raise ValueError("result must be the exact successor")
        if transition.from_phase is not previous.phase:
            raise ValueError("source phase must match the previous state")
        if state.phase is not request.to_phase:
            raise ValueError("target phase must match the request")
        if (
            state.objective_id != previous.objective_id
            or state.scope != previous.scope
        ):
            raise ValueError("transition must preserve objective and scope")

        if set(previous.resource_links).intersection(request.resource_links):
            raise ValueError("requested links must be new additions")
        expected_links = tuple(sorted(
            previous.resource_links + request.resource_links,
            key=lambda link: (
                link.relationship, link.resource_type, link.resource_id,
            ),
        ))
        if state.resource_links != expected_links:
            raise ValueError("result must retain previous links and exact additions")
