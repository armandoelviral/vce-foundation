from typing import Protocol, runtime_checkable

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


@runtime_checkable
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant(
    Protocol
):
    """Participant boundary for durable checkpoint publication."""

    @property
    def participant_id(self) -> str:
        ...

    def prepare(
        self,
        *,
        publication_intent: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
    ) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState:
        ...

    def commit(
        self,
        *,
        publication_id: str,
    ) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState:
        ...

    def abort(
        self,
        *,
        publication_id: str,
    ) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState:
        ...
