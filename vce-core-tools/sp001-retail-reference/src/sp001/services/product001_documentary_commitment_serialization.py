"""Canonical binary representation of original documentary bytes."""

import hashlib
import json
import struct

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.product001_documentary_commitment import (
    Product001DocumentaryCommitmentKey,
)


MAGIC = b"P1DOC001"
FORMAT_VERSION = 1
MAX_METADATA_LENGTH = 65536


class InvalidDocumentaryCommitmentArtifactError(ValueError):
    """Invalid or noncanonical documentary artifact."""


def _canonical_metadata(metadata: dict) -> bytes:
    return json.dumps(
        metadata,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def serialize_product001_documentary_commitment(
    *,
    key: Product001DocumentaryCommitmentKey,
    content: bytes,
) -> bytes:
    if not isinstance(key, Product001DocumentaryCommitmentKey):
        raise TypeError(
            "key must be a Product001DocumentaryCommitmentKey"
        )

    if type(content) is not bytes:
        raise TypeError("content must be bytes")

    identity = key.source_identity

    actual_digest = hashlib.sha256(content).hexdigest()

    if actual_digest != identity.source_content_digest.value:
        raise InvalidDocumentaryCommitmentArtifactError(
            "documentary content digest mismatch"
        )

    metadata = {
        "format_version": FORMAT_VERSION,
        "organization_id": key.organization_id,
        "source_id": identity.source_id,
        "source_version": identity.source_version,
        "digest_algorithm": identity.source_content_digest.algorithm,
        "digest_value": identity.source_content_digest.value,
        "content_length": len(content),
    }

    metadata_bytes = _canonical_metadata(metadata)

    if len(metadata_bytes) > MAX_METADATA_LENGTH:
        raise InvalidDocumentaryCommitmentArtifactError(
            "metadata exceeds maximum length"
        )

    return (
        MAGIC
        + struct.pack(">I", len(metadata_bytes))
        + metadata_bytes
        + content
    )


def deserialize_product001_documentary_commitment(
    artifact: bytes,
) -> tuple[Product001DocumentaryCommitmentKey, bytes]:
    if type(artifact) is not bytes:
        raise TypeError("artifact must be bytes")

    if len(artifact) < 12 or artifact[:8] != MAGIC:
        raise InvalidDocumentaryCommitmentArtifactError(
            "invalid documentary artifact header"
        )

    metadata_length = struct.unpack(">I", artifact[8:12])[0]

    if metadata_length > MAX_METADATA_LENGTH:
        raise InvalidDocumentaryCommitmentArtifactError(
            "metadata exceeds maximum length"
        )

    metadata_end = 12 + metadata_length

    if metadata_end > len(artifact):
        raise InvalidDocumentaryCommitmentArtifactError(
            "truncated metadata"
        )

    metadata_bytes = artifact[12:metadata_end]
    content = artifact[metadata_end:]

    try:
        metadata = json.loads(metadata_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise InvalidDocumentaryCommitmentArtifactError(
            "invalid metadata encoding"
        ) from error

    if type(metadata) is not dict:
        raise InvalidDocumentaryCommitmentArtifactError(
            "metadata must be an object"
        )

    expected_fields = {
        "format_version",
        "organization_id",
        "source_id",
        "source_version",
        "digest_algorithm",
        "digest_value",
        "content_length",
    }

    if set(metadata) != expected_fields:
        raise InvalidDocumentaryCommitmentArtifactError(
            "invalid metadata fields"
        )

    if _canonical_metadata(metadata) != metadata_bytes:
        raise InvalidDocumentaryCommitmentArtifactError(
            "noncanonical metadata"
        )

    if type(metadata["format_version"]) is not int or (
        metadata["format_version"] != FORMAT_VERSION
    ):
        raise InvalidDocumentaryCommitmentArtifactError(
            "unsupported format version"
        )

    if (
        type(metadata["content_length"]) is not int
        or metadata["content_length"] != len(content)
    ):
        raise InvalidDocumentaryCommitmentArtifactError(
            "documentary content length mismatch"
        )

    try:
        identity = KnowledgeSourceIdentity(
            source_id=metadata["source_id"],
            source_version=metadata["source_version"],
            source_content_digest=KnowledgeContentDigest(
                algorithm=metadata["digest_algorithm"],
                value=metadata["digest_value"],
            ),
        )

        key = Product001DocumentaryCommitmentKey(
            organization_id=metadata["organization_id"],
            source_identity=identity,
        )
    except (TypeError, ValueError) as error:
        raise InvalidDocumentaryCommitmentArtifactError(
            "invalid documentary identity"
        ) from error

    actual_digest = hashlib.sha256(content).hexdigest()

    if actual_digest != identity.source_content_digest.value:
        raise InvalidDocumentaryCommitmentArtifactError(
            "documentary content digest mismatch"
        )

    return key, content
