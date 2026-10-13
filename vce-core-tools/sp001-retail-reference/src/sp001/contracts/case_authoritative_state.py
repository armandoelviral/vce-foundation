from dataclasses import dataclass

from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_resource_link import CaseResourceLink


_UINT64_MAX = (1 << 64) - 1


@dataclass(frozen=True, slots=True)
class CaseAuthoritativeState:
    """Versioned current-state snapshot for one case."""

    case_id: str
    objective_id: str
    scope: str
    phase: CaseLifecyclePhase
    revision: int
    resource_links: tuple[CaseResourceLink, ...]

    def __post_init__(self) -> None:
        for field_name in ("case_id", "objective_id"):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string")
            if not value.strip():
                raise ValueError(f"{field_name} must not be empty")

        if not isinstance(self.scope, str):
            raise TypeError("scope must be a string")

        if not isinstance(self.phase, CaseLifecyclePhase):
            raise TypeError("phase must be a CaseLifecyclePhase")

        if (
            isinstance(self.revision, bool)
            or not isinstance(self.revision, int)
        ):
            raise TypeError("revision must be an integer")
        if self.revision < 1 or self.revision > _UINT64_MAX:
            raise ValueError("revision must be a positive uint64")

        if not isinstance(self.resource_links, tuple):
            raise TypeError("resource_links must be a tuple")
        if any(
            not isinstance(link, CaseResourceLink)
            for link in self.resource_links
        ):
            raise TypeError(
                "resource_links must contain only CaseResourceLink values"
            )

        keys = tuple(
            (link.relationship, link.resource_type, link.resource_id)
            for link in self.resource_links
        )
        if len(set(keys)) != len(keys):
            raise ValueError("resource_links must be unique")
        if keys != tuple(sorted(keys)):
            raise ValueError("resource_links must use canonical order")
