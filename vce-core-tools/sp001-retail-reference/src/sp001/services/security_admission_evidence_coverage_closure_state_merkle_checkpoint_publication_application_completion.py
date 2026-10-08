from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision_record import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet,
)


Decision = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision
)
DecisionRecord = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionRecord
)
ConfirmationSet = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationApplicationCompletion:
    """Preserve exhaustive confirmation of one durable global decision."""

    decision_record: DecisionRecord
    confirmation_set: ConfirmationSet

    def __post_init__(self) -> None:
        if not isinstance(
            self.decision_record,
            DecisionRecord,
        ):
            raise TypeError(
                "decision_record must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationDecisionRecord"
            )

        if not isinstance(
            self.confirmation_set,
            ConfirmationSet,
        ):
            raise TypeError(
                "confirmation_set must be a "
                "SecurityAdmissionEvidenceCoverageClosureState"
                "MerkleCheckpointPublicationParticipant"
                "ApplicationConfirmationSet"
            )

        rederived = (
            derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision(
                publication_intent=(
                    self.decision_record.publication_intent
                ),
                participant_set=(
                    self.decision_record.participant_set
                ),
                preparation_set=(
                    self.decision_record.preparation_set
                ),
            )
        )
        if rederived != self.decision_record:
            raise ValueError(
                "decision_record must retain the exactly "
                "re-derived publication decision"
            )

        target_ids = self._target_ids()
        confirmed_ids = tuple(
            confirmation.participant_id
            for confirmation in (
                self.confirmation_set.confirmations
            )
        )
        if confirmed_ids != target_ids:
            raise ValueError(
                "confirmation_set must exhaustively match "
                "the targeted participant identifiers"
            )

        for confirmation in (
            self.confirmation_set.confirmations
        ):
            if (
                confirmation.decision
                is not self.decision_record.decision
            ):
                raise ValueError(
                    "confirmations must retain the recorded "
                    "publication decision"
                )

            if (
                confirmation
                .publication_state
                .publication_intent
                != self.decision_record.publication_intent
            ):
                raise ValueError(
                    "confirmations must retain the exact "
                    "recorded publication intent"
                )

    def _target_ids(self) -> tuple[str, ...]:
        if self.decision_record.decision is Decision.COMMIT:
            return tuple(
                participant.participant_id
                for participant in (
                    self.decision_record
                    .participant_set
                    .participants
                )
            )

        return tuple(
            preparation.participant_id
            for preparation in (
                self.decision_record
                .preparation_set
                .preparations
            )
        )
