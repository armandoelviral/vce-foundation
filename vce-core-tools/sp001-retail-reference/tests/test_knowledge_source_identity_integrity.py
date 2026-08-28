from dataclasses import FrozenInstanceError

import hashlib
import re

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
    verify_knowledge_source_content,
)


SOURCE_CONTENT = (
    b"canonical visual merchandising planogram bytes"
)


def create_digest(
    *,
    content: bytes = SOURCE_CONTENT,
) -> KnowledgeContentDigest:
    return digest_knowledge_source_content(
        content=content,
    )


def create_identity(
    *,
    source_id: str = "POG-2026-DENIM-012",
    source_version: str = "v1.0",
    digest: KnowledgeContentDigest | None = None,
) -> KnowledgeSourceIdentity:
    return KnowledgeSourceIdentity(
        source_id=source_id,
        source_version=source_version,
        source_content_digest=(
            digest
            if digest is not None
            else create_digest()
        ),
    )


def test_digest_declares_sha256_algorithm() -> None:
    digest = create_digest()

    assert digest.algorithm == "SHA-256"


def test_digest_contains_canonical_lowercase_hexadecimal_value() -> None:
    digest = create_digest()

    assert re.fullmatch(
        r"[0-9a-f]{64}",
        digest.value,
    )


def test_digest_matches_independent_sha256_calculation() -> None:
    digest = create_digest()

    expected = hashlib.sha256(
        SOURCE_CONTENT,
    ).hexdigest()

    assert digest.value == expected


def test_digest_is_deterministic_for_identical_bytes() -> None:
    first = create_digest()
    second = create_digest()

    assert first == second


def test_digest_changes_when_one_source_byte_changes() -> None:
    original = create_digest(
        content=b"PLANOGRAM-A",
    )
    modified = create_digest(
        content=b"PLANOGRAM-B",
    )

    assert original != modified
    assert original.value != modified.value


def test_digest_preserves_exact_byte_semantics() -> None:
    uppercase = create_digest(
        content=b"Planogram",
    )
    lowercase = create_digest(
        content=b"planogram",
    )

    assert uppercase.value != lowercase.value


def test_digest_rejects_unsupported_algorithm() -> None:
    with pytest.raises(
        ValueError,
        match="digest algorithm must be SHA-256",
    ):
        KnowledgeContentDigest(
            algorithm="SHA-512",
            value="0" * 64,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "0" * 63,
        "0" * 65,
        "A" * 64,
        "g" * 64,
        123,
    ),
)
def test_digest_rejects_noncanonical_value(
    invalid_value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        ),
    ):
        KnowledgeContentDigest(
            algorithm="SHA-256",
            value=invalid_value,
        )


def test_digest_is_immutable() -> None:
    digest = create_digest()

    with pytest.raises(FrozenInstanceError):
        digest.value = "0" * 64


def test_identity_preserves_source_version_and_digest() -> None:
    digest = create_digest()
    identity = create_identity(
        digest=digest,
    )

    assert identity.source_id == "POG-2026-DENIM-012"
    assert identity.source_version == "v1.0"
    assert identity.source_content_digest is digest


@pytest.mark.parametrize(
    "field, value",
    (
        ("source_id", ""),
        ("source_id", " "),
        ("source_id", None),
        ("source_version", ""),
        ("source_version", " "),
        ("source_version", 1),
    ),
)
def test_identity_rejects_empty_identity_fields(
    field: str,
    value: object,
) -> None:
    values = {
        "source_id": "POG-2026-DENIM-012",
        "source_version": "v1.0",
        "digest": create_digest(),
    }

    if field == "source_id":
        values["source_id"] = value
    else:
        values["source_version"] = value

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_identity(
            source_id=values["source_id"],
            source_version=values["source_version"],
            digest=values["digest"],
        )


def test_identity_rejects_untyped_digest() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_content_digest must be a "
            "KnowledgeContentDigest"
        ),
    ):
        create_identity(
            digest="sha256-value",
        )


def test_identity_is_immutable() -> None:
    identity = create_identity()

    with pytest.raises(FrozenInstanceError):
        identity.source_version = "v2.0"


def test_same_source_version_with_different_bytes_remains_distinct() -> None:
    first = create_identity(
        digest=create_digest(
            content=b"ORIGINAL",
        ),
    )
    second = create_identity(
        digest=create_digest(
            content=b"MODIFIED",
        ),
    )

    assert first.source_id == second.source_id
    assert first.source_version == second.source_version
    assert first != second


def test_different_source_versions_can_preserve_identical_bytes() -> None:
    digest = create_digest()

    version_one = create_identity(
        source_version="v1.0",
        digest=digest,
    )
    version_two = create_identity(
        source_version="v2.0",
        digest=digest,
    )

    assert (
        version_one.source_content_digest
        == version_two.source_content_digest
    )
    assert version_one != version_two


def test_verification_accepts_matching_source_bytes() -> None:
    identity = create_identity()

    assert (
        verify_knowledge_source_content(
            identity=identity,
            content=SOURCE_CONTENT,
        )
        is True
    )


def test_verification_rejects_modified_source_bytes() -> None:
    identity = create_identity()

    assert (
        verify_knowledge_source_content(
            identity=identity,
            content=SOURCE_CONTENT + b"-modified",
        )
        is False
    )


def test_integrity_rejects_untyped_identity() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "identity must be a "
            "KnowledgeSourceIdentity"
        ),
    ):
        verify_knowledge_source_content(
            identity="POG-2026-DENIM-012",
            content=SOURCE_CONTENT,
        )


@pytest.mark.parametrize(
    "invalid_content",
    (
        "text",
        bytearray(b"mutable"),
        memoryview(b"view"),
        None,
    ),
)
def test_integrity_rejects_non_byte_content(
    invalid_content: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="content must be immutable bytes",
    ):
        digest_knowledge_source_content(
            content=invalid_content,
        )


def test_integrity_rejects_empty_content() -> None:
    with pytest.raises(
        ValueError,
        match="content must not be empty",
    ):
        digest_knowledge_source_content(
            content=b"",
        )


def test_verification_does_not_mutate_identity() -> None:
    identity = create_identity()
    original_digest = identity.source_content_digest

    verify_knowledge_source_content(
        identity=identity,
        content=SOURCE_CONTENT,
    )

    assert identity.source_content_digest is original_digest


def test_identity_and_digest_do_not_claim_authenticity_or_authority() -> None:
    identity = create_identity()

    for target in (
        identity,
        identity.source_content_digest,
    ):
        for attribute in (
            "signature",
            "signer",
            "authentic",
            "authority",
            "approved",
            "evidence_status",
            "lifecycle_status",
            "customer_id",
            "organization_id",
            "effective_from",
            "effective_until",
        ):
            assert not hasattr(
                target,
                attribute,
            )
