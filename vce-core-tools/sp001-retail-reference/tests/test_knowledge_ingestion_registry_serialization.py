import json

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
from sp001.services.knowledge_ingestion_registry_serialization import (
    KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION,
    serialize_knowledge_ingestion_registry,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


SOURCE_BYTES = b"source bytes"
CONFIG_BYTES = b"configuration"
ARTIFACT_BYTES = b"firstsecond"


def digest(content: bytes):
    return digest_knowledge_source_content(
        content=content,
    )


def create_record(
    *,
    ingestion_id: str = "INGESTION-001",
    artifact_id: str = "ARTIFACT-001",
    source_id: str = "SOURCE-001",
    fragment_prefix: str = "FRAGMENT",
) -> KnowledgeIngestionRecord:
    artifact = KnowledgeDerivedArtifactIdentity(
        artifact_id=artifact_id,
        artifact_version="v1",
        source_identity=KnowledgeSourceIdentity(
            source_id=source_id,
            source_version="v1",
            source_content_digest=digest(SOURCE_BYTES),
        ),
        extraction_identity=KnowledgeExtractionIdentity(
            extraction_id=f"EXTRACTION-{artifact_id}",
            extractor_id="TEXT-EXTRACTOR",
            extractor_version="1.0.0",
            configuration_digest=digest(CONFIG_BYTES),
        ),
        artifact_content_digest=digest(ARTIFACT_BYTES),
    )

    fragments = (
        KnowledgeFragmentIdentity(
            fragment_id=f"{fragment_prefix}-001",
            artifact_identity=artifact,
            sequence_number=0,
            byte_start=0,
            byte_end=5,
            fragment_content_digest=digest(b"first"),
        ),
        KnowledgeFragmentIdentity(
            fragment_id=f"{fragment_prefix}-002",
            artifact_identity=artifact,
            sequence_number=1,
            byte_start=5,
            byte_end=11,
            fragment_content_digest=digest(b"second"),
        ),
    )

    return KnowledgeIngestionRecord(
        ingestion_id=ingestion_id,
        artifact_identity=artifact,
        fragment_set=KnowledgeFragmentSet(
            artifact_identity=artifact,
            fragments=fragments,
        ),
    )


def create_registry(
    *records: KnowledgeIngestionRecord,
) -> KnowledgeIngestionRegistry:
    return KnowledgeIngestionRegistry(
        records=tuple(records),
    )


def create_payload() -> str:
    return serialize_knowledge_ingestion_registry(
        registry=create_registry(
            create_record(),
        ),
    )


def test_serializer_returns_text() -> None:
    assert isinstance(create_payload(), str)


def test_serializer_produces_json_object() -> None:
    document = json.loads(create_payload())

    assert isinstance(document, dict)


def test_schema_version_is_explicit_integer() -> None:
    document = json.loads(create_payload())

    assert KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION == 1
    assert document["schema_version"] == 1
    assert type(document["schema_version"]) is int


def test_empty_registry_preserves_empty_record_universe() -> None:
    payload = serialize_knowledge_ingestion_registry(
        registry=create_registry(),
    )

    assert json.loads(payload) == {
        "schema_version": 1,
        "records": [],
    }


def test_payload_preserves_complete_artifact_lineage() -> None:
    record = json.loads(create_payload())["records"][0]
    artifact = record["artifact"]

    assert record["ingestion_id"] == "INGESTION-001"
    assert artifact["artifact_id"] == "ARTIFACT-001"
    assert artifact["source"]["source_id"] == "SOURCE-001"
    assert (
        artifact["extraction"]["extractor_id"]
        == "TEXT-EXTRACTOR"
    )
    assert (
        artifact["content_digest"]["algorithm"]
        == "SHA-256"
    )


def test_payload_preserves_fragment_ranges_and_digests() -> None:
    fragments = json.loads(
        create_payload()
    )["records"][0]["fragments"]

    assert tuple(
        (
            fragment["fragment_id"],
            fragment["sequence_number"],
            fragment["byte_start"],
            fragment["byte_end"],
        )
        for fragment in fragments
    ) == (
        ("FRAGMENT-001", 0, 0, 5),
        ("FRAGMENT-002", 1, 5, 11),
    )

    assert all(
        fragment["content_digest"]["algorithm"]
        == "SHA-256"
        for fragment in fragments
    )


def test_serializer_preserves_declared_record_order() -> None:
    registry = create_registry(
        create_record(
            ingestion_id="INGESTION-002",
            artifact_id="ARTIFACT-002",
            source_id="SOURCE-002",
            fragment_prefix="SECOND",
        ),
        create_record(
            ingestion_id="INGESTION-001",
            artifact_id="ARTIFACT-001",
            source_id="SOURCE-001",
            fragment_prefix="FIRST",
        ),
    )

    document = json.loads(
        serialize_knowledge_ingestion_registry(
            registry=registry,
        )
    )

    assert tuple(
        record["ingestion_id"]
        for record in document["records"]
    ) == (
        "INGESTION-002",
        "INGESTION-001",
    )


def test_serializer_is_deterministic_for_same_registry() -> None:
    registry = create_registry(create_record())

    first = serialize_knowledge_ingestion_registry(
        registry=registry,
    )
    second = serialize_knowledge_ingestion_registry(
        registry=registry,
    )

    assert first == second


def test_equivalent_registries_produce_identical_payloads() -> None:
    first = create_registry(create_record())
    second = create_registry(create_record())

    assert serialize_knowledge_ingestion_registry(
        registry=first,
    ) == serialize_knowledge_ingestion_registry(
        registry=second,
    )


def test_record_order_changes_payload() -> None:
    first = create_record(
        ingestion_id="INGESTION-001",
        artifact_id="ARTIFACT-001",
        fragment_prefix="FIRST",
    )
    second = create_record(
        ingestion_id="INGESTION-002",
        artifact_id="ARTIFACT-002",
        source_id="SOURCE-002",
        fragment_prefix="SECOND",
    )

    assert serialize_knowledge_ingestion_registry(
        registry=create_registry(first, second),
    ) != serialize_knowledge_ingestion_registry(
        registry=create_registry(second, first),
    )


def test_serializer_orders_object_keys_deterministically() -> None:
    payload = create_payload()

    assert payload.startswith(
        '{"records":['
    )
    assert payload.endswith(
        ',"schema_version":1}'
    )


def test_serializer_uses_compact_json_separators() -> None:
    payload = create_payload()

    assert ": " not in payload
    assert ", " not in payload
    assert "\n" not in payload


def test_serializer_preserves_unicode_without_ascii_escape() -> None:
    registry = create_registry(
        create_record(
            ingestion_id="INGESTIÓN-001",
            artifact_id="ARTEFACTO-CAFÉ",
            source_id="FUENTE-NIÑEZ",
        ),
    )

    payload = serialize_knowledge_ingestion_registry(
        registry=registry,
    )

    assert "INGESTIÓN-001" in payload
    assert "ARTEFACTO-CAFÉ" in payload
    assert "FUENTE-NIÑEZ" in payload
    assert "\\u00" not in payload


def test_serializer_rejects_untyped_registry() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistry",
    ):
        serialize_knowledge_ingestion_registry(
            registry="registry",
        )


def test_serialization_does_not_mutate_registry() -> None:
    record = create_record()
    registry = create_registry(record)

    serialize_knowledge_ingestion_registry(
        registry=registry,
    )

    assert registry.records == (record,)


def test_payload_does_not_claim_persistence_or_integrity() -> None:
    document = json.loads(create_payload())

    for field in (
        "persisted",
        "storage_path",
        "signature",
        "authentic",
        "verified",
        "indexed",
        "embedded",
        "retrieval_eligible",
    ):
        assert field not in document
