from sp001.contracts.case_lifecycle_completion import CaseLifecycleCompletion
from sp001.contracts.case_lifecycle_execution_store import (
    CaseLifecycleRequestConflict,
)
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)


def match_case_lifecycle_completion(
    *,
    request: CaseOpeningRequest | CaseTransitionRequest,
    completion: CaseLifecycleCompletion | None,
) -> CaseLifecycleCompletion | None:
    """Check an already-read completion; no storage, authorization or mutation."""
    if type(request) not in (CaseOpeningRequest, CaseTransitionRequest):
        raise TypeError("request must be an exact lifecycle request")
    if completion is None:
        return None
    if type(completion) is not CaseLifecycleCompletion:
        raise TypeError("completion must be a CaseLifecycleCompletion or None")
    if completion.request.transition_id != request.transition_id:
        raise ValueError("retrieved completion has a different transition identity")
    if completion.request != request:
        raise CaseLifecycleRequestConflict(
            "transition identity is bound to a different lifecycle request"
        )
    return completion
