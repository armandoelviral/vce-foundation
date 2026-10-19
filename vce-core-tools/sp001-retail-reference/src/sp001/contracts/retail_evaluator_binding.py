from dataclasses import dataclass

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_process_actor import RetailProcessActor


@dataclass(frozen=True, slots=True)
class RetailEvaluatorBinding:
    """Declared principal-to-actor association scoped to one exact case.

    Construction authenticates nobody and grants no case permission.
    Validity applies to attribution admission, not the asserted inspection time.
    """

    binding_id: str
    revision: int
    principal: AuthenticatedPrincipal
    actor: RetailProcessActor
    case_id: str
    valid_from: int
    expires_at: int

    def __post_init__(self) -> None:
        for name in ("binding_id", "case_id"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if type(self.revision) is not int:
            raise TypeError("revision must be an integer")
        if self.revision < 1:
            raise ValueError("revision must be positive")
        if not isinstance(self.principal, AuthenticatedPrincipal):
            raise TypeError("principal must be an AuthenticatedPrincipal")
        if not isinstance(self.actor, RetailProcessActor):
            raise TypeError("actor must be a RetailProcessActor")

        for name in ("valid_from", "expires_at"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be integer Unix seconds")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative")
        if self.valid_from >= self.expires_at:
            raise ValueError("binding validity interval must be nonempty")


@dataclass(frozen=True, slots=True)
class RetailEvaluatorBindingSnapshot:
    """Supplied binding state; does not establish freshness or persistence."""

    binding: RetailEvaluatorBinding
    revoked: bool

    def __post_init__(self) -> None:
        if not isinstance(self.binding, RetailEvaluatorBinding):
            raise TypeError("binding must be a RetailEvaluatorBinding")
        if type(self.revoked) is not bool:
            raise TypeError("revoked must be an exact bool")
