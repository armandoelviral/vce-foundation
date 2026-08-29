from sp001.contracts.knowledge_ingestion_registration import (
    KnowledgeIngestionRegistrationResult,
    KnowledgeIngestionRegistrationStatus,
)
from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRecord,
    KnowledgeIngestionRegistry,
)


def register_knowledge_ingestion(
    *,
    registry: KnowledgeIngestionRegistry,
    proposed_record: KnowledgeIngestionRecord,
) -> KnowledgeIngestionRegistrationResult:
    """Register, preserve or reject without mutating the input registry."""

    if not isinstance(
        registry,
        KnowledgeIngestionRegistry,
    ):
        raise TypeError(
            "registry must be a KnowledgeIngestionRegistry"
        )

    if not isinstance(
        proposed_record,
        KnowledgeIngestionRecord,
    ):
        raise TypeError(
            "proposed_record must be a "
            "KnowledgeIngestionRecord"
        )

    existing_by_ingestion_id = next(
        (
            record
            for record in registry.records
            if (
                record.ingestion_id
                == proposed_record.ingestion_id
            )
        ),
        None,
    )

    if existing_by_ingestion_id is not None:
        if existing_by_ingestion_id == proposed_record:
            status = (
                KnowledgeIngestionRegistrationStatus.UNCHANGED
            )
        else:
            status = (
                KnowledgeIngestionRegistrationStatus.CONFLICT
            )

        return KnowledgeIngestionRegistrationResult(
            status=status,
            registry=registry,
            proposed_record=proposed_record,
            existing_record=existing_by_ingestion_id,
        )

    existing_by_artifact_key = next(
        (
            record
            for record in registry.records
            if record.artifact_key == proposed_record.artifact_key
        ),
        None,
    )

    if existing_by_artifact_key is not None:
        same_artifact_payload = (
            existing_by_artifact_key.artifact_identity
            == proposed_record.artifact_identity
            and existing_by_artifact_key.fragment_set
            == proposed_record.fragment_set
        )

        status = (
            KnowledgeIngestionRegistrationStatus.UNCHANGED
            if same_artifact_payload
            else KnowledgeIngestionRegistrationStatus.CONFLICT
        )

        return KnowledgeIngestionRegistrationResult(
            status=status,
            registry=registry,
            proposed_record=proposed_record,
            existing_record=existing_by_artifact_key,
        )

    updated_registry = KnowledgeIngestionRegistry(
        records=registry.records + (proposed_record,),
    )

    return KnowledgeIngestionRegistrationResult(
        status=KnowledgeIngestionRegistrationStatus.REGISTERED,
        registry=updated_registry,
        proposed_record=proposed_record,
        existing_record=None,
    )
