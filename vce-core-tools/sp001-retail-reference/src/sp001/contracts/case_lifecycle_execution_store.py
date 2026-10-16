from typing import Protocol, runtime_checkable

from sp001.contracts.case_lifecycle_completion import CaseLifecycleCompletion
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)


class CaseLifecycleRequestConflict(RuntimeError):
    """A transition identity is already bound to a different request."""


@runtime_checkable
class CaseLifecycleExecutionStore(Protocol):
    """Atomic execution and exact-result recovery port.

    No authentication or authorization is supplied by this port.
    The trusted caller must establish the required access boundary.
    """

    def execute(
        self,
        *,
        request: CaseOpeningRequest | CaseTransitionRequest,
        write_deadline_ns: int | None = None,
    ) -> CaseLifecycleCompletion | None:
        """Execute or recover the exact request.

        Persist request, state, transition and completion atomically.
        An existing exact completion is returned without another mutation.
        Reused identity with different content raises CaseLifecycleRequestConflict.
        None means this attempt was not applied due to current state conflict
        or absence; it is not a durable cancellation record.

        A supplied deadline uses the process-local perf_counter_ns domain.
        It does not guarantee interruption of blocking calls. Errors must not
        be interpreted as proof that no commit occurred.
        """
        ...

    def recover(
        self,
        *,
        request: CaseOpeningRequest | CaseTransitionRequest,
    ) -> CaseLifecycleCompletion | None:
        """Return the original completion only for the exact request.

        Same identity with different content raises CaseLifecycleRequestConflict.
        None means no completion was observed at this read, not cancellation.
        A later case revision must not replace the original result.
        """
        ...
