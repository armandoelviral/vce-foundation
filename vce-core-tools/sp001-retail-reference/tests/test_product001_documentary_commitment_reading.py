"""Contract tests for documentary commitment reading."""

from dataclasses import FrozenInstanceError
import hashlib

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_documentary_commitment_reading import (
    Product001DocumentaryCommitmentReadResult,
    Product001DocumentaryCommitmentReadStatus,
)


def make_key(content=b"document"):
    return Product001DocumentaryCommitmentKey(
        organization_id="org-1",
        source_identity=KnowledgeSourceIdentity(
            source_id="planogram-1",
            source_version="v1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value=hashlib.sha256(content).hexdigest(),
            ),
        ),
    )


def test_present_requires_bytes():
    key = make_key()
    result = Product001DocumentaryCommitmentReadResult(
        key=key,
        status=Product001DocumentaryCommitmentReadStatus.PRESENT,
        content=b"document",
    )
    assert result.content == b"document"

    with pytest.raises(TypeError):
        Product001DocumentaryCommitmentReadResult(
            key=key,
            status=Product001DocumentaryCommitmentReadStatus.PRESENT,
        )


@pytest.mark.parametrize(
    "status",
    [
        Product001DocumentaryCommitmentReadStatus.ABSENT,
        Product001DocumentaryCommitmentReadStatus.CONFLICT,
        Product001DocumentaryCommitmentReadStatus.INVALID,
        Product001DocumentaryCommitmentReadStatus.IO_FAILURE,
    ],
)
def test_negative_status_rejects_content(status):
    with pytest.raises(ValueError):
        Product001DocumentaryCommitmentReadResult(
            key=make_key(),
            status=status,
            content=b"document",
        )


@pytest.mark.parametrize(
    "status",
    [
        Product001DocumentaryCommitmentReadStatus.ABSENT,
        Product001DocumentaryCommitmentReadStatus.CONFLICT,
        Product001DocumentaryCommitmentReadStatus.INVALID,
        Product001DocumentaryCommitmentReadStatus.IO_FAILURE,
    ],
)
def test_negative_status_allows_no_content(status):
    result = Product001DocumentaryCommitmentReadResult(
        key=make_key(),
        status=status,
    )
    assert result.content is None


def test_rejects_invalid_key_and_status():
    with pytest.raises(TypeError):
        Product001DocumentaryCommitmentReadResult(
            key="not-a-key",
            status=Product001DocumentaryCommitmentReadStatus.ABSENT,
        )

    with pytest.raises(TypeError):
        Product001DocumentaryCommitmentReadResult(
            key=make_key(),
            status="PRESENT",
            content=b"document",
        )


def test_result_is_immutable_and_slotted():
    result = Product001DocumentaryCommitmentReadResult(
        key=make_key(),
        status=Product001DocumentaryCommitmentReadStatus.ABSENT,
    )

    assert not hasattr(result, "__dict__")

    with pytest.raises(FrozenInstanceError):
        result.content = b"changed"


def test_result_has_no_admission_authority():
    fields = set(
        Product001DocumentaryCommitmentReadResult.__dataclass_fields__
    )
    assert fields == {"key", "status", "content"}
