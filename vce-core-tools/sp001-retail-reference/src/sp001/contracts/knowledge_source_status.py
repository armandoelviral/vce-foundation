from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeSourceScope,
)


class KnowledgeLifecycleStatus(StrEnum):
    """Editorial lifecycle status without authority implications."""

    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REVOKED = "REVOKED"
    ARCHIVED = "ARCHIVED"


class KnowledgeEvidenceStatus(StrEnum):
    """Declared evidence assessment kept separate from lifecycle."""

    NOT_ASSESSED = "NOT_ASSESSED"
    SUPPORTED = "SUPPORTED"
    DISPUTED = "DISPUTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True, slots=True)
class KnowledgeSourceStatus:
    """Versioned lifecycle and evidence declaration for one scoped source."""

    status_record_id: str
    status_version: int
    identity: KnowledgeSourceIdentity
    scope: KnowledgeSourceScope
    lifecycle_status: KnowledgeLifecycleStatus
    evidence_status: KnowledgeEvidenceStatus

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.status_record_id,
                str,
            )
            or not self.status_record_id.strip()
        ):
            raise ValueError(
                "status_record_id must not be empty"
            )

        if (
            isinstance(
                self.status_version,
                bool,
            )
            or not isinstance(
                self.status_version,
                int,
            )
            or self.status_version < 1
        ):
            raise ValueError(
                "status_version must be a positive integer"
            )

        if not isinstance(
            self.identity,
            KnowledgeSourceIdentity,
        ):
            raise TypeError(
                "identity must be a KnowledgeSourceIdentity"
            )

        if not isinstance(
            self.scope,
            KnowledgeSourceScope,
        ):
            raise TypeError(
                "scope must be a KnowledgeSourceScope"
            )

        if not isinstance(
            self.lifecycle_status,
            KnowledgeLifecycleStatus,
        ):
            raise TypeError(
                "lifecycle_status must be a "
                "KnowledgeLifecycleStatus"
            )

        if not isinstance(
            self.evidence_status,
            KnowledgeEvidenceStatus,
        ):
            raise TypeError(
                "evidence_status must be a "
                "KnowledgeEvidenceStatus"
            )
