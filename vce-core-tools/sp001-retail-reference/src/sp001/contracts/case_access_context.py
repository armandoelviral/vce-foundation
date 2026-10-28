from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable

from sp001.contracts.case_read_access import AuthenticatedPrincipal


class CaseAccessOperation(StrEnum):
    READ_STATE = "READ_STATE"
    SUBSCRIBE_EVENTS = "SUBSCRIBE_EVENTS"
    OPEN_CASE = "OPEN_CASE"
    APPLY_CASE_TRANSITION = "APPLY_CASE_TRANSITION"
    READ_LIFECYCLE_RESULT = "READ_LIFECYCLE_RESULT"
    SAVE_RETAIL_REPORT = "SAVE_RETAIL_REPORT"
    READ_RETAIL_REPORT = "READ_RETAIL_REPORT"
    SAVE_RETAIL_OBSERVATION = "SAVE_RETAIL_OBSERVATION"
    READ_RETAIL_OBSERVATION = "READ_RETAIL_OBSERVATION"


@dataclass(frozen=True, slots=True)
class CaseAccessPermission:
    case_id: str
    operation: CaseAccessOperation

    def __post_init__(self) -> None:
        if not isinstance(self.case_id, str):
            raise TypeError("case_id must be a string")
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty")
        if not isinstance(self.operation, CaseAccessOperation):
            raise TypeError("operation must be a CaseAccessOperation")


@dataclass(frozen=True, slots=True)
class ValidatedCaseAccessContext:
    """Claims attributed by a verifier; construction verifies no signature.

    Time values are integer Unix seconds. Audience and permissions are exact.
    """

    principal: AuthenticatedPrincipal
    audience: str
    issued_at: int
    not_before: int
    expires_at: int
    permissions: tuple[CaseAccessPermission, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.principal, AuthenticatedPrincipal):
            raise TypeError("principal must be an AuthenticatedPrincipal")
        if not isinstance(self.audience, str):
            raise TypeError("audience must be a string")
        if not self.audience.strip():
            raise ValueError("audience must not be empty")
        for name in ("issued_at", "not_before", "expires_at"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be integer Unix seconds")
            if value < 0:
                raise ValueError(f"{name} must not be negative")
        if not self.issued_at <= self.not_before < self.expires_at:
            raise ValueError("invalid validity interval")
        if not isinstance(self.permissions, tuple):
            raise TypeError("permissions must be a tuple")
        if any(
            not isinstance(permission, CaseAccessPermission)
            for permission in self.permissions
        ):
            raise TypeError("permissions must contain CaseAccessPermission")
        if len(set(self.permissions)) != len(self.permissions):
            raise ValueError("permissions must be unique")


@runtime_checkable
class CaseAccessContextAuthenticator(Protocol):
    def authenticate(
        self, *, credential: str
    ) -> ValidatedCaseAccessContext | None:
        """Verify credential and return its access context or explicit rejection."""
        ...


@runtime_checkable
class CaseAccessContextAuthorizer(Protocol):
    def can_read_case(
        self, *, access: ValidatedCaseAccessContext, case_id: str
    ) -> bool:
        """Evaluate validated access and any additional current access policy."""
        ...
