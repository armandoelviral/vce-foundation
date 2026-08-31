from dataclasses import dataclass, field

from sp001.contracts.knowledge_lexical_ordering_evidence import (
    KNOWLEDGE_LEXICAL_ORDERING_POLICY,
    KnowledgeCandidateLexicalOrderingEvidence,
)
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)


@dataclass(frozen=True, slots=True)
class KnowledgeLexicalOrderingEntry:
    """One candidate's declared and resulting lexical positions."""

    declared_candidate_index: int
    ordered_candidate_index: int
    evidence: KnowledgeCandidateLexicalOrderingEvidence

    def __post_init__(self) -> None:
        for name, value in (
            (
                "declared_candidate_index",
                self.declared_candidate_index,
            ),
            (
                "ordered_candidate_index",
                self.ordered_candidate_index,
            ),
        ):
            if (
                isinstance(
                    value,
                    bool,
                )
                or not isinstance(
                    value,
                    int,
                )
            ):
                raise TypeError(
                    f"{name} must be an integer"
                )
            if value < 0:
                raise ValueError(
                    f"{name} must not be negative"
                )

        if not isinstance(
            self.evidence,
            KnowledgeCandidateLexicalOrderingEvidence,
        ):
            raise TypeError(
                "evidence must be a "
                "KnowledgeCandidateLexicalOrderingEvidence"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeLexicalOrdering:
    """Stable auditable lexical ordering without relevance claims."""

    query: KnowledgeLexicalQuery
    entries: tuple[
        KnowledgeLexicalOrderingEntry,
        ...,
    ]
    ordering_policy: str = field(
        init=False,
        default=KNOWLEDGE_LEXICAL_ORDERING_POLICY,
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.query,
            KnowledgeLexicalQuery,
        ):
            raise TypeError(
                "query must be a KnowledgeLexicalQuery"
            )
        if not isinstance(
            self.entries,
            tuple,
        ):
            raise TypeError(
                "entries must be an immutable tuple"
            )

        expected_indexes = set(
            range(
                len(
                    self.entries
                )
            )
        )
        declared_indexes: set[int] = set()
        candidate_ids: set[str] = set()
        source_identities: set[object] = set()

        previous_entry: (
            KnowledgeLexicalOrderingEntry | None
        ) = None

        for expected_ordered_index, entry in enumerate(
            self.entries
        ):
            if not isinstance(
                entry,
                KnowledgeLexicalOrderingEntry,
            ):
                raise TypeError(
                    "entries must contain "
                    "KnowledgeLexicalOrderingEntry values"
                )
            if (
                entry.ordered_candidate_index
                != expected_ordered_index
            ):
                raise ValueError(
                    "ordered_candidate_index must be contiguous "
                    "and reflect entry order"
                )
            if entry.declared_candidate_index in declared_indexes:
                raise ValueError(
                    "duplicate declared_candidate_index: "
                    f"{entry.declared_candidate_index}"
                )
            declared_indexes.add(
                entry.declared_candidate_index
            )

            match = entry.evidence.match
            if match.query != self.query:
                raise ValueError(
                    "entry evidence must use ordering query"
                )
            if match.candidate_id in candidate_ids:
                raise ValueError(
                    "duplicate candidate_id: "
                    f"{match.candidate_id}"
                )
            candidate_ids.add(
                match.candidate_id
            )
            if match.source_identity in source_identities:
                raise ValueError(
                    "duplicate candidate source identity: "
                    f"{match.source_identity.source_id} "
                    f"{match.source_identity.source_version}"
                )
            source_identities.add(
                match.source_identity
            )

            if previous_entry is not None:
                previous_key = (
                    previous_entry.evidence.ordering_key
                )
                current_key = entry.evidence.ordering_key

                if current_key > previous_key:
                    raise ValueError(
                        "entries must use descending ordering keys"
                    )
                if (
                    current_key == previous_key
                    and entry.declared_candidate_index
                    < previous_entry.declared_candidate_index
                ):
                    raise ValueError(
                        "equal ordering keys must preserve "
                        "declared candidate order"
                    )

            previous_entry = entry

        if declared_indexes != expected_indexes:
            raise ValueError(
                "declared_candidate_index values must be "
                "contiguous"
            )
