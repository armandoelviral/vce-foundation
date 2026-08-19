from dataclasses import dataclass
from enum import StrEnum


class DependencySourceType(StrEnum):
    """Declared type of a retail rule derivation source."""

    RULE = "RULE"
    CONTEXT_POLICY = "CONTEXT_POLICY"


@dataclass(frozen=True, slots=True)
class RetailContextDependencySource:
    """Immutable, explicitly typed dependency source."""

    source_id: str
    source_type: DependencySourceType

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.source_id,
                str,
            )
            or not self.source_id.strip()
        ):
            raise ValueError(
                "source_id must not be empty"
            )

        if not isinstance(
            self.source_type,
            DependencySourceType,
        ):
            raise TypeError(
                "source_type must be a "
                "DependencySourceType"
            )
