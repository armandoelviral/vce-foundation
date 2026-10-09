from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)


ApplicationCompletion = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion
)
Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)


def derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_application_completion(
    *,
    decision_record: DecisionRecord,
    confirmation_set: ConfirmationSet,
) -> ApplicationCompletion | None:
    """Derive completion only from exact durable confirmation coverage."""

    if not isinstance(
        decision_record,
        DecisionRecord,
    ):
        raise TypeError(
            "decision_record must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecord"
        )

    if not isinstance(
        confirmation_set,
        ConfirmationSet,
    ):
        raise TypeError(
            "confirmation_set must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipantApplication"
            "ConfirmationSet"
        )

    target_ids = (
        tuple(
            participant.participant_id
            for participant in (
                decision_record
                .participant_set
                .participants
            )
        )
        if decision_record.decision is Decision.COMMIT
        else tuple(
            preparation.participant_id
            for preparation in (
                decision_record
                .preparation_set
                .preparations
            )
        )
    )
    confirmed_ids = tuple(
        confirmation.participant_id
        for confirmation in confirmation_set.confirmations
    )

    target_id_set = set(target_ids)
    if any(
        participant_id not in target_id_set
        for participant_id in confirmed_ids
    ):
        raise ValueError(
            "confirmation_set contains a participant "
            "outside the application target"
        )

    if confirmed_ids != target_ids:
        return None

    return ApplicationCompletion(
        decision_record=decision_record,
        confirmation_set=confirmation_set,
    )
