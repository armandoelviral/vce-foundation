import pytest

from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
    digest_knowledge_ingestion_registry,
)
from sp001.services.knowledge_ingestion_registry_digest_verification import (
    verify_knowledge_ingestion_registry_digest,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def test_verification_accepts_matching_registry_digest() -> None:
    registry = create_registry(
        create_record(),
    )

    digest = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    assert verify_knowledge_ingestion_registry_digest(
        registry=registry,
        digest=digest,
    )


def test_verification_accepts_equivalent_registry() -> None:
    original = create_registry(
        create_record(),
    )

    equivalent = create_registry(
        create_record(),
    )

    digest = digest_knowledge_ingestion_registry(
        registry=original,
    )

    assert original is not equivalent

    assert verify_knowledge_ingestion_registry_digest(
        registry=equivalent,
        digest=digest,
    )


def test_verification_rejects_nonmatching_registry_content() -> None:
    original = create_registry(
        create_record(),
    )

    changed = create_registry(
        create_record(
            ingestion_id="INGESTION-CHANGED",
        ),
    )

    digest = digest_knowledge_ingestion_registry(
        registry=original,
    )

    assert not verify_knowledge_ingestion_registry_digest(
        registry=changed,
        digest=digest,
    )


def test_verification_rejects_nonmatching_record_order() -> None:
    record_a = create_record(
        ingestion_id="INGESTION-A",
        artifact_id="ARTIFACT-A",
    )

    record_b = create_record(
        ingestion_id="INGESTION-B",
        artifact_id="ARTIFACT-B",
    )

    forward = create_registry(
        record_a,
        record_b,
    )

    reverse = create_registry(
        record_b,
        record_a,
    )

    digest = digest_knowledge_ingestion_registry(
        registry=forward,
    )

    assert not verify_knowledge_ingestion_registry_digest(
        registry=reverse,
        digest=digest,
    )


@pytest.mark.parametrize(
    "invalid_registry",
    (
        None,
        {},
        (),
        "registry",
    ),
)
def test_verification_rejects_untyped_registry(
    invalid_registry: object,
) -> None:
    digest = digest_knowledge_ingestion_registry(
        registry=create_registry(),
    )

    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistry",
    ):
        verify_knowledge_ingestion_registry_digest(
            registry=invalid_registry,
            digest=digest,
        )


@pytest.mark.parametrize(
    "invalid_digest",
    (
        None,
        {},
        (),
        "digest",
    ),
)
def test_verification_rejects_untyped_digest(
    invalid_digest: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistryDigest",
    ):
        verify_knowledge_ingestion_registry_digest(
            registry=create_registry(),
            digest=invalid_digest,
        )


def test_verification_rejects_unsupported_algorithm() -> None:
    digest = KnowledgeIngestionRegistryDigest(
        algorithm="SHA-512",
        encoding="UTF-8",
        value="0" * 64,
    )

    with pytest.raises(
        ValueError,
        match="algorithm must be SHA-256",
    ):
        verify_knowledge_ingestion_registry_digest(
            registry=create_registry(),
            digest=digest,
        )


def test_verification_rejects_unsupported_encoding() -> None:
    digest = KnowledgeIngestionRegistryDigest(
        algorithm="SHA-256",
        encoding="UTF-16",
        value="0" * 64,
    )

    with pytest.raises(
        ValueError,
        match="encoding must be UTF-8",
    ):
        verify_knowledge_ingestion_registry_digest(
            registry=create_registry(),
            digest=digest,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        "",
        "0" * 63,
        "0" * 65,
        "G" * 64,
        "A" * 64,
        123,
    ),
)
def test_verification_rejects_invalid_digest_value(
    invalid_value: object,
) -> None:
    digest = KnowledgeIngestionRegistryDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=invalid_value,
    )

    with pytest.raises(
        ValueError,
        match="64 lowercase hexadecimal characters",
    ):
        verify_knowledge_ingestion_registry_digest(
            registry=create_registry(),
            digest=digest,
        )


def test_verification_returns_boolean_result() -> None:
    registry = create_registry()

    digest = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    result = verify_knowledge_ingestion_registry_digest(
        registry=registry,
        digest=digest,
    )

    assert result is True


def test_verification_does_not_mutate_inputs() -> None:
    registry = create_registry(
        create_record(),
    )

    digest = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    records_before = registry.records
    digest_before = digest

    verify_knowledge_ingestion_registry_digest(
        registry=registry,
        digest=digest,
    )

    assert registry.records == records_before
    assert digest == digest_before


def test_success_establishes_no_authenticity_or_authority() -> None:
    registry = create_registry()

    digest = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    assert verify_knowledge_ingestion_registry_digest(
        registry=registry,
        digest=digest,
    )

    for attribute in (
        "signature",
        "signer",
        "authenticity",
        "authority",
        "approved",
        "legal_status",
        "customer_acceptance",
    ):
        assert not hasattr(
            digest,
            attribute,
        )
