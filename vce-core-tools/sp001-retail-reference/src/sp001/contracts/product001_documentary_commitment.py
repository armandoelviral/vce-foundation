"""PRODUCT-001 documentary commitment facts without admission authority."""

from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)


@dataclass(frozen=True, slots=True)
class Product001DocumentaryCommitmentKey:
    """Organization-scoped documentary identity.

    The source digest is retained for verification, but must not
    participate in the exclusive storage-path identity.
    """

    organization_id: str
    source_identity: KnowledgeSourceIdentity

    def __post_init__(self) -> None:
        if (
            not isinstance(self.organization_id, str)
            or not self.organization_id.strip()
        ):
            raise ValueError("organization_id must be nonempty")

        if not isinstance(
            self.source_identity,
            KnowledgeSourceIdentity,
        ):
            raise TypeError(
                "source_identity must be a KnowledgeSourceIdentity"
            )

    @property
    def exclusive_identity(self) -> tuple[str, str, str]:
        return (
            self.organization_id,
            self.source_identity.source_id,
            self.source_identity.source_version,
        )


class Product001DocumentaryCommitmentStatus(StrEnum):
    CREATED = "CREATED"
    ALREADY_PRESENT = "ALREADY_PRESENT"


@dataclass(frozen=True, slots=True)
class Product001DocumentaryCommitmentResult:
    """Positive local commitment fact; never documentary admission."""

    key: Product001DocumentaryCommitmentKey
    status: Product001DocumentaryCommitmentStatus
    bytes_committed: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.key,
            Product001DocumentaryCommitmentKey,
        ):
            raise TypeError(
                "key must be a Product001DocumentaryCommitmentKey"
            )

        if not isinstance(
            self.status,
            Product001DocumentaryCommitmentStatus,
        ):
            raise TypeError(
                "status must be a Product001DocumentaryCommitmentStatus"
            )

        if (
            type(self.bytes_committed) is not int
            or self.bytes_committed < 0
        ):
            raise ValueError(
                "bytes_committed must be a nonnegative integer"
            )
