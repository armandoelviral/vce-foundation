from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_binding_set_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
)


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError(
    RuntimeError
):
    """Raised when durable publication state cannot be authenticated."""


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore:
    """Authenticates publication state at every persistence boundary."""

    __slots__ = (
        "_state_store",
        "_binding_set",
    )

    def __init__(
        self,
        *,
        state_store: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
        binding_set: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
    ) -> None:
        if not isinstance(
            state_store,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore,
        ):
            raise TypeError(
                "state_store must implement "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateStore"
            )

        if not isinstance(
            binding_set,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
        ):
            raise TypeError(
                "binding_set must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet"
            )

        self._state_store = state_store
        self._binding_set = binding_set

    def read(
        self,
        *,
        publication_id: str,
    ) -> (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
        | None
    ):
        state = self._state_store.read(
            publication_id=publication_id,
        )

        if state is None:
            return None

        self._verify_state(state)

        return state

    def create(
        self,
        *,
        state: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
    ) -> bool:
        self._verify_state(state)

        return self._state_store.create(
            state=state,
        )

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
    ) -> bool:
        self._verify_state(next_state)

        return self._state_store.compare_and_swap(
            expected_revision=expected_revision,
            next_state=next_state,
        )

    def _verify_state(
        self,
        state: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
    ) -> None:
        if not isinstance(
            state,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
        ):
            raise TypeError(
                "state must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState"
            )

        verified = (
            verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
                checkpoint_signature=(
                    state
                    .publication_intent
                    .checkpoint_signature
                ),
                binding_set=self._binding_set,
            )
        )

        if not verified:
            raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStateVerificationError(
                "publication state checkpoint signature verification failed"
            )
