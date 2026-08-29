from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
    KnowledgeSourceScopeEvaluation,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceTemporalEvaluation,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeSourceStatus,
)


class KnowledgeRetrievalDecisionStatus(StrEnum):
    """Technical source inclusion outcome."""

    INCLUDED = "INCLUDED"
    EXCLUDED = "EXCLUDED"


class KnowledgeRetrievalExclusionReason(StrEnum):
    """Independent technical reasons preventing source inclusion."""

    CONTENT_BYTES_MISMATCH = "CONTENT_BYTES_MISMATCH"
    SCOPE_MISMATCH = "SCOPE_MISMATCH"
    LIFECYCLE_NOT_APPROVED = "LIFECYCLE_NOT_APPROVED"
    EVIDENCE_NOT_SUPPORTED = "EVIDENCE_NOT_SUPPORTED"
    TEMPORALLY_INACTIVE = "TEMPORALLY_INACTIVE"
    NO_VERIFIED_AUTHORITY_BINDING = (
        "NO_VERIFIED_AUTHORITY_BINDING"
    )
    SOURCE_SUPERSEDED = "SOURCE_SUPERSEDED"


@dataclass(frozen=True, slots=True)
class KnowledgeSourceRetrievalDecision:
    """Auditable technical decision without truth or relevance claims."""

    source_status: KnowledgeSourceStatus
    retrieval_context: KnowledgeRetrievalContext
    content_bytes_match_digest: bool
    scope_evaluation: KnowledgeSourceScopeEvaluation
    temporal_evaluation: KnowledgeSourceTemporalEvaluation
    verified_authority_binding_ids: tuple[str, ...]
    supersession_ids: tuple[str, ...]
    decision_status: KnowledgeRetrievalDecisionStatus
    exclusion_reasons: tuple[
        KnowledgeRetrievalExclusionReason,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.source_status,
            KnowledgeSourceStatus,
        ):
            raise TypeError(
                "source_status must be a KnowledgeSourceStatus"
            )

        if not isinstance(
            self.retrieval_context,
            KnowledgeRetrievalContext,
        ):
            raise TypeError(
                "retrieval_context must be a "
                "KnowledgeRetrievalContext"
            )

        if type(self.content_bytes_match_digest) is not bool:
            raise TypeError(
                "content_bytes_match_digest must be a boolean"
            )

        if not isinstance(
            self.scope_evaluation,
            KnowledgeSourceScopeEvaluation,
        ):
            raise TypeError(
                "scope_evaluation must be a "
                "KnowledgeSourceScopeEvaluation"
            )

        if not isinstance(
            self.temporal_evaluation,
            KnowledgeSourceTemporalEvaluation,
        ):
            raise TypeError(
                "temporal_evaluation must be a "
                "KnowledgeSourceTemporalEvaluation"
            )

        if (
            self.scope_evaluation.source_scope
            != self.source_status.scope
        ):
            raise ValueError(
                "scope evaluation must describe source status"
            )

        if (
            self.scope_evaluation.retrieval_context
            != self.retrieval_context
        ):
            raise ValueError(
                "scope evaluation must use retrieval context"
            )

        if (
            self.temporal_evaluation.effective_period.source_status
            != self.source_status
        ):
            raise ValueError(
                "temporal evaluation must describe source status"
            )

        if (
            self.temporal_evaluation.evaluated_at
            != self.retrieval_context.evaluated_at
        ):
            raise ValueError(
                "temporal evaluation must use retrieval instant"
            )

        self._validate_identifiers(
            field="verified_authority_binding_ids",
            values=self.verified_authority_binding_ids,
        )
        self._validate_identifiers(
            field="supersession_ids",
            values=self.supersession_ids,
        )

        if not isinstance(
            self.decision_status,
            KnowledgeRetrievalDecisionStatus,
        ):
            raise TypeError(
                "decision_status must be a "
                "KnowledgeRetrievalDecisionStatus"
            )

        if not isinstance(self.exclusion_reasons, tuple):
            raise TypeError(
                "exclusion_reasons must be an immutable tuple"
            )

        seen_reasons: set[
            KnowledgeRetrievalExclusionReason
        ] = set()

        for reason in self.exclusion_reasons:
            if not isinstance(
                reason,
                KnowledgeRetrievalExclusionReason,
            ):
                raise TypeError(
                    "exclusion_reasons must contain "
                    "KnowledgeRetrievalExclusionReason values"
                )

            if reason in seen_reasons:
                raise ValueError(
                    f"duplicate exclusion reason: {reason}"
                )

            seen_reasons.add(reason)

        if (
            self.decision_status
            is KnowledgeRetrievalDecisionStatus.INCLUDED
            and self.exclusion_reasons
        ):
            raise ValueError(
                "INCLUDED decision cannot contain "
                "exclusion reasons"
            )

        if (
            self.decision_status
            is KnowledgeRetrievalDecisionStatus.EXCLUDED
            and not self.exclusion_reasons
        ):
            raise ValueError(
                "EXCLUDED decision requires "
                "at least one exclusion reason"
            )

    @staticmethod
    def _validate_identifiers(
        *,
        field: str,
        values: object,
    ) -> None:
        if not isinstance(values, tuple):
            raise TypeError(
                f"{field} must be an immutable tuple"
            )

        seen: set[str] = set()

        for identity in values:
            if (
                not isinstance(identity, str)
                or not identity.strip()
            ):
                raise ValueError(
                    f"{field} must contain non-empty identities"
                )

            if identity in seen:
                raise ValueError(
                    f"duplicate {field} identity: {identity}"
                )

            seen.add(identity)
