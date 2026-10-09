from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore,
)


ApplicationCompletion = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
DecisionRecordStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
ConfirmationStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore
)


def read_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion(
    *,
    decision_record_store: DecisionRecordStore,
    confirmation_store: ConfirmationStore,
    publication_id: str,
) -> ApplicationCompletion | None:
    """Reconstruct completion from the durable decision and confirmations."""

    if not isinstance(
        decision_record_store,
        DecisionRecordStore,
    ):
        raise TypeError(
            "decision_record_store must implement "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecordStore"
        )

    if not isinstance(
        confirmation_store,
        ConfirmationStore,
    ):
        raise TypeError(
            "confirmation_store must implement "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipantApplication"
            "ConfirmationStore"
        )

    if type(publication_id) is not str:
        raise TypeError(
            "publication_id must be a string"
        )
    if not publication_id:
        raise ValueError(
            "publication_id must not be empty"
        )

    decision_record = decision_record_store.read(
        publication_id=publication_id,
    )
    if decision_record is None:
        return None
    if not isinstance(
        decision_record,
        DecisionRecord,
    ):
        raise TypeError(
            "decision_record_store.read must return a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecord or None"
        )

    retained_publication_id = (
        decision_record
        .publication_intent
        .publication_id
    )
    if retained_publication_id != publication_id:
        raise ValueError(
            "durable decision record has a different "
            "publication_id"
        )

    confirmation_set = confirmation_store.read(
        publication_id=publication_id,
    )
    if not isinstance(
        confirmation_set,
        ConfirmationSet,
    ):
        raise TypeError(
            "confirmation_store.read must return a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipantApplication"
            "ConfirmationSet"
        )

    return (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion(
            decision_record=decision_record,
            confirmation_set=confirmation_set,
        )
    )
