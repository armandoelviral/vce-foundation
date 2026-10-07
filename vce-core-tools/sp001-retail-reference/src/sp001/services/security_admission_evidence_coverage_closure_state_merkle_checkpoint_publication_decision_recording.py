from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation_collection import (
    collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet,
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


def record_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
    *,
    publication_intent: PublicationIntent,
    participant_set: ParticipantSet,
    decision_record_store: DecisionRecordStore,
) -> DecisionRecord:
    """Derive and durably record one append-only global decision."""

    if not isinstance(
        publication_intent,
        PublicationIntent,
    ):
        raise TypeError(
            "publication_intent must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationIntent"
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

    if not isinstance(
        decision_record_store,
        DecisionRecordStore,
    ):
        raise TypeError(
            "decision_record_store must implement "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecordStore"
        )

    publication_id = publication_intent.publication_id
    existing = decision_record_store.read(
        publication_id=publication_id,
    )

    if existing is not None:
        return _require_matching_decision_record(
            decision_record=existing,
            publication_intent=publication_intent,
            participant_set=participant_set,
            source="decision_record_store.read",
        )

    preparation_set = (
        collect_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparations(
            publication_intent=publication_intent,
            participant_set=participant_set,
        )
    )
    decision_record = (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=publication_intent,
            participant_set=participant_set,
            preparation_set=preparation_set,
        )
    )

    created = decision_record_store.create(
        decision_record=decision_record,
    )
    if type(created) is not bool:
        raise TypeError(
            "decision_record_store.create must return a bool"
        )

    if created:
        return decision_record

    retained = decision_record_store.read(
        publication_id=publication_id,
    )
    if retained is None:
        raise RuntimeError(
            "decision record create conflict did not retain "
            "a durable decision"
        )

    return _require_matching_decision_record(
        decision_record=retained,
        publication_intent=publication_intent,
        participant_set=participant_set,
        source="decision_record_store.read after create conflict",
    )


def _require_matching_decision_record(
    *,
    decision_record: object,
    publication_intent: PublicationIntent,
    participant_set: ParticipantSet,
    source: str,
) -> DecisionRecord:
    if not isinstance(
        decision_record,
        DecisionRecord,
    ):
        raise TypeError(
            f"{source} must return a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecord or None"
        )

    if (
        decision_record.publication_intent
        != publication_intent
    ):
        raise ValueError(
            "durable decision record retains a different "
            "publication intent"
        )

    if (
        decision_record.participant_set
        != participant_set
    ):
        raise ValueError(
            "durable decision record retains a different "
            "participant set"
        )

    return decision_record
