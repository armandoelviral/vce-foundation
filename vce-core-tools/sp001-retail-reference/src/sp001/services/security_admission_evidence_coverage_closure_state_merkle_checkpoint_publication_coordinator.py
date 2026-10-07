from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_recording import (
    record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision_application import (
    apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
DecisionRecordStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore
)
PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)


def coordinate_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
    *,
    publication_intent: PublicationIntent,
    participant_set: ParticipantSet,
    decision_record_store: DecisionRecordStore,
) -> DecisionRecord:
    """Record one global decision durably before applying its effects."""

    decision_record = (
        record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=publication_intent,
            participant_set=participant_set,
            decision_record_store=decision_record_store,
        )
    )

    apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision(
        decision_record_store=decision_record_store,
        publication_id=publication_intent.publication_id,
    )

    return decision_record
