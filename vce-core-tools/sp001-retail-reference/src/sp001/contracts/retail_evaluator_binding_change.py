from dataclasses import dataclass

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBindingSnapshot,
)


@dataclass(frozen=True, slots=True)
class RetailEvaluatorBindingChange:
    """Declared administrative occurrence; construction grants no authority."""

    event_id: str
    snapshot: RetailEvaluatorBindingSnapshot
    administrator: AuthenticatedPrincipal
    recorded_at: int

    def __post_init__(self) -> None:
        if not isinstance(self.event_id, str):
            raise TypeError("event_id must be a string")
        if not self.event_id.strip():
            raise ValueError("event_id must not be empty")
        if not isinstance(self.snapshot, RetailEvaluatorBindingSnapshot):
            raise TypeError("snapshot must be a RetailEvaluatorBindingSnapshot")
        if not isinstance(self.administrator, AuthenticatedPrincipal):
            raise TypeError("administrator must be an AuthenticatedPrincipal")
        if type(self.recorded_at) is not int:
            raise TypeError("recorded_at must be integer Unix seconds")
        if self.recorded_at < 0:
            raise ValueError("recorded_at must be nonnegative")
