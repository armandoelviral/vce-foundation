from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
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


def derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
    *,
    publication_intent: PublicationIntent,
    participant_set: ParticipantSet,
    preparation_set: PreparationSet,
) -> DecisionRecord:
    """Derive one fail-closed global decision from exact preparation coverage."""

    if not isinstance(
        publication_intent,
        PublicationIntent,
    ):
        raise TypeError(
            "publication_intent must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationIntent"
        )

    if not isinstance(
        participant_set,
        ParticipantSet,
    ):
        raise TypeError(
            "participant_set must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipantSet"
        )

    if not isinstance(
        preparation_set,
        PreparationSet,
    ):
        raise TypeError(
            "preparation_set must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipantPreparationSet"
        )

    exhaustive = (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set(
            participant_set=participant_set,
            preparation_set=preparation_set,
        )
    )
    if type(exhaustive) is not bool:
        raise TypeError(
            "preparation-set verification must return a bool"
        )

    decision = (
        Decision.COMMIT
        if exhaustive
        else Decision.ABORT
    )

    return DecisionRecord(
        publication_intent=publication_intent,
        participant_set=participant_set,
        preparation_set=preparation_set,
        decision=decision,
    )
