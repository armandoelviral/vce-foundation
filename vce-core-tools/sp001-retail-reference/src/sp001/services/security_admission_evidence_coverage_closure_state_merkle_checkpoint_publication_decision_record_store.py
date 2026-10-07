from typing import Protocol, runtime_checkable

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)


DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)


@runtime_checkable
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore(
    Protocol
):
    """Durable append-only port for global checkpoint-publication decisions."""

    def read(
        self,
        *,
        publication_id: str,
    ) -> DecisionRecord | None:
        """Return the durable decision, or None when it does not exist."""
        ...

    def create(
        self,
        *,
        decision_record: DecisionRecord,
    ) -> bool:
        """Create once; return False when publication_id already exists."""
        ...
