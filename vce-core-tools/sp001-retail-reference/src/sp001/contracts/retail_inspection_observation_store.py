from dataclasses import dataclass
from typing import Protocol, runtime_checkable


def _text(name: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True)
class RetailInspectionObservationIdentity:
    """Exact observation version within one store namespace."""

    observation_id: str
    observation_version: int

    def __post_init__(self) -> None:
        _text("observation_id", self.observation_id)
        if type(self.observation_version) is not int:
            raise TypeError("observation_version must be an integer")
        if self.observation_version < 1:
            raise ValueError("observation_version must be positive")


@dataclass(frozen=True, slots=True)
class StoredRetailInspectionObservation:
    """Opaque exact document; construction proves no durable storage."""

    identity: RetailInspectionObservationIdentity
    document: str

    def __post_init__(self) -> None:
        if not isinstance(self.identity, RetailInspectionObservationIdentity):
            raise TypeError("identity must be an observation identity")
        _text("document", self.document)


class RetailInspectionObservationConflict(RuntimeError):
    """The exact observation identity/version has different stored content."""


@runtime_checkable
class RetailInspectionObservationStore(Protocol):
    """Append-only port for exact versioned documents.

    Adapters must enforce identity/version uniqueness atomically.
    No update or deletion operation is offered.
    Versions are independent positive keys: this port does not enforce
    consecutive versions, stable cross-version fields or current-version
    selection. A higher number does not establish approval or authority.

    Schema validation and agreement between document and identity belong
    to the caller's codec boundary. Infrastructure failures propagate.
    This port performs no authentication or authorization.
    """

    def put(
        self, *, observation: StoredRetailInspectionObservation,
    ) -> StoredRetailInspectionObservation:
        """Confirm storage or return the identical existing record.

        Different document text under the same exact identity/version
        raises RetailInspectionObservationConflict without replacement.
        Adding another version must preserve all existing versions.
        A successful return confirms persistence; an exception may leave
        the outcome unknown. Recover by exact identity before retrying.
        """
        ...

    def get(
        self, *, identity: RetailInspectionObservationIdentity,
    ) -> StoredRetailInspectionObservation | None:
        """Return that exact version; None only for absence, never failure."""
        ...
