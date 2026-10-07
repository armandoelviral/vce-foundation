from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
ParticipantPreparation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)
ParticipantPreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
PublicationPhase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)


def collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations(
    *,
    publication_intent: PublicationIntent,
    participant_set: ParticipantSet,
) -> ParticipantPreparationSet:
    """Collect only exact PREPARED evidence from the canonical participants."""

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

    preparations: list[ParticipantPreparation] = []

    for participant in participant_set.participants:
        try:
            publication_state = participant.prepare(
                publication_intent=publication_intent,
            )
        except Exception:
            continue

        if not isinstance(
            publication_state,
            PublicationState,
        ):
            continue

        if (
            publication_state.publication_intent
            != publication_intent
        ):
            continue

        if (
            publication_state.phase
            is not PublicationPhase.PREPARED
        ):
            continue

        preparations.append(
            ParticipantPreparation(
                participant_id=participant.participant_id,
                publication_state=publication_state,
            )
        )

    return ParticipantPreparationSet(
        preparations=tuple(preparations),
    )
