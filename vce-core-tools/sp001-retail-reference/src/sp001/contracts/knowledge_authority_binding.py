from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.knowledge_source_status import (
    KnowledgeSourceStatus,
)
from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)


class KnowledgeAuthorityRelationshipType(StrEnum):
    """Declared relationship between a governed and governing source."""

    GOVERNS = "GOVERNS"
    DELEGATES = "DELEGATES"


class KnowledgeAuthorityAdjudicationStatus(StrEnum):
    """Recorded adjudication status without legal-authority guarantees."""

    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    REVOKED = "REVOKED"


@dataclass(frozen=True, slots=True)
class KnowledgeAuthorityBinding:
    """Versioned authority reference and its explicit adjudication record."""

    authority_binding_id: str
    binding_version: int
    governed_source_status: KnowledgeSourceStatus
    authority_source_status: KnowledgeSourceStatus
    relationship_type: KnowledgeAuthorityRelationshipType
    adjudication_status: KnowledgeAuthorityAdjudicationStatus
    adjudication_evidence_ids: tuple[str, ...] = ()
    adjudicated_by: RetailProcessActor | None = None
    adjudicated_at: datetime | None = None

    def __post_init__(self) -> None:
        if (
            not isinstance(
                self.authority_binding_id,
                str,
            )
            or not self.authority_binding_id.strip()
        ):
            raise ValueError(
                "authority_binding_id must not be empty"
            )

        if (
            isinstance(
                self.binding_version,
                bool,
            )
            or not isinstance(
                self.binding_version,
                int,
            )
            or self.binding_version < 1
        ):
            raise ValueError(
                "binding_version must be a positive integer"
            )

        if not isinstance(
            self.governed_source_status,
            KnowledgeSourceStatus,
        ):
            raise TypeError(
                "governed_source_status must be a "
                "KnowledgeSourceStatus"
            )

        if not isinstance(
            self.authority_source_status,
            KnowledgeSourceStatus,
        ):
            raise TypeError(
                "authority_source_status must be a "
                "KnowledgeSourceStatus"
            )

        if (
            self.governed_source_status.identity
            == self.authority_source_status.identity
        ):
            raise ValueError(
                "source cannot govern itself"
            )

        if not isinstance(
            self.relationship_type,
            KnowledgeAuthorityRelationshipType,
        ):
            raise TypeError(
                "relationship_type must be a "
                "KnowledgeAuthorityRelationshipType"
            )

        if not isinstance(
            self.adjudication_status,
            KnowledgeAuthorityAdjudicationStatus,
        ):
            raise TypeError(
                "adjudication_status must be a "
                "KnowledgeAuthorityAdjudicationStatus"
            )

        if not isinstance(
            self.adjudication_evidence_ids,
            tuple,
        ):
            raise TypeError(
                "adjudication_evidence_ids must be "
                "an immutable tuple"
            )

        seen_evidence_ids: set[str] = set()

        for evidence_id in self.adjudication_evidence_ids:
            if (
                not isinstance(
                    evidence_id,
                    str,
                )
                or not evidence_id.strip()
            ):
                raise ValueError(
                    "adjudication evidence_id must not be empty"
                )

            if evidence_id in seen_evidence_ids:
                raise ValueError(
                    "duplicate adjudication evidence_id: "
                    f"{evidence_id}"
                )

            seen_evidence_ids.add(
                evidence_id,
            )

        if (
            self.adjudication_status
            is KnowledgeAuthorityAdjudicationStatus.UNVERIFIED
        ):
            if self.adjudication_evidence_ids:
                raise ValueError(
                    "UNVERIFIED binding cannot contain "
                    "adjudication evidence"
                )

            if self.adjudicated_by is not None:
                raise ValueError(
                    "UNVERIFIED binding cannot declare "
                    "an adjudicator"
                )

            if self.adjudicated_at is not None:
                raise ValueError(
                    "UNVERIFIED binding cannot declare "
                    "an adjudication time"
                )

            return

        if not self.adjudication_evidence_ids:
            raise ValueError(
                "adjudicated binding requires evidence"
            )

        if not isinstance(
            self.adjudicated_by,
            RetailProcessActor,
        ):
            raise TypeError(
                "adjudicated_by must be a RetailProcessActor"
            )

        if (
            self.adjudicated_by.actor_type
            is ActorType.SYSTEM
        ):
            raise ValueError(
                "SYSTEM actor cannot adjudicate authority"
            )

        governed_customer_id = (
            self.governed_source_status.scope.customer_id
        )

        if (
            self.adjudicated_by.customer_id
            != governed_customer_id
        ):
            raise ValueError(
                "adjudicator customer must match "
                "governed source customer"
            )

        if not isinstance(
            self.adjudicated_at,
            datetime,
        ):
            raise TypeError(
                "adjudicated_at must be a datetime"
            )

        if (
            self.adjudicated_at.tzinfo is None
            or self.adjudicated_at.utcoffset() is None
        ):
            raise ValueError(
                "adjudicated_at must be timezone-aware"
            )
