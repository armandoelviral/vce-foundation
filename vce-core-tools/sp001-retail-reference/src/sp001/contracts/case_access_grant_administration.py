from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_read_access import AuthenticatedPrincipal


class GrantAdministrationAction(StrEnum):
    GRANT = "GRANT"
    REVOKE = "REVOKE"


@dataclass(frozen=True, slots=True)
class GrantAdministrationRecord:
    event_id: str
    actor: AuthenticatedPrincipal
    action: GrantAdministrationAction
    grant: CaseAccessGrant
    recorded_at: int

    def __post_init__(self) -> None:
        if not isinstance(self.event_id, str):
            raise TypeError("event_id must be a string")
        if not self.event_id.strip():
            raise ValueError("event_id must not be empty")
        if not isinstance(self.actor, AuthenticatedPrincipal):
            raise TypeError("actor must be an AuthenticatedPrincipal")
        if not isinstance(self.action, GrantAdministrationAction):
            raise TypeError("action must be a GrantAdministrationAction")
        if not isinstance(self.grant, CaseAccessGrant):
            raise TypeError("grant must be a CaseAccessGrant")
        if isinstance(self.recorded_at, bool) or not isinstance(self.recorded_at, int):
            raise TypeError("recorded_at must be integer Unix seconds")
        if self.recorded_at < 0:
            raise ValueError("recorded_at must not be negative")


@runtime_checkable
class CaseGrantAdministrationPolicy(Protocol):
    def may_administer(
        self,
        *,
        actor: AuthenticatedPrincipal,
        action: GrantAdministrationAction,
        grant: CaseAccessGrant,
    ) -> bool:
        """Authorize the exact administrative action and target grant."""
        ...


@runtime_checkable
class CaseAccessGrantAdministrationStore(Protocol):
    def apply(self, *, record: GrantAdministrationRecord) -> bool:
        """Atomically persist mutation and audit record.

        Exact event replay returns True without another mutation.
        Conflicting event IDs or grant definitions must raise.
        Revoking an unknown grant returns False.
        Revocation is immediate and irreversible for this grant ID.
        Permission reads exclude revoked grants, including historical at_time.
        This port is a trusted storage capability, not an authorization gate.
        """
        ...
