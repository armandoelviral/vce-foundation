from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)


def project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
    *,
    decision_record: DecisionRecord,
) -> StoredEvidence:
    """Project one decision and its exact signed intent into portable evidence."""

    if not isinstance(
        decision_record,
        DecisionRecord,
    ):
        raise TypeError(
            "decision_record must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecord"
        )

    publication_intent = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            publication_intent=(
                decision_record.publication_intent
            ),
        )
    )
    stored_decision_record = (
        project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
            decision_record=decision_record,
        )
    )

    return StoredEvidence(
        publication_intent=publication_intent,
        decision_record=stored_decision_record,
    )
