from typing import Protocol, runtime_checkable

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)


@runtime_checkable
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore(
    Protocol
):
    """Append-only port for durable participant application confirmations."""

    def read(
        self,
        *,
        publication_id: str,
    ) -> ConfirmationSet:
        """Return the canonical confirmations retained for one publication."""
        ...

    def create(
        self,
        *,
        confirmation: Confirmation,
    ) -> bool:
        """Append once; return False when the participant is already retained."""
        ...
