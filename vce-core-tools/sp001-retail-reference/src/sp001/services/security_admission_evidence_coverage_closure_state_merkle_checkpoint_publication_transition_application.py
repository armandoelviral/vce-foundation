from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition import (
    transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)
StateStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore
)


def apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition(
    *,
    state_store: StateStore,
    publication_id: str,
    expected_revision: int,
    target_phase: Phase,
) -> PublicationState:
    """Apply one legal publication transition with optimistic concurrency."""

    if not isinstance(state_store, StateStore):
        raise TypeError(
            "state_store must implement "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationStateStore"
        )

    if type(publication_id) is not str:
        raise TypeError("publication_id must be a string")
    if not publication_id:
        raise ValueError("publication_id must not be empty")

    validate_security_admission_positive_uint64(
        value=expected_revision,
        field="expected_revision",
    )

    if not isinstance(target_phase, Phase):
        raise TypeError(
            "target_phase must be a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationPhase"
        )

    current_state = state_store.read(
        publication_id=publication_id,
    )
    if current_state is None:
        raise ValueError(
            "publication state does not exist"
        )
    if not isinstance(current_state, PublicationState):
        raise TypeError(
            "state_store.read must return a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationState or None"
        )

    retained_publication_id = (
        current_state
        .publication_intent
        .publication_id
    )
    if retained_publication_id != publication_id:
        raise ValueError(
            "state_store returned a different publication_id"
        )

    if current_state.revision != expected_revision:
        raise ValueError(
            "publication revision conflict before "
            "compare-and-swap"
        )

    next_state = (
        transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
            current_state=current_state,
            target_phase=target_phase,
        )
    )

    swapped = state_store.compare_and_swap(
        expected_revision=expected_revision,
        next_state=next_state,
    )
    if type(swapped) is not bool:
        raise TypeError(
            "state_store.compare_and_swap must return a bool"
        )
    if not swapped:
        raise ValueError(
            "publication revision conflict during "
            "compare-and-swap"
        )

    return next_state
