from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.knowledge_derived_artifact import (
    KnowledgeDerivedArtifactIdentity,
    KnowledgeExtractionIdentity,
    KnowledgeFragmentIdentity,
    KnowledgeFragmentSet,
)
from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRecord,
    KnowledgeIngestionRegistry,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


SOURCE_BYTES = b"source bytes"
CONFIG_BYTES = b"extractor configuration"
ARTIFACT_BYTES = b"firstsecond"


def digest(content: bytes):
    return digest_knowledge_source_content(
        content=content,
    )


def artifact_identity(
    *,
    artifact_id: str = "ARTIFACT-001",
    artifact_version: str = "v1",
    artifact_content: bytes = ARTIFACT_BYTES,
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
            extractor_id="TEXT-EXTRACTOR",
            extractor_version="1.0.0",
            configuration_digest=digest(CONFIG_BYTES),
        ),
        artifact_content_digest=digest(artifact_content),
    )


def fragment_set(
    artifact: KnowledgeDerivedArtifactIdentity,
) -> KnowledgeFragmentSet:
    return KnowledgeFragmentSet(
        artifact_identity=artifact,
        fragments=(
            KnowledgeFragmentIdentity(
                fragment_id=(
                    f"FRAGMENT-{artifact.artifact_id}"
                ),
                artifact_identity=artifact,
                sequence_number=0,
                byte_start=0,
                byte_end=len(ARTIFACT_BYTES),
                fragment_content_digest=digest(
                    ARTIFACT_BYTES
                ),
            ),
        ),
    )


def create_record(
    *,
    ingestion_id: str = "INGESTION-001",
    artifact: KnowledgeDerivedArtifactIdentity | None = None,
) -> KnowledgeIngestionRecord:
    selected_artifact = artifact or artifact_identity()

    return KnowledgeIngestionRecord(
        ingestion_id=ingestion_id,
        artifact_identity=selected_artifact,
        fragment_set=fragment_set(selected_artifact),
    )


def test_record_preserves_artifact_and_fragments() -> None:
    record = create_record()

    assert record.ingestion_id == "INGESTION-001"
    assert (
        record.fragment_set.artifact_identity
        is record.artifact_identity
    )


@pytest.mark.parametrize(
    "ingestion_id",
    ("", " "),
)
def test_record_rejects_empty_identity(
    ingestion_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="ingestion_id must not be empty",
    ):
        create_record(ingestion_id=ingestion_id)


def test_record_rejects_untyped_artifact() -> None:
    artifact = artifact_identity()

    with pytest.raises(
        TypeError,
        match="KnowledgeDerivedArtifactIdentity",
    ):
        KnowledgeIngestionRecord(
            ingestion_id="INGESTION-001",
            artifact_identity="artifact",
            fragment_set=fragment_set(artifact),
        )


def test_record_rejects_untyped_fragment_set() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeFragmentSet",
    ):
        KnowledgeIngestionRecord(
            ingestion_id="INGESTION-001",
            artifact_identity=artifact_identity(),
            fragment_set="fragments",
        )


def test_record_rejects_cross_artifact_fragment_set() -> None:
    artifact = artifact_identity()
    other = artifact_identity(
        artifact_id="ARTIFACT-OTHER",
    )

    with pytest.raises(
        ValueError,
        match="fragment_set must describe artifact_identity",
    ):
        KnowledgeIngestionRecord(
            ingestion_id="INGESTION-001",
            artifact_identity=artifact,
            fragment_set=fragment_set(other),
        )


def test_artifact_key_uses_opaque_id_and_version() -> None:
    record = create_record()

    assert record.artifact_key == (
        "ARTIFACT-001",
        "v1",
    )


def test_record_is_immutable() -> None:
    record = create_record()

    with pytest.raises(FrozenInstanceError):
        record.ingestion_id = "OTHER"


def test_empty_registry_is_explicitly_valid() -> None:
    registry = KnowledgeIngestionRegistry(
        records=(),
    )

    assert registry.records == ()


def test_registry_preserves_declared_record_order() -> None:
    first = create_record(
        ingestion_id="INGESTION-001",
        artifact=artifact_identity(
            artifact_id="ARTIFACT-001",
        ),
    )
    second = create_record(
        ingestion_id="INGESTION-002",
        artifact=artifact_identity(
            artifact_id="ARTIFACT-002",
        ),
    )

    registry = KnowledgeIngestionRegistry(
        records=(first, second),
    )

    assert registry.records == (first, second)


def test_registry_rejects_mutable_collection() -> None:
    with pytest.raises(
        TypeError,
        match="records must be an immutable tuple",
    ):
        KnowledgeIngestionRegistry(
            records=[],
        )


def test_registry_rejects_untyped_record() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRecord values",
    ):
        KnowledgeIngestionRegistry(
            records=("record",),
        )


def test_registry_rejects_duplicate_ingestion_identity() -> None:
    first = create_record()
    second = create_record(
        ingestion_id="INGESTION-001",
        artifact=artifact_identity(
            artifact_id="ARTIFACT-002",
        ),
    )

    with pytest.raises(
        ValueError,
        match="duplicate ingestion_id",
    ):
        KnowledgeIngestionRegistry(
            records=(first, second),
        )


def test_registry_rejects_duplicate_artifact_key() -> None:
    first = create_record()
    conflicting_artifact = artifact_identity(
        artifact_id="ARTIFACT-001",
        artifact_version="v1",
        artifact_content=b"different artifact bytes",
    )
    second = create_record(
        ingestion_id="INGESTION-002",
        artifact=conflicting_artifact,
    )

    with pytest.raises(
        ValueError,
        match="duplicate artifact key",
    ):
        KnowledgeIngestionRegistry(
            records=(first, second),
        )


def test_registry_allows_same_artifact_id_with_distinct_version() -> None:
    first = create_record(
        ingestion_id="INGESTION-001",
        artifact=artifact_identity(
            artifact_version="opaque-a",
        ),
    )
    second = create_record(
        ingestion_id="INGESTION-002",
        artifact=artifact_identity(
            artifact_version="opaque-b",
        ),
    )

    registry = KnowledgeIngestionRegistry(
        records=(first, second),
    )

    assert len(registry.records) == 2


def test_registry_is_immutable() -> None:
    registry = KnowledgeIngestionRegistry(
        records=(create_record(),),
    )

    with pytest.raises(FrozenInstanceError):
        registry.records = ()


def test_registry_does_not_claim_persistence_or_acceptance() -> None:
    registry = KnowledgeIngestionRegistry(
        records=(create_record(),),
    )

    for attribute in (
        "saved",
        "database_id",
        "persisted_at",
        "accepted",
        "indexed",
        "embedded",
        "retrieval_eligible",
        "authority",
    ):
        assert not hasattr(registry, attribute)
