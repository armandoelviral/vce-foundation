from __future__ import annotations

from dataclasses import dataclass


VALID_STATES = frozenset(
    {
        "Available",
        "Missing",
        "Invalid",
    }
)


@dataclass(frozen=True, slots=True)
class Evidence:
    """
    Immutable evidence produced by an
    executable verification process.
    """

    source: str

    status: str

    def __post_init__(self) -> None:
        if self.status not in VALID_STATES:
            raise ValueError(
                f"Invalid evidence status: {self.status}"
            )

    @property
    def available(self) -> bool:
        return self.status == "Available"
