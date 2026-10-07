from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)
_STORAGE_SCHEMA_VERSION = 1


def project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
    *,
    confirmation: Confirmation,
) -> StoredConfirmation:
    """Project one participant application confirmation into portable values."""

    if not isinstance(
        confirmation,
        Confirmation,
    ):
        raise TypeError(
            "confirmation must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipant"
            "ApplicationConfirmation"
        )

    return StoredConfirmation(
        storage_schema_version=_STORAGE_SCHEMA_VERSION,
        participant_id=confirmation.participant_id,
        decision=confirmation.decision.value,
        publication_state=(
            project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
                state=confirmation.publication_state,
            )
        ),
    )
