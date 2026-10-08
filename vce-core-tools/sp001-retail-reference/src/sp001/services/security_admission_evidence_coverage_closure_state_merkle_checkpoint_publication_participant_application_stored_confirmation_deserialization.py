from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
StoredConfirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation
)
_SUPPORTED_STORAGE_SCHEMA_VERSION = 1


def deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_stored_confirmation(
    *,
    stored_confirmation: StoredConfirmation,
) -> Confirmation:
    """Reconstruct one participant application confirmation from portable data."""

    if not isinstance(
        stored_confirmation,
        StoredConfirmation,
    ):
        raise TypeError(
            "stored_confirmation must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipant"
            "ApplicationStoredConfirmation"
        )

    if (
        stored_confirmation.storage_schema_version
        != _SUPPORTED_STORAGE_SCHEMA_VERSION
    ):
        raise ValueError(
            "stored confirmation uses an unsupported "
            "storage schema version"
        )

    publication_state = (
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
            stored_state=(
                stored_confirmation.publication_state
            ),
        )
    )

    return Confirmation(
        participant_id=(
            stored_confirmation.participant_id
        ),
        decision=Decision(
            stored_confirmation.decision
        ),
        publication_state=publication_state,
    )
