from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_application_confirmation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation,
)


Confirmation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmation
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantApplicationConfirmationSet:
    """Preserve one canonical set of participant application confirmations."""

    confirmations: tuple[
        Confirmation,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.confirmations,
            tuple,
        ):
            raise TypeError(
                "confirmations must be a tuple"
            )

        for confirmation in self.confirmations:
            if not isinstance(
                confirmation,
                Confirmation,
            ):
                raise TypeError(
                    "confirmations must contain only "
                    "SecurityAdmissionEvidenceCoverageClosureState"
                    "MerkleCheckpointPublicationParticipant"
                    "ApplicationConfirmation values"
                )

        participant_ids = tuple(
            confirmation.participant_id
            for confirmation in self.confirmations
        )

        if len(set(participant_ids)) != len(
            participant_ids
        ):
            raise ValueError(
                "confirmations must contain unique "
                "participant identifiers"
            )

        if participant_ids != tuple(
            sorted(participant_ids)
        ):
            raise ValueError(
                "confirmations must use canonical "
                "participant identifier order"
            )

        if not self.confirmations:
            return

        retained_decision = (
            self.confirmations[0].decision
        )
        if any(
            confirmation.decision is not retained_decision
            for confirmation in self.confirmations[1:]
        ):
            raise ValueError(
                "confirmations must retain the same "
                "publication decision"
            )

        retained_intent = (
            self.confirmations[0]
            .publication_state
            .publication_intent
        )
        if any(
            (
                confirmation
                .publication_state
                .publication_intent
            )
            != retained_intent
            for confirmation in self.confirmations[1:]
        ):
            raise ValueError(
                "confirmations must reference the exact "
                "same publication intent"
            )
