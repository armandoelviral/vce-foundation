from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)

_UINT64_MAX = (1 << 64) - 1

_ALLOWED_PHASE_TRANSITIONS = frozenset(
    {
        (
            Phase.INTENT_RECORDED,
            Phase.PREPARED,
        ),
        (
            Phase.INTENT_RECORDED,
            Phase.ABORT_DECIDED,
        ),
        (
            Phase.PREPARED,
            Phase.COMMIT_DECIDED,
        ),
        (
            Phase.PREPARED,
            Phase.ABORT_DECIDED,
        ),
        (
            Phase.COMMIT_DECIDED,
            Phase.COMMITTED,
        ),
        (
            Phase.ABORT_DECIDED,
            Phase.ABORTED,
        ),
    }
)


def transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
    *,
    current_state: PublicationState,
    target_phase: Phase,
) -> PublicationState:
    """Return the next legal immutable publication state."""

    if not isinstance(current_state, PublicationState):
        raise TypeError(
            "current_state must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationState"
        )

    if not isinstance(target_phase, Phase):
        raise TypeError(
            "target_phase must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationPhase"
        )

    transition = (
        current_state.phase,
        target_phase,
    )
    if transition not in _ALLOWED_PHASE_TRANSITIONS:
        raise ValueError(
            "publication phase transition is not allowed"
        )

    if current_state.revision == _UINT64_MAX:
        raise ValueError(
            "publication revision cannot exceed uint64"
        )

    return PublicationState(
        publication_intent=current_state.publication_intent,
        phase=target_phase,
        revision=current_state.revision + 1,
    )
