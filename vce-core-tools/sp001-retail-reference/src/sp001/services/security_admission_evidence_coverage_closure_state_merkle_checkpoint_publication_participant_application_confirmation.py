from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation:
    """Preserve one participant's confirmed application of a global decision."""

    participant_id: str
    decision: Decision
    publication_state: PublicationState

    def __post_init__(self) -> None:
        if type(self.participant_id) is not str:
            raise TypeError(
                "participant_id must be a string"
            )
        if not self.participant_id:
            raise ValueError(
                "participant_id must not be empty"
            )

        if not isinstance(self.decision, Decision):
            raise TypeError(
                "decision must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationDecision"
            )

        if not isinstance(
            self.publication_state,
            PublicationState,
        ):
            raise TypeError(
                "publication_state must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationState"
            )

        expected_phase = (
            Phase.COMMITTED
            if self.decision is Decision.COMMIT
            else Phase.ABORTED
        )
        if self.publication_state.phase is not expected_phase:
            raise ValueError(
                "publication_state phase must confirm "
                "the retained publication decision"
            )
