from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_participant import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipantSet:
    """Preserve one canonical set of publication participants."""

    participants: tuple[
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.participants,
            tuple,
        ):
            raise TypeError(
                "participants must be a tuple"
            )

        if not self.participants:
            raise ValueError(
                "participants must not be empty"
            )

        for participant in self.participants:
            if not isinstance(
                participant,
                SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant,
            ):
                raise TypeError(
                    "participants must contain only "
                    "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationParticipant "
                    "values"
                )

            if type(participant.participant_id) is not str:
                raise TypeError(
                    "participant_id must be a string"
                )

            if not participant.participant_id.strip():
                raise ValueError(
                    "participant_id must not be blank"
                )

        participant_ids = tuple(
            participant.participant_id
            for participant in self.participants
        )

        if len(set(participant_ids)) != len(
            participant_ids
        ):
            raise ValueError(
                "participants must contain unique "
                "participant identifiers"
            )

        if participant_ids != tuple(
            sorted(participant_ids)
        ):
            raise ValueError(
                "participants must use canonical "
                "participant identifier order"
            )
