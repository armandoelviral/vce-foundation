from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence,
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
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
StoredEvidence = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence
)
ParticipantPreparation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
_SUPPORTED_DECISION_RECORD_SCHEMA_VERSION = 1


def deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_evidence(
    *,
    stored_evidence: StoredEvidence,
    participant_set: ParticipantSet,
) -> DecisionRecord:
    """Rebuild and re-derive durable signed publication decision evidence."""

    if not isinstance(
        stored_evidence,
        StoredEvidence,
    ):
        raise TypeError(
            "stored_evidence must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionStoredEvidence"
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

    stored_record = stored_evidence.decision_record
    if (
        stored_record.storage_schema_version
        != _SUPPORTED_DECISION_RECORD_SCHEMA_VERSION
    ):
        raise ValueError(
            "stored decision record uses an unsupported "
            "storage schema version"
        )

    provisioned_participant_ids = tuple(
        participant.participant_id
        for participant in participant_set.participants
    )
    if (
        provisioned_participant_ids
        != stored_record.participant_ids
    ):
        raise ValueError(
            "stored participant identifiers do not match "
            "the provisioned participant set"
        )

    publication_intent = (
        deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent(
            stored_intent=(
                stored_evidence.publication_intent
            ),
        )
    )

    preparations = tuple(
        ParticipantPreparation(
            participant_id=participant_id,
            publication_state=(
                deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state(
                    stored_state=stored_state,
                )
            ),
        )
        for participant_id, stored_state in (
            stored_record.preparations
        )
    )

    if any(
        preparation.publication_state.publication_intent
        != publication_intent
        for preparation in preparations
    ):
        raise ValueError(
            "preparations must reference the exact "
            "stored publication intent"
        )

    preparation_set = PreparationSet(
        preparations=preparations,
    )

    decision_record = (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=publication_intent,
            participant_set=participant_set,
            preparation_set=preparation_set,
        )
    )

    if (
        decision_record.decision.value
        != stored_record.decision
    ):
        raise ValueError(
            "stored publication decision does not match "
            "the re-derived decision"
        )

    return decision_record
