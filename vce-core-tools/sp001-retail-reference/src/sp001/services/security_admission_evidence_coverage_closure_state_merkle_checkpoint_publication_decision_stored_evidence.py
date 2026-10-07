from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_stored_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent,
)


StoredDecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord
)
StoredIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredEvidence:
    """Preserve a durable decision together with its exact signed intent."""

    publication_intent: StoredIntent
    decision_record: StoredDecisionRecord

    def __post_init__(self) -> None:
        if not isinstance(
            self.publication_intent,
            StoredIntent,
        ):
            raise TypeError(
                "publication_intent must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationStoredIntent"
            )

        if not isinstance(
            self.decision_record,
            StoredDecisionRecord,
        ):
            raise TypeError(
                "decision_record must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationDecisionStoredRecord"
            )

        if (
            self.publication_intent.publication_id
            != self.decision_record.publication_id
        ):
            raise ValueError(
                "publication_intent and decision_record must "
                "retain the same publication_id"
            )
