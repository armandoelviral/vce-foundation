from dataclasses import dataclass
from typing import ClassVar

from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_resource_link import CaseResourceLink


def _text(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


def _links(value):
    if not isinstance(value, tuple):
        raise TypeError("resource_links must be a tuple")
    if any(not isinstance(link, CaseResourceLink) for link in value):
        raise TypeError("resource_links must contain CaseResourceLink values")
    keys = tuple(
        (link.relationship, link.resource_type, link.resource_id)
        for link in value
    )
    if len(set(keys)) != len(keys):
        raise ValueError("resource_links must be unique")
    if keys != tuple(sorted(keys)):
        raise ValueError("resource_links must use canonical order")


@dataclass(frozen=True, slots=True)
class CaseOpeningRequest:
    """Exact generic opening intent; no persistence or authorization."""

    schema_version: ClassVar[int] = 1
    operation: ClassVar[str] = "OPEN_CASE"

    transition_id: str
    case_id: str
    objective_id: str
    scope: str
    resource_links: tuple[CaseResourceLink, ...] = ()

    def __post_init__(self):
        for name in ("transition_id", "case_id", "objective_id"):
            _text(getattr(self, name), name)
        if not isinstance(self.scope, str):
            raise TypeError("scope must be a string")
        _links(self.resource_links)


@dataclass(frozen=True, slots=True)
class CaseTransitionRequest:
    """Exact transition intent; links are additions, not accumulated state."""

    schema_version: ClassVar[int] = 1
    operation: ClassVar[str] = "APPLY_CASE_TRANSITION"

    transition_id: str
    case_id: str
    expected_revision: int
    to_phase: CaseLifecyclePhase
    resource_links: tuple[CaseResourceLink, ...] = ()

    def __post_init__(self):
        for name in ("transition_id", "case_id"):
            _text(getattr(self, name), name)
        if (
            isinstance(self.expected_revision, bool)
            or not isinstance(self.expected_revision, int)
        ):
            raise TypeError("expected_revision must be an integer")
        if not 1 <= self.expected_revision < (1 << 64) - 1:
            raise ValueError("expected_revision must admit a uint64 successor")
        if not isinstance(self.to_phase, CaseLifecyclePhase):
            raise TypeError("to_phase must be a CaseLifecyclePhase")
        _links(self.resource_links)
