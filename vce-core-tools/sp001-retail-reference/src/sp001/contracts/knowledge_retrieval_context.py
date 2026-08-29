from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeSourceScope,
)


class KnowledgeScopeMatchStatus(StrEnum):
    """Deterministic outcome of source-scope comparison."""

    MATCHES = "MATCHES"
    DOES_NOT_MATCH = "DOES_NOT_MATCH"


class KnowledgeScopeMismatchReason(StrEnum):
    """Exact dimensions preventing source-scope applicability."""

    ORGANIZATION_MISMATCH = "ORGANIZATION_MISMATCH"
    CUSTOMER_MISMATCH = "CUSTOMER_MISMATCH"
    JURISDICTION_MISMATCH = "JURISDICTION_MISMATCH"
    COMMERCIAL_CHANNEL_MISMATCH = (
        "COMMERCIAL_CHANNEL_MISMATCH"
    )
    DOCUMENT_TYPE_MISMATCH = "DOCUMENT_TYPE_MISMATCH"
    POINT_OF_SALE_MISMATCH = "POINT_OF_SALE_MISMATCH"
    DEPARTMENT_MISMATCH = "DEPARTMENT_MISMATCH"
    CAMPAIGN_MISMATCH = "CAMPAIGN_MISMATCH"


@dataclass(frozen=True, slots=True)
class KnowledgeRetrievalContext:
    """Explicit retail context and evaluation instant for retrieval."""

    organization_id: str
    customer_id: str
    jurisdiction: str
    commercial_channel_id: str
    document_type: KnowledgeDocumentType
    point_of_sale_id: str
    department_id: str
    campaign_id: str | None
    evaluated_at: datetime

    def __post_init__(self) -> None:
        identity_fields = {
            "organization_id": self.organization_id,
            "customer_id": self.customer_id,
            "jurisdiction": self.jurisdiction,
            "commercial_channel_id": (
                self.commercial_channel_id
            ),
            "point_of_sale_id": self.point_of_sale_id,
            "department_id": self.department_id,
        }

        for field, identity in identity_fields.items():
            if (
                not isinstance(identity, str)
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must not be empty"
                )

        if not isinstance(
            self.document_type,
            KnowledgeDocumentType,
        ):
            raise TypeError(
                "document_type must be a "
                "KnowledgeDocumentType"
            )

        if (
            self.campaign_id is not None
            and (
                not isinstance(self.campaign_id, str)
                or not self.campaign_id.strip()
            )
        ):
            raise ValueError(
                "campaign_id must not be empty when declared"
            )

        if not isinstance(self.evaluated_at, datetime):
            raise TypeError(
                "evaluated_at must be a datetime"
            )

        if (
            self.evaluated_at.tzinfo is None
            or self.evaluated_at.utcoffset() is None
        ):
            raise ValueError(
                "evaluated_at must be timezone-aware"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeSourceScopeEvaluation:
    """Auditable scope comparison without retrieval decision claims."""

    source_scope: KnowledgeSourceScope
    retrieval_context: KnowledgeRetrievalContext
    match_status: KnowledgeScopeMatchStatus
    mismatch_reasons: tuple[
        KnowledgeScopeMismatchReason,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.source_scope,
            KnowledgeSourceScope,
        ):
            raise TypeError(
                "source_scope must be a KnowledgeSourceScope"
            )

        if not isinstance(
            self.retrieval_context,
            KnowledgeRetrievalContext,
        ):
            raise TypeError(
                "retrieval_context must be a "
                "KnowledgeRetrievalContext"
            )

        if not isinstance(
            self.match_status,
            KnowledgeScopeMatchStatus,
        ):
            raise TypeError(
                "match_status must be a "
                "KnowledgeScopeMatchStatus"
            )

        if not isinstance(self.mismatch_reasons, tuple):
            raise TypeError(
                "mismatch_reasons must be an immutable tuple"
            )

        seen_reasons: set[
            KnowledgeScopeMismatchReason
        ] = set()

        for reason in self.mismatch_reasons:
            if not isinstance(
                reason,
                KnowledgeScopeMismatchReason,
            ):
                raise TypeError(
                    "mismatch_reasons must contain "
                    "KnowledgeScopeMismatchReason values"
                )

            if reason in seen_reasons:
                raise ValueError(
                    f"duplicate mismatch reason: {reason}"
                )

            seen_reasons.add(reason)

        if (
            self.match_status
            is KnowledgeScopeMatchStatus.MATCHES
            and self.mismatch_reasons
        ):
            raise ValueError(
                "MATCHES evaluation cannot contain "
                "mismatch reasons"
            )

        if (
            self.match_status
            is KnowledgeScopeMatchStatus.DOES_NOT_MATCH
            and not self.mismatch_reasons
        ):
            raise ValueError(
                "DOES_NOT_MATCH evaluation requires "
                "at least one mismatch reason"
            )
