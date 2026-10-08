from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_store import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_state import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
DecisionRecordStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecordStore
)
Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)
ConfirmationStore = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationStore
)
Phase = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
)
PublicationState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationState
)


class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationRecordedDecisionApplicationError(
    RuntimeError
):
    """Report participants that did not confirm the durable decision."""

    __slots__ = (
        "failed_participant_ids",
    )

    def __init__(
        self,
        *,
        failed_participant_ids: tuple[str, ...],
    ) -> None:
        self.failed_participant_ids = (
            failed_participant_ids
        )
        super().__init__(
            "recorded publication decision was not "
            "confirmed by every targeted participant"
        )


def apply_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_recorded_decision(
    *,
    decision_record_store: DecisionRecordStore,
    confirmation_store: ConfirmationStore,
    publication_id: str,
) -> tuple[PublicationState, ...]:
    """Converge one durable global decision using durable confirmations."""

    if not isinstance(
        decision_record_store,
        DecisionRecordStore,
    ):
        raise TypeError(
            "decision_record_store must implement "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecordStore"
        )

    if not isinstance(
        confirmation_store,
        ConfirmationStore,
    ):
        raise TypeError(
            "confirmation_store must implement "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipantApplication"
            "ConfirmationStore"
        )

    if type(publication_id) is not str:
        raise TypeError(
            "publication_id must be a string"
        )
    if not publication_id:
        raise ValueError(
            "publication_id must not be empty"
        )

    decision_record = decision_record_store.read(
        publication_id=publication_id,
    )
    if decision_record is None:
        raise ValueError(
            "durable publication decision does not exist"
        )
    if not isinstance(
        decision_record,
        DecisionRecord,
    ):
        raise TypeError(
            "decision_record_store.read must return a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationDecisionRecord or None"
        )

    retained_publication_id = (
        decision_record
        .publication_intent
        .publication_id
    )
    if retained_publication_id != publication_id:
        raise ValueError(
            "durable decision record has a different "
            "publication_id"
        )

    participants_by_id = {
        participant.participant_id: participant
        for participant in (
            decision_record
            .participant_set
            .participants
        )
    }
    preparation_ids = tuple(
        preparation.participant_id
        for preparation in (
            decision_record
            .preparation_set
            .preparations
        )
    )

    unknown_preparation_ids = tuple(
        participant_id
        for participant_id in preparation_ids
        if participant_id not in participants_by_id
    )
    if unknown_preparation_ids:
        raise ValueError(
            "durable decision record contains preparation "
            "evidence outside the participant set"
        )

    rederived_decision_record = (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
            publication_intent=(
                decision_record.publication_intent
            ),
            participant_set=(
                decision_record.participant_set
            ),
            preparation_set=(
                decision_record.preparation_set
            ),
        )
    )
    if rederived_decision_record != decision_record:
        raise ValueError(
            "durable publication decision does not match "
            "the retained preparation evidence"
        )

    if decision_record.decision is Decision.COMMIT:
        target_ids = tuple(
            participant.participant_id
            for participant in (
                decision_record
                .participant_set
                .participants
            )
        )
        method_name = "commit"
        expected_phase = Phase.COMMITTED
    else:
        target_ids = preparation_ids
        method_name = "abort"
        expected_phase = Phase.ABORTED

    retained_confirmations = _read_valid_confirmations(
        confirmation_store=confirmation_store,
        publication_id=publication_id,
        decision_record=decision_record,
        target_ids=target_ids,
        expected_phase=expected_phase,
    )
    confirmations_by_id = {
        confirmation.participant_id: confirmation
        for confirmation in (
            retained_confirmations.confirmations
        )
    }

    confirmed_states: list[PublicationState] = []
    failed_participant_ids: list[str] = []

    for participant_id in target_ids:
        retained_confirmation = (
            confirmations_by_id.get(participant_id)
        )
        if retained_confirmation is not None:
            confirmed_states.append(
                retained_confirmation.publication_state
            )
            continue

        participant = participants_by_id[
            participant_id
        ]
        method = getattr(
            participant,
            method_name,
        )

        try:
            state = method(
                publication_id=publication_id,
            )
        except Exception:
            failed_participant_ids.append(
                participant_id
            )
            continue

        if not isinstance(
            state,
            PublicationState,
        ):
            failed_participant_ids.append(
                participant_id
            )
            continue

        if (
            state.publication_intent
            != decision_record.publication_intent
        ):
            failed_participant_ids.append(
                participant_id
            )
            continue

        if state.phase is not expected_phase:
            failed_participant_ids.append(
                participant_id
            )
            continue

        confirmation = Confirmation(
            participant_id=participant_id,
            decision=decision_record.decision,
            publication_state=state,
        )

        try:
            created = confirmation_store.create(
                confirmation=confirmation,
            )
        except Exception:
            failed_participant_ids.append(
                participant_id
            )
            continue

        if type(created) is not bool:
            failed_participant_ids.append(
                participant_id
            )
            continue

        if not created:
            concurrent_confirmations = (
                _read_valid_confirmations(
                    confirmation_store=confirmation_store,
                    publication_id=publication_id,
                    decision_record=decision_record,
                    target_ids=target_ids,
                    expected_phase=expected_phase,
                )
            )
            concurrent_by_id = {
                retained.participant_id: retained
                for retained in (
                    concurrent_confirmations
                    .confirmations
                )
            }
            if (
                concurrent_by_id.get(participant_id)
                != confirmation
            ):
                failed_participant_ids.append(
                    participant_id
                )
                continue

        confirmed_states.append(state)

    if failed_participant_ids:
        raise SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationRecordedDecisionApplicationError(
            failed_participant_ids=tuple(
                failed_participant_ids
            ),
        )

    return tuple(confirmed_states)


def _read_valid_confirmations(
    *,
    confirmation_store: ConfirmationStore,
    publication_id: str,
    decision_record: DecisionRecord,
    target_ids: tuple[str, ...],
    expected_phase: Phase,
) -> ConfirmationSet:
    retained = confirmation_store.read(
        publication_id=publication_id,
    )

    if not isinstance(
        retained,
        ConfirmationSet,
    ):
        raise TypeError(
            "confirmation_store.read must return a "
            "SecurityAdmissionEvidenceCoverageClosureState"
            "MerkleCheckpointPublicationParticipantApplication"
            "ConfirmationSet"
        )

    target_id_set = set(target_ids)

    for confirmation in retained.confirmations:
        if confirmation.participant_id not in target_id_set:
            raise ValueError(
                "durable application confirmation is outside "
                "the targeted participant set"
            )

        if confirmation.decision is not decision_record.decision:
            raise ValueError(
                "durable application confirmation has a "
                "different publication decision"
            )

        if (
            confirmation
            .publication_state
            .publication_intent
            != decision_record.publication_intent
        ):
            raise ValueError(
                "durable application confirmation has a "
                "different publication intent"
            )

        if (
            confirmation.publication_state.phase
            is not expected_phase
        ):
            raise ValueError(
                "durable application confirmation has a "
                "different terminal phase"
            )

    return retained
