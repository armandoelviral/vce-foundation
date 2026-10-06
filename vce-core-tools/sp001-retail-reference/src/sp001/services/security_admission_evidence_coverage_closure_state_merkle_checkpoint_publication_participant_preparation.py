from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation:
    """Bind one participant to its exact durable prepared state."""

    participant_id: str
    publication_state: PublicationState

    def __post_init__(self) -> None:
        if type(self.participant_id) is not str:
            raise TypeError(
                "participant_id must be a string"
            )
        if not self.participant_id.strip():
            raise ValueError(
                "participant_id must not be blank"
            )

        if not isinstance(
            self.publication_state,
            PublicationState,
        ):
            raise TypeError(
                "publication_state must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState"
            )

        if (
            self.publication_state.phase
            is not Phase.PREPARED
        ):
            raise ValueError(
                "publication_state must be in "
                "PREPARED phase"
            )
