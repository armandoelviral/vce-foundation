from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
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
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state_deserialization import (
    deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
Participant = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)
PreparationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet
)
ParticipantSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet
)
_SUPPORTED_STORAGE_SCHEMA_VERSION = 1


def deserialize_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record(
    *,
    stored_record: StoredDecisionRecord,
    participant_set: ParticipantSet,
) -> DecisionRecord:
    """Rebuild and re-derive one durable global publication decision."""

    if not isinstance(
        stored_record,
        StoredDecisionRecord,
    ):
        raise TypeError(
            "stored_record must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionStoredRecord"
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

    if (
        stored_record.storage_schema_version
        != _SUPPORTED_STORAGE_SCHEMA_VERSION
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

    preparations = tuple(
        Participant(
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
    preparation_set = PreparationSet(
        preparations=preparations,
    )

    publication_intent = (
        preparations[0]
        .publication_state
        .publication_intent
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
