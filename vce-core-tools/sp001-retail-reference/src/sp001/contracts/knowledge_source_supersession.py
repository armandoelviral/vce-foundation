from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeSourceStatus,
)
from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)


@dataclass(frozen=True, slots=True)
class KnowledgeSourceSupersession:
    """Explicit predecessor-to-successor declaration with preserved history."""

    supersession_id: str
    supersession_version: int
    predecessor_source_status: KnowledgeSourceStatus
    successor_source_status: KnowledgeSourceStatus
    declaration_evidence_ids: tuple[str, ...]
    declared_by: RetailProcessActor
    declared_at: datetime

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.supersession_id,
                str,
            )
            or not self.supersession_id.strip()
        ):
            raise ValueError(
                "supersession_id must not be empty"
            )

        if (
            isinstance(
                self.supersession_version,
                bool,
            )
            or not isinstance(
                self.supersession_version,
                int,
            )
            or self.supersession_version < 1
        ):
            raise ValueError(
                "supersession_version must be a positive integer"
            )

        source_fields = {
            "predecessor_source_status": (
                self.predecessor_source_status
            ),
            "successor_source_status": (
                self.successor_source_status
            ),
        }

        for field, source_status in source_fields.items():
            if not isinstance(
                source_status,
                KnowledgeSourceStatus,
            ):
                raise TypeError(
                    f"{field} must be a "
                    "KnowledgeSourceStatus"
                )

        predecessor_identity = (
            self.predecessor_source_status.identity
        )
        successor_identity = (
            self.successor_source_status.identity
        )

        if predecessor_identity == successor_identity:
            raise ValueError(
                "source cannot supersede itself"
            )

        predecessor_scope = (
            self.predecessor_source_status.scope
        )
        successor_scope = (
            self.successor_source_status.scope
        )

        if (
            predecessor_scope.customer_id
            != successor_scope.customer_id
        ):
            raise ValueError(
                "supersession sources must share customer"
            )

        if (
            predecessor_scope.document_type
            is not successor_scope.document_type
        ):
            raise ValueError(
                "supersession sources must share document_type"
            )

        if not isinstance(
            self.declaration_evidence_ids,
            tuple,
        ):
            raise TypeError(
                "declaration_evidence_ids must be "
                "an immutable tuple"
            )

        if not self.declaration_evidence_ids:
            raise ValueError(
                "declaration_evidence_ids must not be empty"
            )

        seen_evidence_ids: set[str] = set()

        for evidence_id in self.declaration_evidence_ids:
            if (
                not isinstance(
                    evidence_id,
                    str,
                )
                or not evidence_id.strip()
            ):
                raise ValueError(
                    "declaration evidence_id must not be empty"
                )

            if evidence_id in seen_evidence_ids:
                raise ValueError(
                    "duplicate declaration evidence_id: "
                    f"{evidence_id}"
                )

            seen_evidence_ids.add(
                evidence_id,
            )

        if not isinstance(
            self.declared_by,
            RetailProcessActor,
        ):
            raise TypeError(
                "declared_by must be a RetailProcessActor"
            )

        if self.declared_by.actor_type is ActorType.SYSTEM:
            raise ValueError(
                "SYSTEM actor cannot declare supersession"
            )

        if (
            self.declared_by.customer_id
            != successor_scope.customer_id
        ):
            raise ValueError(
                "declarer customer must match "
                "supersession customer"
            )

        if not isinstance(
            self.declared_at,
            datetime,
        ):
            raise TypeError(
                "declared_at must be a datetime"
            )

        if (
            self.declared_at.tzinfo is None
            or self.declared_at.utcoffset() is None
        ):
            raise ValueError(
                "declared_at must be timezone-aware"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeSourceSupersessionGraph:
    """Immutable acyclic supersession lineage."""

    supersessions: tuple[
        KnowledgeSourceSupersession,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.supersessions,
            tuple,
        ):
            raise TypeError(
                "supersessions must be an immutable tuple"
            )

        seen_supersession_ids: set[str] = set()
        seen_edges: set[
            tuple[
                KnowledgeSourceIdentity,
                KnowledgeSourceIdentity,
            ]
        ] = set()
        successor_by_predecessor: dict[
            KnowledgeSourceIdentity,
            KnowledgeSourceIdentity,
        ] = {}
        adjacency: dict[
            KnowledgeSourceIdentity,
            set[KnowledgeSourceIdentity],
        ] = {}

        for supersession in self.supersessions:
            if not isinstance(
                supersession,
                KnowledgeSourceSupersession,
            ):
                raise TypeError(
                    "supersessions must contain "
                    "KnowledgeSourceSupersession values"
                )

            if (
                supersession.supersession_id
                in seen_supersession_ids
            ):
                raise ValueError(
                    "duplicate supersession_id: "
                    f"{supersession.supersession_id}"
                )

            seen_supersession_ids.add(
                supersession.supersession_id,
            )

            predecessor = (
                supersession.predecessor_source_status.identity
            )
            successor = (
                supersession.successor_source_status.identity
            )
            edge = (
                predecessor,
                successor,
            )

            if edge in seen_edges:
                raise ValueError(
                    "duplicate supersession edge"
                )

            seen_edges.add(
                edge,
            )

            existing_successor = (
                successor_by_predecessor.get(
                    predecessor,
                )
            )

            if (
                existing_successor is not None
                and existing_successor != successor
            ):
                raise ValueError(
                    "ambiguous successors for predecessor source"
                )

            successor_by_predecessor[
                predecessor
            ] = successor

            adjacency.setdefault(
                predecessor,
                set(),
            ).add(
                successor,
            )
            adjacency.setdefault(
                successor,
                set(),
            )

        visiting: set[KnowledgeSourceIdentity] = set()
        visited: set[KnowledgeSourceIdentity] = set()

        def visit(
            source: KnowledgeSourceIdentity,
        ) -> None:
            if source in visiting:
                raise ValueError(
                    "supersession graph must be acyclic"
                )

            if source in visited:
                return

            visiting.add(
                source,
            )

            for successor in adjacency[source]:
                visit(
                    successor,
                )

            visiting.remove(
                source,
            )
            visited.add(
                source,
            )

        for source in adjacency:
            visit(
                source,
            )
