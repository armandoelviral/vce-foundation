from dataclasses import dataclass, field

from sp001.contracts.knowledge_governed_retrieval import (
    KnowledgeGovernedRetrievalResult,
)


KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalEvidence:
    """Versioned immutable evidence before wire serialization."""

    result: KnowledgeGovernedRetrievalResult
    schema_version: int = field(
        init=False,
        default=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION
        ),
    )
    candidate_count: int = field(
        init=False,
    )
    included_candidate_count: int = field(
        init=False,
    )
    excluded_candidate_count: int = field(
        init=False,
    )
    ordered_candidate_count: int = field(
        init=False,
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.result,
            KnowledgeGovernedRetrievalResult,
        ):
            raise TypeError(
                "result must be a "
                "KnowledgeGovernedRetrievalResult"
            )

        candidate_count = len(
            self.result.manifest.candidate_decisions
        )
        included_candidate_count = len(
            self.result.included_candidate_decisions
        )
        excluded_candidate_count = len(
            self.result.excluded_candidate_decisions
        )
        ordered_candidate_count = len(
            self.result.lexical_ordering.entries
        )

        if (
            included_candidate_count
            + excluded_candidate_count
            != candidate_count
        ):
            raise ValueError(
                "included and excluded counts must reconcile "
                "with candidate count"
            )

        if (
            ordered_candidate_count
            != included_candidate_count
        ):
            raise ValueError(
                "ordered candidate count must equal included "
                "candidate count"
            )

        object.__setattr__(
            self,
            "candidate_count",
            candidate_count,
        )
        object.__setattr__(
            self,
            "included_candidate_count",
            included_candidate_count,
        )
        object.__setattr__(
            self,
            "excluded_candidate_count",
            excluded_candidate_count,
        )
        object.__setattr__(
            self,
            "ordered_candidate_count",
            ordered_candidate_count,
        )
