from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant_preparation import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation,
)


ParticipantPreparation = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparationSet:
    """Preserve one canonical set of participant preparations."""

    preparations: tuple[
        ParticipantPreparation,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.preparations,
            tuple,
        ):
            raise TypeError(
                "preparations must be a tuple"
            )

        for preparation in self.preparations:
            if not isinstance(
                preparation,
                ParticipantPreparation,
            ):
                raise TypeError(
                    "preparations must contain only "
                    "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantPreparation "
                    "values"
                )

        participant_ids = tuple(
            preparation.participant_id
            for preparation in self.preparations
        )

        if len(set(participant_ids)) != len(
            participant_ids
        ):
            raise ValueError(
                "preparations must contain unique "
                "participant identifiers"
            )

        if participant_ids != tuple(
            sorted(participant_ids)
        ):
            raise ValueError(
                "preparations must use canonical "
                "participant identifier order"
            )

        if not self.preparations:
            return

        publication_intents = tuple(
            preparation
            .publication_state
            .publication_intent
            for preparation in self.preparations
        )
        retained_intent = publication_intents[0]

        if any(
            publication_intent
            != retained_intent
            for publication_intent
            in publication_intents[1:]
        ):
            raise ValueError(
                "preparations must reference the exact "
                "same publication intent"
            )
