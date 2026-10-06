from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent:
    """Bind one idempotent publication identity to a signed checkpoint."""

    publication_id: str
    checkpoint_signature: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.publication_id,
            str,
        ):
            raise TypeError(
                "publication_id must be a string"
            )
        if not self.publication_id:
            raise ValueError(
                "publication_id must not be empty"
            )
        if not isinstance(
            self.checkpoint_signature,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
        ):
            raise TypeError(
                "checkpoint_signature must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature"
            )
