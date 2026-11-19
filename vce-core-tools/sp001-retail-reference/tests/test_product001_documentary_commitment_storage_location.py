"""Tests for exclusive documentary commitment locations."""

import hashlib
from pathlib import Path

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.contracts.product001_documentary_commitment_storage_location import (
    Product001DocumentaryCommitmentStorageLocation,
)


def make_key(
    content=b"original",
    organization="ORG",
    source="POG-001",
    version="v1",
):
    return Product001DocumentaryCommitmentKey(
        organization_id=organization,
        source_identity=KnowledgeSourceIdentity(
            source_id=source,
            source_version=version,
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value=hashlib.sha256(content).hexdigest(),
            ),
        ),
    )


def test_same_identity_produces_same_path(tmp_path):
    first = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key(b"original")
    )
    second = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key(b"modified")
    )

    assert first.artifact_path == second.artifact_path


def test_different_identity_produces_different_path(tmp_path):
    first = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key()
    )
    second = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key(version="v2")
    )

    assert first.artifact_path != second.artifact_path


@pytest.mark.parametrize(
    "source",
    ["../escape", "a/b", "á/文", "..", "/absolute"],
)
def test_untrusted_source_cannot_escape_root(tmp_path, source):
    location = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key(source=source)
    )

    assert location.artifact_path.parent == tmp_path
    assert location.artifact_path.name.startswith("doc-")
    assert location.artifact_path.suffix == ".bin"


def test_invalid_root_is_rejected():
    with pytest.raises(ValueError):
        Product001DocumentaryCommitmentStorageLocation(
            Path("relative"), make_key()
        )


@pytest.mark.parametrize(
    "changed",
    [
        {"organization": "ORG-2"},
        {"source": "POG-002"},
        {"version": "v2"},
    ],
)
def test_each_exclusive_identity_dimension_changes_path(
    tmp_path, changed
):
    original = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key()
    )
    modified = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key(**changed)
    )

    assert original.artifact_path != modified.artifact_path


def test_length_prefix_prevents_identity_ambiguity(tmp_path):
    first = Product001DocumentaryCommitmentStorageLocation(
        tmp_path,
        make_key(
            organization="a",
            source="bc",
            version="d",
        ),
    )
    second = Product001DocumentaryCommitmentStorageLocation(
        tmp_path,
        make_key(
            organization="ab",
            source="c",
            version="d",
        ),
    )

    assert first.artifact_path != second.artifact_path


def test_location_contract_does_not_mutate_filesystem(tmp_path):
    location = Product001DocumentaryCommitmentStorageLocation(
        tmp_path, make_key()
    )

    assert not location.artifact_path.exists()
    assert list(tmp_path.iterdir()) == []
