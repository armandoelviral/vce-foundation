from dataclasses import FrozenInstanceError
import hashlib
import re

import pytest

from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
    digest_knowledge_ingestion_registry,
)
from sp001.services.knowledge_ingestion_registry_serialization import (
    serialize_knowledge_ingestion_registry,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def test_digest_returns_immutable_content_identity() -> None:
    digest = digest_knowledge_ingestion_registry(
        registry=create_registry(),
    )

    assert isinstance(
        digest,
        KnowledgeIngestionRegistryDigest,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        digest.value = "0" * 64


def test_digest_declares_sha256_algorithm() -> None:
    digest = digest_knowledge_ingestion_registry(
        registry=create_registry(),
    )

    assert digest.algorithm == "SHA-256"


def test_digest_declares_utf8_encoding() -> None:
    digest = digest_knowledge_ingestion_registry(
        registry=create_registry(),
    )

    assert digest.encoding == "UTF-8"


def test_digest_contains_canonical_lowercase_hexadecimal_value() -> None:
    digest = digest_knowledge_ingestion_registry(
        registry=create_registry(),
    )

    assert re.fullmatch(
        r"[0-9a-f]{64}",
        digest.value,
    )


def test_digest_matches_independent_sha256_calculation() -> None:
    registry = create_registry(
        create_record(),
    )

    payload = serialize_knowledge_ingestion_registry(
        registry=registry,
    )

    expected = hashlib.sha256(
        payload.encode(
            "utf-8",
        )
    ).hexdigest()

    observed = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    assert observed.value == expected


def test_digest_is_deterministic_for_same_registry() -> None:
    registry = create_registry(
        create_record(),
    )

    first = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    second = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    assert first == second


def test_digest_is_deterministic_across_equivalent_registries() -> None:
    first_registry = create_registry(
        create_record(),
    )

    second_registry = create_registry(
        create_record(),
    )

    assert first_registry is not second_registry

    first = digest_knowledge_ingestion_registry(
        registry=first_registry,
    )

    second = digest_knowledge_ingestion_registry(
        registry=second_registry,
    )

    assert first == second


def test_digest_changes_when_record_order_changes() -> None:
    record_a = create_record(
        ingestion_id="INGESTION-A",
        artifact_id="ARTIFACT-A",
    )

    record_b = create_record(
        ingestion_id="INGESTION-B",
        artifact_id="ARTIFACT-B",
    )

    forward = digest_knowledge_ingestion_registry(
        registry=create_registry(
            record_a,
            record_b,
        ),
    )

    reverse = digest_knowledge_ingestion_registry(
        registry=create_registry(
            record_b,
            record_a,
        ),
    )

    assert forward != reverse


@pytest.mark.parametrize(
    (
        "ingestion_id",
        "artifact_id",
    ),
    (
        (
            "INGESTION-CHANGED",
            "ARTIFACT-001",
        ),
        (
            "INGESTION-001",
            "ARTIFACT-CHANGED",
        ),
    ),
)
def test_digest_changes_when_declared_identity_changes(
    ingestion_id: str,
    artifact_id: str,
) -> None:
    baseline = digest_knowledge_ingestion_registry(
        registry=create_registry(
            create_record(),
        ),
    )

    changed = digest_knowledge_ingestion_registry(
        registry=create_registry(
            create_record(
                ingestion_id=ingestion_id,
                artifact_id=artifact_id,
            ),
        ),
    )

    assert changed != baseline


def test_digest_preserves_unicode_utf8_semantics() -> None:
    registry = create_registry(
        create_record(
            ingestion_id="INGESTIÓN-Ñ",
            artifact_id="ARTEFACTO-CAFÉ",
            source_id="FUENTE-NIÑEZ",
        ),
    )

    payload = serialize_knowledge_ingestion_registry(
        registry=registry,
    )

    observed = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    expected = hashlib.sha256(
        payload.encode(
            "utf-8",
        )
    ).hexdigest()

    assert observed.value == expected


@pytest.mark.parametrize(
    "invalid_registry",
    (
        None,
        {},
        (),
        "registry",
    ),
)
def test_digest_rejects_untyped_registry(
    invalid_registry: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistry",
    ):
        digest_knowledge_ingestion_registry(
            registry=invalid_registry,
        )


def test_digest_does_not_mutate_registry() -> None:
    registry = create_registry(
        create_record(),
    )

    before = registry.records

    digest_knowledge_ingestion_registry(
        registry=registry,
    )

    assert registry.records == before


def test_digest_makes_no_authenticity_or_authority_claim() -> None:
    digest = digest_knowledge_ingestion_registry(
        registry=create_registry(),
    )

    for attribute in (
        "signature",
        "signer",
        "authenticity",
        "authority",
        "verified",
        "approved",
        "trust",
        "legal_status",
        "customer_acceptance",
    ):
        assert not hasattr(
            digest,
            attribute,
        )
