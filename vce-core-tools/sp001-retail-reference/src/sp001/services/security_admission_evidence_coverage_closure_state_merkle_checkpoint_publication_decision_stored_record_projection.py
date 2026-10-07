from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_projection import (
    project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
_STORAGE_SCHEMA_VERSION = 1


def project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
    *,
    decision_record: DecisionRecord,
) -> StoredDecisionRecord:
    """Project one global publication decision into portable stored values."""

    if not isinstance(
        decision_record,
        DecisionRecord,
    ):
        raise TypeError(
            "decision_record must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecord"
        )

    participant_ids = tuple(
        participant.participant_id
        for participant in (
            decision_record
            .participant_set
            .participants
        )
    )

    preparations = tuple(
        (
            preparation.participant_id,
            project_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
                state=preparation.publication_state,
            ),
        )
        for preparation in (
            decision_record
            .preparation_set
            .preparations
        )
    )

    return StoredDecisionRecord(
        storage_schema_version=_STORAGE_SCHEMA_VERSION,
        publication_id=(
            decision_record
            .publication_intent
            .publication_id
        ),
        participant_ids=participant_ids,
        preparations=preparations,
        decision=decision_record.decision.value,
    )
