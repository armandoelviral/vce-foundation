from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_decision import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecision,
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
StoredState = (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState
)
StoredPreparation = tuple[str, StoredState]


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationDecisionStoredRecord:
    """Preserve one portable append-only global publication decision."""

    storage_schema_version: int
    publication_id: str
    participant_ids: tuple[str, ...]
    preparations: tuple[StoredPreparation, ...]
    decision: str

    def __post_init__(self) -> None:
        validate_security_admission_positive_uint64(
            value=self.storage_schema_version,
            field="storage_schema_version",
        )

        if type(self.publication_id) is not str:
            raise TypeError(
                "publication_id must be a string"
            )
        if not self.publication_id:
            raise ValueError(
                "publication_id must not be empty"
            )

        self._validate_participant_ids()
        self._validate_preparations()

        if type(self.decision) is not str:
            raise TypeError(
                "decision must be a string"
            )
        try:
            Decision(self.decision)
        except ValueError as error:
            raise ValueError(
                "decision must identify a supported "
                "publication decision"
            ) from error

    def _validate_participant_ids(self) -> None:
        if not isinstance(
            self.participant_ids,
            tuple,
        ):
            raise TypeError(
                "participant_ids must be a tuple"
            )
        if not self.participant_ids:
            raise ValueError(
                "participant_ids must not be empty"
            )

        for participant_id in self.participant_ids:
            if type(participant_id) is not str:
                raise TypeError(
                    "participant_ids must contain "
                    "only strings"
                )
            if not participant_id:
                raise ValueError(
                    "participant_ids must not contain "
                    "empty values"
                )

        if len(set(self.participant_ids)) != len(
            self.participant_ids
        ):
            raise ValueError(
                "participant_ids must contain unique values"
            )
        if self.participant_ids != tuple(
            sorted(self.participant_ids)
        ):
            raise ValueError(
                "participant_ids must use canonical order"
            )

    def _validate_preparations(self) -> None:
        if not isinstance(
            self.preparations,
            tuple,
        ):
            raise TypeError(
                "preparations must be a tuple"
            )
        if not self.preparations:
            raise ValueError(
                "preparations must not be empty"
            )

        preparation_ids: list[str] = []

        for preparation in self.preparations:
            if (
                not isinstance(preparation, tuple)
                or len(preparation) != 2
            ):
                raise TypeError(
                    "preparations must contain "
                    "(participant_id, stored_state) tuples"
                )

            participant_id, stored_state = preparation

            if type(participant_id) is not str:
                raise TypeError(
                    "preparation participant_id must be "
                    "a string"
                )
            if not participant_id:
                raise ValueError(
                    "preparation participant_id must not "
                    "be empty"
                )
            if not isinstance(
                stored_state,
                StoredState,
            ):
                raise TypeError(
                    "preparation stored_state must be a "
                    "SecurityAdmissionEvidenceCoverageClosureState"
                    "MerkleCheckpointPublicationStoredState"
                )
            if (
                stored_state.publication_id
                != self.publication_id
            ):
                raise ValueError(
                    "preparation stored_state must retain "
                    "the recorded publication_id"
                )

            preparation_ids.append(participant_id)

        preparation_id_tuple = tuple(preparation_ids)

        if len(set(preparation_id_tuple)) != len(
            preparation_id_tuple
        ):
            raise ValueError(
                "preparations must contain unique "
                "participant identifiers"
            )
        if preparation_id_tuple != tuple(
            sorted(preparation_id_tuple)
        ):
            raise ValueError(
                "preparations must use canonical "
                "participant order"
            )
