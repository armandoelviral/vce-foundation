from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_DOMAIN,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)


def project_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
    *,
    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
) -> dict[str, object]:
    """Project one validated Merkle checkpoint to its canonical document."""

    if not isinstance(
        checkpoint,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
    ):
        raise TypeError(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        )

    root = checkpoint.root

    return {
        "domain": SECURITY_ADMISSION_MERKLE_CHECKPOINT_DOMAIN,
        "origin": checkpoint.origin,
        "root": {
            "algorithm": root.algorithm,
            "tree_hash_profile": root.tree_hash_profile,
            "leaf_count": root.leaf_count,
            "value": root.value,
        },
    }
