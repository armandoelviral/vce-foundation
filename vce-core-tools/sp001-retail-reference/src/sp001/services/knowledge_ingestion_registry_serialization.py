import json

from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRegistry,
)


KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION = 1


def serialize_knowledge_ingestion_registry(
    *,
    registry: KnowledgeIngestionRegistry,
) -> str:
    """Serialize one registry to deterministic compact JSON text."""

    if not isinstance(
        registry,
        KnowledgeIngestionRegistry,
    ):
        raise TypeError(
            "registry must be a KnowledgeIngestionRegistry"
        )

    document = {
        "schema_version": (
            KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION
        ),
        "records": [
            _record_document(record)
            for record in registry.records
        ],
    }

    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _record_document(record):
    artifact = record.artifact_identity
    source = artifact.source_identity
    extraction = artifact.extraction_identity

    return {
        "ingestion_id": record.ingestion_id,
        "artifact": {
            "artifact_id": artifact.artifact_id,
            "artifact_version": artifact.artifact_version,
            "source": {
                "source_id": source.source_id,
                "source_version": source.source_version,
                "content_digest": _digest_document(
                    source.source_content_digest
                ),
            },
            "extraction": {
                "extraction_id": extraction.extraction_id,
                "extractor_id": extraction.extractor_id,
                "extractor_version": (
                    extraction.extractor_version
                ),
                "configuration_digest": _digest_document(
                    extraction.configuration_digest
                ),
            },
            "content_digest": _digest_document(
                artifact.artifact_content_digest
            ),
        },
        "fragments": [
            {
                "fragment_id": fragment.fragment_id,
                "sequence_number": fragment.sequence_number,
                "byte_start": fragment.byte_start,
                "byte_end": fragment.byte_end,
                "content_digest": _digest_document(
                    fragment.fragment_content_digest
                ),
            }
            for fragment in record.fragment_set.fragments
        ],
    }


def _digest_document(digest):
    return {
        "algorithm": digest.algorithm,
        "value": digest.value,
    }
