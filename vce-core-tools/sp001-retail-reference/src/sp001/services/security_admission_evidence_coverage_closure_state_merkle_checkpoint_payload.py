from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_serialization import (
    serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)


SECURITY_ADMISSION_MERKLE_CHECKPOINT_ENCODING = "UTF-8"


def canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
    *,
    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
) -> bytes:
    """Return exact canonical bytes for one validated Merkle checkpoint."""

    if not isinstance(
        checkpoint,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
    ):
        raise TypeError(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        )

    payload = (
        serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )

    return payload.encode(
        SECURITY_ADMISSION_MERKLE_CHECKPOINT_ENCODING,
    )
