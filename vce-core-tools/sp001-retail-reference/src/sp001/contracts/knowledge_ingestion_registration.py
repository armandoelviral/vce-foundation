from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRecord,
    KnowledgeIngestionRegistry,
)


class KnowledgeIngestionRegistrationStatus(StrEnum):
    """Result of a pure ingestion registry transition."""

    REGISTERED = "REGISTERED"
    UNCHANGED = "UNCHANGED"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistrationResult:
    """Registry transition result without persistence claims."""

    status: KnowledgeIngestionRegistrationStatus
    registry: KnowledgeIngestionRegistry
    proposed_record: KnowledgeIngestionRecord
    existing_record: KnowledgeIngestionRecord | None

    def __post_init__(self) -> None:
        if not isinstance(
            self.status,
            KnowledgeIngestionRegistrationStatus,
        ):
            raise TypeError(
                "status must be a "
                "KnowledgeIngestionRegistrationStatus"
            )

        if not isinstance(
            self.registry,
            KnowledgeIngestionRegistry,
        ):
            raise TypeError(
                "registry must be a KnowledgeIngestionRegistry"
            )

        if not isinstance(
            self.proposed_record,
            KnowledgeIngestionRecord,
        ):
            raise TypeError(
                "proposed_record must be a "
                "KnowledgeIngestionRecord"
            )

        if (
            self.existing_record is not None
            and not isinstance(
                self.existing_record,
                KnowledgeIngestionRecord,
            )
        ):
            raise TypeError(
                "existing_record must be a "
                "KnowledgeIngestionRecord when declared"
            )

        if (
            self.status
            is KnowledgeIngestionRegistrationStatus.REGISTERED
        ):
            if self.existing_record is not None:
                raise ValueError(
                    "REGISTERED result cannot contain "
                    "existing_record"
                )

            if self.proposed_record not in self.registry.records:
                raise ValueError(
                    "REGISTERED result registry must contain "
                    "proposed_record"
                )

            return

        if self.existing_record is None:
            raise ValueError(
                f"{self.status.value} result requires "
                "existing_record"
            )

        if self.existing_record not in self.registry.records:
            raise ValueError(
                "existing_record must belong to registry"
            )

        if (
            self.status
            is KnowledgeIngestionRegistrationStatus.UNCHANGED
            and (
                self.existing_record.artifact_identity
                != self.proposed_record.artifact_identity
                or self.existing_record.fragment_set
                != self.proposed_record.fragment_set
            )
        ):
            raise ValueError(
                "UNCHANGED result requires equivalent "
                "artifact and fragment set"
            )

        if (
            self.status
            is KnowledgeIngestionRegistrationStatus.CONFLICT
            and self.existing_record == self.proposed_record
        ):
            raise ValueError(
                "CONFLICT result requires distinct records"
            )
