from dataclasses import dataclass

from sp001.contracts.case_access_context import CaseAccessPermission
from sp001.contracts.case_read_access import AuthenticatedPrincipal


def _text(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


def _integer(value: object, name: str, minimum: int = 0) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} is below its minimum")


@dataclass(frozen=True, slots=True)
class FederatedPrincipalBinding:
    """Declared identity association; construction establishes no authority."""

    binding_id: str
    revision: int
    external_principal: AuthenticatedPrincipal
    internal_subject: str

    def __post_init__(self) -> None:
        _text(self.binding_id, "binding_id")
        _integer(self.revision, "revision", 1)
        if not isinstance(self.external_principal, AuthenticatedPrincipal):
            raise TypeError("external_principal must be an AuthenticatedPrincipal")
        _text(self.internal_subject, "internal_subject")


@dataclass(frozen=True, slots=True)
class IssuanceGrantReference:
    """Reference to a grant revision used to authorize one permission."""

    grant_id: str
    revision: int
    permission: CaseAccessPermission
    expires_at: int

    def __post_init__(self) -> None:
        _text(self.grant_id, "grant_id")
        _integer(self.revision, "revision", 1)
        if not isinstance(self.permission, CaseAccessPermission):
            raise TypeError("permission must be a CaseAccessPermission")
        _integer(self.expires_at, "expires_at")


@dataclass(frozen=True, slots=True)
class CaseAccessTokenPayload:
    issuer: str
    subject: str
    audience: str
    issued_at: int
    not_before: int
    expires_at: int
    token_id: str
    permissions: tuple[CaseAccessPermission, ...]

    def __post_init__(self) -> None:
        for name in ("issuer", "subject", "audience", "token_id"):
            _text(getattr(self, name), name)
        for name in ("issued_at", "not_before", "expires_at"):
            _integer(getattr(self, name), name)
        if not self.issued_at <= self.not_before < self.expires_at:
            raise ValueError("invalid token validity interval")
        if not isinstance(self.permissions, tuple) or not self.permissions:
            raise ValueError("permissions must be a nonempty tuple")
        if any(not isinstance(value, CaseAccessPermission) for value in self.permissions):
            raise TypeError("permissions must contain CaseAccessPermission")
        keys = tuple(
            (value.case_id, value.operation.value) for value in self.permissions
        )
        if len(set(keys)) != len(keys):
            raise ValueError("permissions must be unique")
        if keys != tuple(sorted(keys)):
            raise ValueError("permissions must use canonical order")

    def to_claims(self) -> dict:
        return {
            "iss": self.issuer,
            "sub": self.subject,
            "aud": self.audience,
            "iat": self.issued_at,
            "nbf": self.not_before,
            "exp": self.expires_at,
            "jti": self.token_id,
            "sp001_profile": "case-access.v1",
            "case_permissions": [
                {"case_id": value.case_id, "operation": value.operation.value}
                for value in self.permissions
            ],
        }


@dataclass(frozen=True, slots=True)
class CaseAccessIssuancePreparation:
    request_id: str
    binding: FederatedPrincipalBinding
    payload: CaseAccessTokenPayload
    signing_key_id: str
    grant_references: tuple[IssuanceGrantReference, ...]

    def __post_init__(self) -> None:
        _text(self.request_id, "request_id")
        _text(self.signing_key_id, "signing_key_id")
        if not isinstance(self.binding, FederatedPrincipalBinding):
            raise TypeError("binding must be a FederatedPrincipalBinding")
        if not isinstance(self.payload, CaseAccessTokenPayload):
            raise TypeError("payload must be a CaseAccessTokenPayload")
        if self.payload.subject != self.binding.internal_subject:
            raise ValueError("payload subject must match the bound internal subject")
        if not isinstance(self.grant_references, tuple) or not self.grant_references:
            raise ValueError("grant_references must be a nonempty tuple")
        if any(
            not isinstance(value, IssuanceGrantReference)
            for value in self.grant_references
        ):
            raise TypeError("grant_references must contain IssuanceGrantReference")
        grant_ids = tuple(value.grant_id for value in self.grant_references)
        if len(set(grant_ids)) != len(grant_ids):
            raise ValueError("grant references must use unique grant IDs")
        if grant_ids != tuple(sorted(grant_ids)):
            raise ValueError("grant references must use canonical order")
        covered = {value.permission for value in self.grant_references}
        if covered != set(self.payload.permissions):
            raise ValueError("grant references must cover exactly the emitted permissions")
        if any(
            self.payload.expires_at > value.expires_at
            for value in self.grant_references
        ):
            raise ValueError("token must not outlive its referenced grants")
