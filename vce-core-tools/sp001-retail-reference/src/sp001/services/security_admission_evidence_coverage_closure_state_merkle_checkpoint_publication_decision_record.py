from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord:
    """Preserve one nominal global decision and its exact evidence graph."""

    publication_intent: PublicationIntent
    participant_set: ParticipantSet
    preparation_set: PreparationSet
    decision: Decision

    def __post_init__(self) -> None:
        if not isinstance(
            self.publication_intent,
            PublicationIntent,
        ):
            raise TypeError(
                "publication_intent must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationIntent"
            )

        if not isinstance(
            self.participant_set,
            ParticipantSet,
        ):
            raise TypeError(
                "participant_set must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationParticipantSet"
            )

        if not isinstance(
            self.preparation_set,
            PreparationSet,
        ):
            raise TypeError(
                "preparation_set must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationParticipantPreparationSet"
            )

        if not isinstance(self.decision, Decision):
            raise TypeError(
                "decision must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationDecision"
            )

        for preparation in self.preparation_set.preparations:
            retained_intent = (
                preparation
                .publication_state
                .publication_intent
            )
            if retained_intent != self.publication_intent:
                raise ValueError(
                    "preparations must retain the exact "
                    "publication intent"
                )
