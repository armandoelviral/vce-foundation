"""Canonical documentary artifact serialization tests."""

import hashlib
import json
import struct

import pytest

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)
from sp001.services.product001_documentary_commitment_serialization import (
    MAGIC,
    InvalidDocumentaryCommitmentArtifactError,
    deserialize_product001_documentary_commitment,
    serialize_product001_documentary_commitment,
)


def make_key(content):
    return Product001DocumentaryCommitmentKey(
        organization_id="RETAIL-GROUP-GLOBAL",
        source_identity=KnowledgeSourceIdentity(
            source_id="POG-001",
            source_version="v1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value=hashlib.sha256(content).hexdigest(),
            ),
        ),
    )


@pytest.mark.parametrize(
    "content",
    [
        b"",
        b"original planogram",
        b"\x00\xff\x80\x00",
        bytes(range(256)),
    ],
)
def test_round_trip_preserves_exact_bytes(content):
    key = make_key(content)

    artifact = serialize_product001_documentary_commitment(
        key=key,
        content=content,
    )

    recovered_key, recovered_content = (
        deserialize_product001_documentary_commitment(artifact)
    )

    assert recovered_key == key
    assert recovered_content == content


def test_serialization_is_deterministic():
    content = b"document"
    key = make_key(content)

    first = serialize_product001_documentary_commitment(
        key=key,
        content=content,
    )
    second = serialize_product001_documentary_commitment(
        key=key,
        content=content,
    )

    assert first == second


def test_wrong_digest_is_rejected_before_serialization():
    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        serialize_product001_documentary_commitment(
            key=make_key(b"original"),
            content=b"modified",
        )


def test_modified_content_is_rejected_during_recovery():
    content = b"original"
    artifact = serialize_product001_documentary_commitment(
        key=make_key(content),
        content=content,
    )

    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        deserialize_product001_documentary_commitment(
            artifact[:-1] + b"X"
        )


def test_truncated_metadata_is_rejected():
    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        deserialize_product001_documentary_commitment(
            MAGIC + struct.pack(">I", 100) + b"{}"
        )


def test_unknown_format_version_is_rejected():
    content = b"original"
    key = make_key(content)

    artifact = serialize_product001_documentary_commitment(
        key=key,
        content=content,
    )

    length = struct.unpack(">I", artifact[8:12])[0]
    metadata = json.loads(artifact[12:12 + length])
    metadata["format_version"] = 999

    encoded = json.dumps(
        metadata,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    altered = (
        MAGIC
        + struct.pack(">I", len(encoded))
        + encoded
        + content
    )

    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        deserialize_product001_documentary_commitment(altered)


def test_trailing_bytes_are_rejected():
    content = b"original"
    artifact = serialize_product001_documentary_commitment(
        key=make_key(content),
        content=content,
    )

    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        deserialize_product001_documentary_commitment(
            artifact + b"trailing"
        )


def test_invalid_magic_is_rejected():
    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        deserialize_product001_documentary_commitment(
            b"BADMAGIC" + b"\x00" * 20
        )


def _replace_documentary_metadata(artifact, metadata_bytes):
    original_length = struct.unpack(">I", artifact[8:12])[0]
    content = artifact[12 + original_length:]
    return (
        MAGIC
        + struct.pack(">I", len(metadata_bytes))
        + metadata_bytes
        + content
    )


def test_duplicate_metadata_keys_are_rejected():
    content = b"original"
    artifact = serialize_product001_documentary_commitment(
        key=make_key(content),
        content=content,
    )
    length = struct.unpack(">I", artifact[8:12])[0]
    metadata = artifact[12:12 + length]
    duplicate = metadata[:-1] + b',"source_id":"POG-OTHER"}'
    altered = _replace_documentary_metadata(
        artifact, duplicate
    )

    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        deserialize_product001_documentary_commitment(altered)


@pytest.mark.parametrize(
    "field,invalid_value",
    [
        ("organization_id", None),
        ("source_id", 123),
        ("source_version", False),
        ("digest_value", []),
        ("content_length", True),
        ("format_version", True),
    ],
)
def test_invalid_metadata_types_are_rejected(
    field, invalid_value
):
    content = b"original"
    artifact = serialize_product001_documentary_commitment(
        key=make_key(content),
        content=content,
    )
    length = struct.unpack(">I", artifact[8:12])[0]
    metadata = json.loads(artifact[12:12 + length])
    metadata[field] = invalid_value

    encoded = json.dumps(
        metadata,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    altered = _replace_documentary_metadata(
        artifact, encoded
    )

    with pytest.raises(
        InvalidDocumentaryCommitmentArtifactError
    ):
        deserialize_product001_documentary_commitment(altered)
