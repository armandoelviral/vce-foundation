from dataclasses import dataclass
import hashlib
import hmac
import re

from sp001.services.security_admission_evidence_coverage_closure_state_digest_manifest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_root import (
    SECURITY_ADMISSION_MERKLE_ALGORITHM,
    SECURITY_ADMISSION_MERKLE_NODE_PREFIX,
    SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    _merkle_tree_hash,
)


_PORTABLE_UINT64_MAX = (1 << 64) - 1
_DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof:
    """Prove that one Merkle tree is an exact prefix of a later tree."""

    old_leaf_count: int
    new_leaf_count: int
    audit_path: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_positive_uint64(
            self.old_leaf_count,
            field="old_leaf_count",
        )
        _validate_positive_uint64(
            self.new_leaf_count,
            field="new_leaf_count",
        )

        if self.old_leaf_count >= self.new_leaf_count:
            raise ValueError(
                "old_leaf_count must be less than new_leaf_count"
            )

        if not isinstance(self.audit_path, tuple):
            raise TypeError("audit_path must be a tuple")

        if not self.audit_path:
            raise ValueError("audit_path must not be empty")

        for value in self.audit_path:
            if (
                not isinstance(value, str)
                or _DIGEST_PATTERN.fullmatch(value) is None
            ):
                raise ValueError(
                    "audit_path values must contain "
                    "64 lowercase hexadecimal characters"
                )


def build_security_admission_evidence_coverage_closure_state_merkle_consistency_proof(
    *,
    old_manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    new_manifest: SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof:
    """Build a proof that new_manifest strictly extends old_manifest."""

    if not isinstance(
        old_manifest,
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    ):
        raise TypeError(
            "old_manifest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifest"
        )
    if not isinstance(
        new_manifest,
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifest,
    ):
        raise TypeError(
            "new_manifest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigestManifest"
        )

    old_leaf_count = len(old_manifest.entries)
    new_leaf_count = len(new_manifest.entries)

    if old_leaf_count >= new_leaf_count:
        raise ValueError(
            "old_manifest must contain fewer entries than new_manifest"
        )

    if (
        old_manifest.entries
        != new_manifest.entries[:old_leaf_count]
    ):
        raise ValueError(
            "old_manifest must be an exact ordered prefix "
            "of new_manifest"
        )

    leaf_values = tuple(
        bytes.fromhex(entry.digest.value)
        for entry in new_manifest.entries
    )

    audit_path = _consistency_path(
        leaf_values=leaf_values,
        old_leaf_count=old_leaf_count,
        include_old_root=True,
    )

    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof(
            old_leaf_count=old_leaf_count,
            new_leaf_count=new_leaf_count,
            audit_path=tuple(
                value.hex()
                for value in audit_path
            ),
        )
    )


def verify_security_admission_evidence_coverage_closure_state_merkle_consistency(
    *,
    old_root: SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    new_root: SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    proof: SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof,
) -> bool:
    """Verify strict append-only consistency between two Merkle roots."""

    if not isinstance(
        old_root,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    ):
        raise TypeError(
            "old_root must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot"
        )
    if not isinstance(
        new_root,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
    ):
        raise TypeError(
            "new_root must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot"
        )
    if not isinstance(
        proof,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof,
    ):
        raise TypeError(
            "proof must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleConsistencyProof"
        )

    if (
        old_root.algorithm
        != SECURITY_ADMISSION_MERKLE_ALGORITHM
        or new_root.algorithm
        != SECURITY_ADMISSION_MERKLE_ALGORITHM
        or old_root.tree_hash_profile
        != SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE
        or new_root.tree_hash_profile
        != SECURITY_ADMISSION_MERKLE_TREE_HASH_PROFILE
    ):
        return False

    if (
        old_root.leaf_count != proof.old_leaf_count
        or new_root.leaf_count != proof.new_leaf_count
    ):
        return False

    try:
        old_root_hash = bytes.fromhex(old_root.value)
        new_root_hash = bytes.fromhex(new_root.value)
        audit_path = tuple(
            bytes.fromhex(value)
            for value in proof.audit_path
        )

        rebuilt_old_root, rebuilt_new_root, path_index = (
            _rebuild_consistent_roots(
                old_leaf_count=proof.old_leaf_count,
                new_leaf_count=proof.new_leaf_count,
                include_old_root=True,
                old_root_hash=old_root_hash,
                audit_path=audit_path,
                path_index=0,
            )
        )
    except (IndexError, ValueError):
        return False

    if path_index != len(audit_path):
        return False

    return (
        hmac.compare_digest(
            rebuilt_old_root,
            old_root_hash,
        )
        and hmac.compare_digest(
            rebuilt_new_root,
            new_root_hash,
        )
    )


def _consistency_path(
    *,
    leaf_values: tuple[bytes, ...],
    old_leaf_count: int,
    include_old_root: bool,
) -> tuple[bytes, ...]:
    new_leaf_count = len(leaf_values)

    if old_leaf_count == new_leaf_count:
        if include_old_root:
            return ()
        return (_merkle_tree_hash(leaf_values),)

    split = _largest_power_of_two_less_than(new_leaf_count)

    if old_leaf_count <= split:
        return (
            _consistency_path(
                leaf_values=leaf_values[:split],
                old_leaf_count=old_leaf_count,
                include_old_root=include_old_root,
            )
            + (
                _merkle_tree_hash(
                    leaf_values[split:],
                ),
            )
        )

    return (
        _consistency_path(
            leaf_values=leaf_values[split:],
            old_leaf_count=old_leaf_count - split,
            include_old_root=False,
        )
        + (
            _merkle_tree_hash(
                leaf_values[:split],
            ),
        )
    )


def _rebuild_consistent_roots(
    *,
    old_leaf_count: int,
    new_leaf_count: int,
    include_old_root: bool,
    old_root_hash: bytes,
    audit_path: tuple[bytes, ...],
    path_index: int,
) -> tuple[bytes, bytes, int]:
    if old_leaf_count == new_leaf_count:
        if include_old_root:
            return (
                old_root_hash,
                old_root_hash,
                path_index,
            )

        subtree_hash = audit_path[path_index]
        return (
            subtree_hash,
            subtree_hash,
            path_index + 1,
        )

    split = _largest_power_of_two_less_than(new_leaf_count)

    if old_leaf_count <= split:
        (
            rebuilt_old_root,
            rebuilt_new_left,
            path_index,
        ) = _rebuild_consistent_roots(
            old_leaf_count=old_leaf_count,
            new_leaf_count=split,
            include_old_root=include_old_root,
            old_root_hash=old_root_hash,
            audit_path=audit_path,
            path_index=path_index,
        )

        new_right = audit_path[path_index]

        return (
            rebuilt_old_root,
            _node_hash(
                rebuilt_new_left,
                new_right,
            ),
            path_index + 1,
        )

    (
        rebuilt_old_right,
        rebuilt_new_right,
        path_index,
    ) = _rebuild_consistent_roots(
        old_leaf_count=old_leaf_count - split,
        new_leaf_count=new_leaf_count - split,
        include_old_root=False,
        old_root_hash=old_root_hash,
        audit_path=audit_path,
        path_index=path_index,
    )

    left_hash = audit_path[path_index]

    return (
        _node_hash(
            left_hash,
            rebuilt_old_right,
        ),
        _node_hash(
            left_hash,
            rebuilt_new_right,
        ),
        path_index + 1,
    )


def _node_hash(
    left: bytes,
    right: bytes,
) -> bytes:
    return hashlib.sha256(
        SECURITY_ADMISSION_MERKLE_NODE_PREFIX
        + left
        + right
    ).digest()


def _largest_power_of_two_less_than(
    value: int,
) -> int:
    return 1 << ((value - 1).bit_length() - 1)


def _validate_positive_uint64(
    value: object,
    *,
    field: str,
) -> None:
    if type(value) is not int:
        raise TypeError(f"{field} must be an int")
    if value <= 0:
        raise ValueError(f"{field} must be greater than zero")
    if value > _PORTABLE_UINT64_MAX:
        raise ValueError(
            f"{field} must not exceed portable uint64 maximum"
        )
