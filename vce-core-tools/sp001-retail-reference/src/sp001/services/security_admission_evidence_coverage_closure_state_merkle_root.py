from dataclasses import dataclass

import hashlib
import re

from sp001.services.security_admission_evidence_coverage_closure_state_digest_manifest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


SECURITY_ADMISSION_MERKLE_ALGORITHM = "SHA-256"
SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE = "RFC6962"
SECURITY_ADMISSION_MERKLE_LEAF_PREFIX = b"\x00"
SECURITY_ADMISSION_MERKLE_NODE_PREFIX = b"\x01"


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot:
    """Immutable commitment to one ordered digest manifest."""

    algorithm: str
    tree_hash_profile: str
    leaf_count: int
    value: str

    def __post_init__(self) -> None:
        if self.algorithm != SECURITY_ADMISSION_MERKLE_ALGORITHM:
            raise ValueError("algorithm must be SHA-256")
        if (
            self.tree_hash_profile
            != SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE
        ):
            raise ValueError("tree_hash_profile must be RFC6962")

        validate_security_admission_positive_uint64(
            value=self.leaf_count,
            field="leaf_count",
        )

        if (
            not isinstance(self.value, str)
            or re.fullmatch(r"[0-9a-f]{64}", self.value) is None
        ):
            raise ValueError(
                "value must contain 64 lowercase hexadecimal characters"
            )


def build_security_admission_evidence_coverage_closure_state_merkle_root(
    *,
    manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot:
    """Commit one validated ordered manifest to an RFC6962 tree hash."""

    if not isinstance(
        manifest,
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    ):
        raise TypeError(
            "manifest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifest"
        )

    leaf_values = tuple(
        bytes.fromhex(entry.digest.value)
        for entry in manifest.entries
    )
    root = _merkle_tree_hash(leaf_values)

    return SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot(
        algorithm=SECURITY_ADMISSION_MERKLE_ALGORITHM,
        tree_hash_profile=(
            SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE
        ),
        leaf_count=len(leaf_values),
        value=root.hex(),
    )


def _merkle_tree_hash(
    leaf_values: tuple[bytes, ...],
) -> bytes:
    if len(leaf_values) == 1:
        return hashlib.sha256(
            SECURITY_ADMISSION_MERKLE_LEAF_PREFIX
            + leaf_values[0]
        ).digest()

    split = 1 << ((len(leaf_values) - 1).bit_length() - 1)
    left = _merkle_tree_hash(leaf_values[:split])
    right = _merkle_tree_hash(leaf_values[split:])

    return hashlib.sha256(
        SECURITY_ADMISSION_MERKLE_NODE_PREFIX
        + left
        + right
    ).digest()
