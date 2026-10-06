from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)


ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)


def verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_set(
    *,
    participant_set: ParticipantSet,
    preparation_set: PreparationSet,
) -> bool:
    """Verify exact preparation coverage of the canonical participant set."""

    if not isinstance(
        participant_set,
        ParticipantSet,
    ):
        raise TypeError(
            "participant_set must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet"
        )

    if not isinstance(
        preparation_set,
        PreparationSet,
    ):
        raise TypeError(
            "preparation_set must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet"
        )

    participant_ids = tuple(
        participant.participant_id
        for participant
        in participant_set.participants
    )
    prepared_participant_ids = tuple(
        preparation.participant_id
        for preparation
        in preparation_set.preparations
    )

    return (
        prepared_participant_ids
        == participant_ids
    )
