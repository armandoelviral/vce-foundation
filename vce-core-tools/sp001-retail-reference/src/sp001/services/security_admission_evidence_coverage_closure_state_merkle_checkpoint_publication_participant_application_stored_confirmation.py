from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_stored_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)
_SUPPORTED_STORAGE_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationStoredConfirmation:
    """Preserve one portable participant application confirmation."""

    storage_schema_version: int
    participant_id: str
    decision: str
    publication_state: StoredState

    def __post_init__(self) -> None:
        validate_security_admission_positive_uint64(
            value=self.storage_schema_version,
            field="storage_schema_version",
        )
        if (
            self.storage_schema_version
            != _SUPPORTED_STORAGE_SCHEMA_VERSION
        ):
            raise ValueError(
                "stored confirmation uses an unsupported "
                "storage schema version"
            )

        if type(self.participant_id) is not str:
            raise TypeError(
                "participant_id must be a string"
            )
        if not self.participant_id:
            raise ValueError(
                "participant_id must not be empty"
            )

        if type(self.decision) is not str:
            raise TypeError(
                "decision must be a string"
            )
        try:
            decision = Decision(
                self.decision
            )
        except ValueError as error:
            raise ValueError(
                "decision must identify a supported "
                "publication decision"
            ) from error

        if not isinstance(
            self.publication_state,
            StoredState,
        ):
            raise TypeError(
                "publication_state must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationStoredState"
            )

        expected_phase = (
            Phase.COMMITTED.value
            if decision is Decision.COMMIT
            else Phase.ABORTED.value
        )
        if self.publication_state.phase != expected_phase:
            raise ValueError(
                "publication_state phase must confirm "
                "the stored publication decision"
            )
