from dataclasses import dataclass

import hashlib
import hmac
import re

from sp001.services.security_admission_evidence_coverage_closure_state_digest_manifest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_root import (
    SECURITY_ADMISSION_MERKLE_LEAF_PREFIX,
    SECURITY_ADMISSION_MERKLE_NODE_PREFIX,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    _merkle_tree_hash,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_non_negative_uint64,
    validate_security_admission_positive_uint64,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof:
    """Immutable RFC6962 audit path for one ordered manifest entry."""

    leaf_index: int
    leaf_count: int
    audit_path: tuple[str, ...]

    def __post_init__(self) -> None:
        validate_security_admission_non_negative_uint64(
            value=self.leaf_index,
            field="leaf_index",
        )
        validate_security_admission_positive_uint64(
            value=self.leaf_count,
            field="leaf_count",
        )
        if self.leaf_index >= self.leaf_count:
            raise ValueError(
                "leaf_index must be less than leaf_count"
            )
        if not isinstance(self.audit_path, tuple):
            raise TypeError("audit_path must be an immutable tuple")

        for value in self.audit_path:
            if (
                not isinstance(value, str)
                or re.fullmatch(r"[0-9a-f]{64}", value) is None
            ):
                raise ValueError(
                    "audit_path must contain 64-character "
                    "lowercase hexadecimal hashes"
                )


def build_security_admission_evidence_coverage_closure_state_merkle_inclusion_proof(
    *,
    manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    leaf_index: int,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof:
    """Build the RFC6962 audit path for one manifest position."""

    if not isinstance(
        manifest,
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    ):
        raise TypeError(
            "manifest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifest"
        )

    validate_security_admission_non_negative_uint64(
        value=leaf_index,
        field="leaf_index",
    )
    if leaf_index >= len(manifest.entries):
        raise ValueError(
            "leaf_index must identify one manifest entry"
        )

    leaf_values = tuple(
        bytes.fromhex(entry.digest.value)
        for entry in manifest.entries
    )
    audit_path = tuple(
        value.hex()
        for value in _inclusion_path(
            leaf_values,
            leaf_index,
        )
    )

    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof(
            leaf_index=leaf_index,
            leaf_count=len(leaf_values),
            audit_path=audit_path,
        )
    )


def verify_security_admission_evidence_coverage_closure_state_merkle_inclusion(
    *,
    entry: SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
    proof: SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof,
    root: SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
) -> bool:
    """Verify one entry and audit path against one exact Merkle root."""

    if not isinstance(
        entry,
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
    ):
        raise TypeError(
            "entry must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry"
        )
    if not isinstance(
        proof,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof,
    ):
        raise TypeError(
            "proof must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleInclusionProof"
        )
    if not isinstance(
        root,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    ):
        raise TypeError(
            "root must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot"
        )

    if proof.leaf_count != root.leaf_count:
        return False

    leaf_hash = hashlib.sha256(
        SECURITY_ADMISSION_MERKLE_LEAF_PREFIX
        + bytes.fromhex(entry.digest.value)
    ).digest()

    try:
        rebuilt, consumed = _rebuild_root(
            leaf_hash=leaf_hash,
            leaf_index=proof.leaf_index,
            leaf_count=proof.leaf_count,
            audit_path=proof.audit_path,
            path_index=0,
        )
    except ValueError:
        return False

    if consumed != len(proof.audit_path):
        return False

    return hmac.compare_digest(
        rebuilt.hex(),
        root.value,
    )


def _inclusion_path(
    leaf_values: tuple[bytes, ...],
    leaf_index: int,
) -> tuple[bytes, ...]:
    if len(leaf_values) == 1:
        return ()

    split = 1 << ((len(leaf_values) - 1).bit_length() - 1)

    if leaf_index < split:
        return (
            *_inclusion_path(
                leaf_values[:split],
                leaf_index,
            ),
            _merkle_tree_hash(leaf_values[split:]),
        )

    return (
        *_inclusion_path(
            leaf_values[split:],
            leaf_index - split,
        ),
        _merkle_tree_hash(leaf_values[:split]),
    )


def _rebuild_root(
    *,
    leaf_hash: bytes,
    leaf_index: int,
    leaf_count: int,
    audit_path: tuple[str, ...],
    path_index: int,
) -> tuple[bytes, int]:
    if leaf_count == 1:
        return leaf_hash, path_index

    split = 1 << ((leaf_count - 1).bit_length() - 1)

    if leaf_index < split:
        child, next_index = _rebuild_root(
            leaf_hash=leaf_hash,
            leaf_index=leaf_index,
            leaf_count=split,
            audit_path=audit_path,
            path_index=path_index,
        )
        if next_index >= len(audit_path):
            raise ValueError("audit_path is incomplete")

        sibling = bytes.fromhex(audit_path[next_index])
        parent = hashlib.sha256(
            SECURITY_ADMISSION_MERKLE_NODE_PREFIX
            + child
            + sibling
        ).digest()
        return parent, next_index + 1

    child, next_index = _rebuild_root(
        leaf_hash=leaf_hash,
        leaf_index=leaf_index - split,
        leaf_count=leaf_count - split,
        audit_path=audit_path,
        path_index=path_index,
    )
    if next_index >= len(audit_path):
        raise ValueError("audit_path is incomplete")

    sibling = bytes.fromhex(audit_path[next_index])
    parent = hashlib.sha256(
        SECURITY_ADMISSION_MERKLE_NODE_PREFIX
        + sibling
        + child
    ).digest()
    return parent, next_index + 1
