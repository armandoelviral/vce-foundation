from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import CaseAccessPermission


@dataclass(frozen=True, slots=True)
class CaseAccessGrant:
    """Configured grant; construction establishes no administrative authority."""

    grant_id: str
    principal: AuthenticatedPrincipal
    permission: CaseAccessPermission
    valid_from: int
    expires_at: int

    def __post_init__(self) -> None:
        if not isinstance(self.grant_id, str):
            raise TypeError("grant_id must be a string")
        if not self.grant_id.strip():
            raise ValueError("grant_id must not be empty")
        if not isinstance(self.principal, AuthenticatedPrincipal):
            raise TypeError("principal must be an AuthenticatedPrincipal")
        if not isinstance(self.permission, CaseAccessPermission):
            raise TypeError("permission must be a CaseAccessPermission")
        for name in ("valid_from", "expires_at"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be integer Unix seconds")
            if value < 0:
                raise ValueError(f"{name} must not be negative")
        if self.valid_from >= self.expires_at:
            raise ValueError("grant validity interval must be nonempty")


@runtime_checkable
class CaseAccessGrantSource(Protocol):
    def permits(
        self,
        *,
        principal: AuthenticatedPrincipal,
        permission: CaseAccessPermission,
        at_time: int,
    ) -> bool:
        """Check exact identity and permission at the supplied Unix second."""
        ...
