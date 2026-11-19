"""Contract-only tests for PRODUCT-001 documentary commitments."""

from dataclasses import FrozenInstanceError, replace
import hashlib

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
    Product001DocumentaryCommitmentResult,
    Product001DocumentaryCommitmentStatus,
)


def make_identity(content=b"original planogram"):
    return KnowledgeSourceIdentity(
        source_id="POG-001",
        source_version="current",
        source_content_digest=KnowledgeContentDigest(
            algorithm="SHA-256",
            value=hashlib.sha256(content).hexdigest(),
        ),
    )


def make_key(content=b"original planogram"):
    return Product001DocumentaryCommitmentKey(
        organization_id="RETAIL-GROUP-GLOBAL",
        source_identity=make_identity(content),
    )


def test_key_preserves_existing_source_identity():
    identity = make_identity()

    key = Product001DocumentaryCommitmentKey(
        organization_id="RETAIL-GROUP-GLOBAL",
        source_identity=identity,
    )

    assert key.source_identity is identity


def test_exclusive_identity_excludes_content_digest():
    original = make_key(b"original")
    changed = make_key(b"changed")

    assert original.exclusive_identity == changed.exclusive_identity
    assert (
        original.source_identity.source_content_digest
        != changed.source_identity.source_content_digest
    )


@pytest.mark.parametrize("organization_id", ["", " ", "\t"])
def test_empty_organization_is_rejected(organization_id):
    with pytest.raises(ValueError):
        Product001DocumentaryCommitmentKey(
            organization_id=organization_id,
            source_identity=make_identity(),
        )


def test_invalid_source_identity_is_rejected():
    with pytest.raises(TypeError):
        Product001DocumentaryCommitmentKey(
            organization_id="RETAIL-GROUP-GLOBAL",
            source_identity=object(),
        )


def test_commitment_result_preserves_positive_facts():
    key = make_key()

    result = Product001DocumentaryCommitmentResult(
        key=key,
        status=Product001DocumentaryCommitmentStatus.CREATED,
        bytes_committed=len(b"original planogram"),
    )

    assert result.key is key
    assert result.status is Product001DocumentaryCommitmentStatus.CREATED
    assert result.bytes_committed == len(b"original planogram")


def test_zero_byte_document_is_representable():
    result = Product001DocumentaryCommitmentResult(
        key=make_key(b""),
        status=Product001DocumentaryCommitmentStatus.CREATED,
        bytes_committed=0,
    )

    assert result.bytes_committed == 0


@pytest.mark.parametrize("invalid_count", [-1, True, 1.5, "10"])
def test_invalid_byte_count_is_rejected(invalid_count):
    with pytest.raises(ValueError):
        Product001DocumentaryCommitmentResult(
            key=make_key(),
            status=Product001DocumentaryCommitmentStatus.CREATED,
            bytes_committed=invalid_count,
        )


def test_invalid_commitment_status_is_rejected():
    with pytest.raises(TypeError):
        Product001DocumentaryCommitmentResult(
            key=make_key(),
            status="CREATED",
            bytes_committed=1,
        )


def test_commitment_contract_is_immutable():
    key = make_key()

    with pytest.raises(FrozenInstanceError):
        key.organization_id = "OTHER-ORGANIZATION"


def test_result_cannot_claim_admission_authority():
    result = Product001DocumentaryCommitmentResult(
        key=make_key(),
        status=Product001DocumentaryCommitmentStatus.CREATED,
        bytes_committed=1,
    )

    assert not hasattr(result, "decision_status")
    assert not hasattr(result, "authorization")
    assert not hasattr(result, "admission_status")
