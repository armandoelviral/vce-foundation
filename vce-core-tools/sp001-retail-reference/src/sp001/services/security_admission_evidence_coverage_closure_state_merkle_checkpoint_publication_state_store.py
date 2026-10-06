from typing import Protocol, runtime_checkable

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


@runtime_checkable
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore(
    Protocol
):
    """Durable optimistic-concurrency port for checkpoint publication state."""

    def read(
        self,
        *,
        publication_id: str,
    ) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState | None:
        """Return the durable state, or None when it does not exist."""
        ...

    def create(
        self,
        *,
        state: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
    ) -> bool:
        """Create once; return False when publication_id already exists."""
        ...

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
    ) -> bool:
        """Replace only the matching revision; return False on conflict."""
        ...
