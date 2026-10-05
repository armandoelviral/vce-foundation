import json

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)


def serialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
    *,
    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
) -> str:
    """Serialize one validated Merkle checkpoint to canonical JSON text."""

    if not isinstance(
        checkpoint,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
    ):
        raise TypeError(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        )

    document = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
        )
    )

    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
