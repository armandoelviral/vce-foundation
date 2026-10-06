from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_intent import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_transition import (
    transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_verified_state_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore,
)


Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationIntent = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)
VerifiedStateStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore
)

_MAX_CAS_ATTEMPTS = 4


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
    RuntimeError
):
    """Raised when a participant cannot preserve publication state."""


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDurableParticipant:
    """Apply idempotent participant operations over authenticated durable state."""

    __slots__ = (
        "_participant_id",
        "_state_store",
    )

    def __init__(
        self,
        *,
        participant_id: str,
        state_store: VerifiedStateStore,
    ) -> None:
        if type(participant_id) is not str:
            raise TypeError(
                "participant_id must be a string"
            )
        if not participant_id.strip():
            raise ValueError(
                "participant_id must not be blank"
            )
        if not isinstance(
            state_store,
            VerifiedStateStore,
        ):
            raise TypeError(
                "state_store must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationVerifiedStateStore"
            )

        self._participant_id = participant_id
        self._state_store = state_store

    @property
    def participant_id(self) -> str:
        return self._participant_id

    def prepare(
        self,
        *,
        publication_intent: PublicationIntent,
    ) -> PublicationState:
        if not isinstance(
            publication_intent,
            PublicationIntent,
        ):
            raise TypeError(
                "publication_intent must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationIntent"
            )

        publication_id = (
            publication_intent.publication_id
        )

        for _ in range(_MAX_CAS_ATTEMPTS):
            current_state = self._read(
                publication_id=publication_id,
            )

            if current_state is None:
                initial_state = PublicationState(
                    publication_intent=publication_intent,
                    phase=Phase.INTENT_RECORDED,
                    revision=1,
                )
                created = self._state_store.create(
                    state=initial_state,
                )
                if type(created) is not bool:
                    raise TypeError(
                        "state_store.create must return a bool"
                    )
                if not created:
                    continue
                current_state = initial_state

            self._require_same_intent(
                current_state=current_state,
                publication_intent=publication_intent,
            )

            if current_state.phase in (
                Phase.PREPARED,
                Phase.COMMIT_DECIDED,
                Phase.COMMITTED,
            ):
                return current_state

            if current_state.phase in (
                Phase.ABORT_DECIDED,
                Phase.ABORTED,
            ):
                raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
                    "aborted publication cannot be prepared"
                )

            next_state = self._transition(
                current_state=current_state,
                target_phase=Phase.PREPARED,
            )
            if next_state is not None:
                return next_state

        self._raise_conflict()

    def commit(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self._validate_publication_id(
            publication_id
        )

        for _ in range(_MAX_CAS_ATTEMPTS):
            current_state = self._require_state(
                publication_id=publication_id,
            )

            if current_state.phase is Phase.COMMITTED:
                return current_state

            if current_state.phase in (
                Phase.INTENT_RECORDED,
                Phase.ABORT_DECIDED,
                Phase.ABORTED,
            ):
                raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
                    "publication cannot be committed from its current phase"
                )

            target_phase = (
                Phase.COMMITTED
                if current_state.phase
                is Phase.COMMIT_DECIDED
                else Phase.COMMIT_DECIDED
            )
            next_state = self._transition(
                current_state=current_state,
                target_phase=target_phase,
            )
            if next_state is None:
                continue
            if next_state.phase is Phase.COMMITTED:
                return next_state

        self._raise_conflict()

    def abort(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        self._validate_publication_id(
            publication_id
        )

        for _ in range(_MAX_CAS_ATTEMPTS):
            current_state = self._require_state(
                publication_id=publication_id,
            )

            if current_state.phase is Phase.ABORTED:
                return current_state

            if current_state.phase in (
                Phase.COMMIT_DECIDED,
                Phase.COMMITTED,
            ):
                raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
                    "commit-decided publication cannot be aborted"
                )

            target_phase = (
                Phase.ABORTED
                if current_state.phase
                is Phase.ABORT_DECIDED
                else Phase.ABORT_DECIDED
            )
            next_state = self._transition(
                current_state=current_state,
                target_phase=target_phase,
            )
            if next_state is None:
                continue
            if next_state.phase is Phase.ABORTED:
                return next_state

        self._raise_conflict()

    def _read(
        self,
        *,
        publication_id: str,
    ) -> PublicationState | None:
        state = self._state_store.read(
            publication_id=publication_id,
        )

        if state is None:
            return None

        if not isinstance(
            state,
            PublicationState,
        ):
            raise TypeError(
                "state_store.read must return a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState "
                "or None"
            )

        retained_publication_id = (
            state
            .publication_intent
            .publication_id
        )
        if retained_publication_id != publication_id:
            raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
                "state_store returned a different publication_id"
            )

        return state

    def _require_state(
        self,
        *,
        publication_id: str,
    ) -> PublicationState:
        state = self._read(
            publication_id=publication_id,
        )

        if state is None:
            raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
                "publication state does not exist"
            )

        return state

    def _require_same_intent(
        self,
        *,
        current_state: PublicationState,
        publication_intent: PublicationIntent,
    ) -> None:
        if (
            current_state.publication_intent
            != publication_intent
        ):
            raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
                "publication_id is already bound to a different publication intent"
            )

    def _transition(
        self,
        *,
        current_state: PublicationState,
        target_phase: Phase,
    ) -> PublicationState | None:
        next_state = (
            transition_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication(
                current_state=current_state,
                target_phase=target_phase,
            )
        )
        swapped = self._state_store.compare_and_swap(
            expected_revision=current_state.revision,
            next_state=next_state,
        )

        if type(swapped) is not bool:
            raise TypeError(
                "state_store.compare_and_swap must return a bool"
            )

        return next_state if swapped else None

    @staticmethod
    def _validate_publication_id(
        publication_id: str,
    ) -> None:
        if type(publication_id) is not str:
            raise TypeError(
                "publication_id must be a string"
            )
        if not publication_id:
            raise ValueError(
                "publication_id must not be empty"
            )

    @staticmethod
    def _raise_conflict() -> None:
        raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantStateError(
            "publication state conflict exceeded bounded CAS attempts"
        )
