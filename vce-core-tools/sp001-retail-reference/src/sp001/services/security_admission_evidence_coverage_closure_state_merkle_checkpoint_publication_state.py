from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState:
    """Preserve one immutable, versioned checkpoint publication state."""

    publication_intent: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
    phase: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
    revision: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.publication_intent,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
        ):
            raise TypeError(
                "publication_intent must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationIntent"
            )

        if not isinstance(
            self.phase,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
        ):
            raise TypeError(
                "phase must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationPhase"
            )

        validate_security_admission_positive_uint64(
            value=self.revision,
            field="revision",
        )
