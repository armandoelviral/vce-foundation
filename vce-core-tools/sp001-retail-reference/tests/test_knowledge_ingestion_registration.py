from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.knowledge_derived_artifact import (
    KnowledgeDerivedArtifactIdentity,
    KnowledgeExtractionIdentity,
    KnowledgeFragmentIdentity,
    KnowledgeFragmentSet,
)
from sp001.contracts.knowledge_ingestion_registration import (
    KnowledgeIngestionRegistrationResult,
    KnowledgeIngestionRegistrationStatus,
)
from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRecord,
    KnowledgeIngestionRegistry,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.services.knowledge_ingestion_registration import (
    register_knowledge_ingestion,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


SOURCE_BYTES = b"source"
CONFIG_BYTES = b"configuration"
ARTIFACT_BYTES = b"artifact"


def digest(content: bytes):
    return digest_knowledge_source_content(
        content=content,
    )


def artifact(
    *,
    artifact_id: str = "ARTIFACT-001",
    artifact_version: str = "v1",
    content: bytes = ARTIFACT_BYTES,
) -> KnowledgeDerivedArtifactIdentity:
    return KnowledgeDerivedArtifactIdentity(
        artifact_id=artifact_id,
        artifact_version=artifact_version,
        source_identity=KnowledgeSourceIdentity(
            source_id="SOURCE-001",
            source_version="v1",
            source_content_digest=digest(SOURCE_BYTES),
        ),
        extraction_identity=KnowledgeExtractionIdentity(
            extraction_id="EXTRACTION-001",
            extractor_id="EXTRACTOR",
            extractor_version="1.0.0",
            configuration_digest=digest(CONFIG_BYTES),
        ),
        artifact_content_digest=digest(content),
    )


def record(
    *,
    ingestion_id: str = "INGESTION-001",
    artifact_identity=None,
) -> KnowledgeIngestionRecord:
    selected = artifact_identity or artifact()

    return KnowledgeIngestionRecord(
        ingestion_id=ingestion_id,
        artifact_identity=selected,
        fragment_set=KnowledgeFragmentSet(
            artifact_identity=selected,
            fragments=(
                KnowledgeFragmentIdentity(
                    fragment_id=(
                        f"FRAGMENT-{selected.artifact_id}"
                    ),
                    artifact_identity=selected,
                    sequence_number=0,
                    byte_start=0,
                    byte_end=len(ARTIFACT_BYTES),
                    fragment_content_digest=digest(
                        ARTIFACT_BYTES
                    ),
                ),
            ),
        ),
    )


def registry(
    *records: KnowledgeIngestionRecord,
) -> KnowledgeIngestionRegistry:
    return KnowledgeIngestionRegistry(
        records=tuple(records),
    )


def test_registration_status_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeIngestionRegistrationStatus) == (
        KnowledgeIngestionRegistrationStatus.REGISTERED,
        KnowledgeIngestionRegistrationStatus.UNCHANGED,
        KnowledgeIngestionRegistrationStatus.CONFLICT,
    )


def test_new_record_is_registered_at_end() -> None:
    existing = record(
        ingestion_id="INGESTION-001",
        artifact_identity=artifact(
            artifact_id="ARTIFACT-001",
        ),
    )
    proposed = record(
        ingestion_id="INGESTION-002",
        artifact_identity=artifact(
            artifact_id="ARTIFACT-002",
        ),
    )
    original = registry(existing)

    result = register_knowledge_ingestion(
        registry=original,
        proposed_record=proposed,
    )

    assert result.status is (
        KnowledgeIngestionRegistrationStatus.REGISTERED
    )
    assert result.registry.records == (
        existing,
        proposed,
    )
    assert result.existing_record is None


def test_registration_does_not_mutate_original_registry() -> None:
    original = registry()
    proposed = record()

    result = register_knowledge_ingestion(
        registry=original,
        proposed_record=proposed,
    )

    assert original.records == ()
    assert result.registry is not original


def test_exact_replay_is_unchanged() -> None:
    existing = record()
    original = registry(existing)

    result = register_knowledge_ingestion(
        registry=original,
        proposed_record=existing,
    )

    assert result.status is (
        KnowledgeIngestionRegistrationStatus.UNCHANGED
    )
    assert result.registry is original
    assert result.existing_record is existing


def test_same_artifact_under_new_ingestion_id_is_unchanged() -> None:
    existing = record(
        ingestion_id="INGESTION-001",
    )
    proposed = record(
        ingestion_id="INGESTION-RETRY",
        artifact_identity=existing.artifact_identity,
    )
    proposed = KnowledgeIngestionRecord(
        ingestion_id=proposed.ingestion_id,
        artifact_identity=existing.artifact_identity,
        fragment_set=existing.fragment_set,
    )
    original = registry(existing)

    result = register_knowledge_ingestion(
        registry=original,
        proposed_record=proposed,
    )

    assert result.status is (
        KnowledgeIngestionRegistrationStatus.UNCHANGED
    )
    assert result.registry is original
    assert result.existing_record is existing


def test_reused_ingestion_id_for_other_artifact_conflicts() -> None:
    existing = record()
    proposed = record(
        ingestion_id="INGESTION-001",
        artifact_identity=artifact(
            artifact_id="ARTIFACT-OTHER",
        ),
    )
    original = registry(existing)

    result = register_knowledge_ingestion(
        registry=original,
        proposed_record=proposed,
    )

    assert result.status is (
        KnowledgeIngestionRegistrationStatus.CONFLICT
    )
    assert result.registry is original
    assert result.existing_record is existing


def test_same_artifact_key_with_different_digest_conflicts() -> None:
    existing = record()
    proposed = record(
        ingestion_id="INGESTION-002",
        artifact_identity=artifact(
            content=b"different artifact",
        ),
    )
    original = registry(existing)

    result = register_knowledge_ingestion(
        registry=original,
        proposed_record=proposed,
    )

    assert result.status is (
        KnowledgeIngestionRegistrationStatus.CONFLICT
    )
    assert result.registry is original
    assert result.existing_record is existing


def test_distinct_opaque_version_registers_independently() -> None:
    existing = record(
        artifact_identity=artifact(
            artifact_version="opaque-a",
        ),
    )
    proposed = record(
        ingestion_id="INGESTION-002",
        artifact_identity=artifact(
            artifact_version="opaque-b",
        ),
    )

    result = register_knowledge_ingestion(
        registry=registry(existing),
        proposed_record=proposed,
    )

    assert result.status is (
        KnowledgeIngestionRegistrationStatus.REGISTERED
    )


def test_empty_registry_accepts_first_record() -> None:
    proposed = record()

    result = register_knowledge_ingestion(
        registry=registry(),
        proposed_record=proposed,
    )

    assert result.registry.records == (proposed,)


def test_registration_rejects_untyped_registry() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistry",
    ):
        register_knowledge_ingestion(
            registry="registry",
            proposed_record=record(),
        )


def test_registration_rejects_untyped_record() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRecord",
    ):
        register_knowledge_ingestion(
            registry=registry(),
            proposed_record="record",
        )


def test_result_rejects_inconsistent_registered_state() -> None:
    proposed = record()

    with pytest.raises(
        ValueError,
        match="must contain proposed_record",
    ):
        KnowledgeIngestionRegistrationResult(
            status=(
                KnowledgeIngestionRegistrationStatus.REGISTERED
            ),
            registry=registry(),
            proposed_record=proposed,
            existing_record=None,
        )


def test_result_rejects_reasonless_existing_state() -> None:
    proposed = record()

    with pytest.raises(
        ValueError,
        match="requires existing_record",
    ):
        KnowledgeIngestionRegistrationResult(
            status=(
                KnowledgeIngestionRegistrationStatus.CONFLICT
            ),
            registry=registry(),
            proposed_record=proposed,
            existing_record=None,
        )


def test_registration_result_is_immutable() -> None:
    result = register_knowledge_ingestion(
        registry=registry(),
        proposed_record=record(),
    )

    with pytest.raises(FrozenInstanceError):
        result.status = (
            KnowledgeIngestionRegistrationStatus.CONFLICT
        )


def test_conflict_preserves_both_existing_and_proposed_records() -> None:
    existing = record()
    proposed = record(
        ingestion_id="INGESTION-002",
        artifact_identity=artifact(
            content=b"different artifact",
        ),
    )

    result = register_knowledge_ingestion(
        registry=registry(existing),
        proposed_record=proposed,
    )

    assert result.existing_record is existing
    assert result.proposed_record is proposed


def test_registration_does_not_claim_persistence_or_indexing() -> None:
    result = register_knowledge_ingestion(
        registry=registry(),
        proposed_record=record(),
    )

    for attribute in (
        "persisted",
        "database_transaction",
        "indexed",
        "embedded",
        "retrieval_eligible",
        "accepted_by_customer",
        "authority",
    ):
        assert not hasattr(result, attribute)
