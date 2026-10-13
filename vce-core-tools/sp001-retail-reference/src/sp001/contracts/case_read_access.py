from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    """Identity attributed by an authenticator, without implicit permissions.

    Constructing this value does not itself authenticate a credential.
    """

    issuer: str
    subject: str

    def __post_init__(self) -> None:
        for field in ("issuer", "subject"):
            value = getattr(self, field)
            if not isinstance(value, str):
                raise TypeError(f"{field} must be a string")
            if not value.strip():
                raise ValueError(f"{field} must not be empty")


@runtime_checkable
class CaseReadAuthenticator(Protocol):
    def authenticate(
        self,
        *,
        credential: str,
    ) -> AuthenticatedPrincipal | None:
        """Return validated identity, or None for rejected credentials.

        Provider failures must raise, not masquerade as credential rejection.
        """
        ...


@runtime_checkable
class CaseReadAuthorizer(Protocol):
    def can_read_case(
        self,
        *,
        principal: AuthenticatedPrincipal,
        case_id: str,
    ) -> bool:
        """Authorize this exact identity to read this exact case.

        Return an exact bool. Do not consult case existence to grant access.
        """
        ...
