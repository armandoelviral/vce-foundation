"""Local documentary reading facts without admission authority."""

from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)


class Product001DocumentaryCommitmentReadStatus(StrEnum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    CONFLICT = "CONFLICT"
    INVALID = "INVALID"
    IO_FAILURE = "IO_FAILURE"


@dataclass(frozen=True, slots=True)
class Product001DocumentaryCommitmentReadResult:
    key: Product001DocumentaryCommitmentKey
    status: Product001DocumentaryCommitmentReadStatus
    content: bytes | None = None

    def __post_init__(self) -> None:
        if not isinstance(
            self.key,
            Product001DocumentaryCommitmentKey,
        ):
            raise TypeError("invalid documentary reading key")

        if not isinstance(
            self.status,
            Product001DocumentaryCommitmentReadStatus,
        ):
            raise TypeError("invalid documentary reading status")

        if self.status is Product001DocumentaryCommitmentReadStatus.PRESENT:
            if type(self.content) is not bytes:
                raise TypeError("PRESENT requires bytes content")
        elif self.content is not None:
            raise ValueError(
                "non-PRESENT reading cannot carry content"
            )
