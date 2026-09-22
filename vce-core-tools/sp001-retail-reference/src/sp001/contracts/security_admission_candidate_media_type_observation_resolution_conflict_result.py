from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.security_admission_candidate_detected_media_type_observation import (
    SecurityAdmissionCandidateDetectedMediaTypeObservation,
)
from sp001.contracts.security_admission_candidate_media_type_observation_resolution_basis import (
    SecurityAdmissionCandidateMediaTypeObservationResolutionBasis,
)


class SecurityAdmissionMediaTypeObservationResolutionConflictReason(
    StrEnum
):
    """Closed reasons why a media-type observation cannot be selected."""

    CONFLICTING_NORMATIVE_PROCEDURE_IDENTITIES = (
        "CONFLICTING_NORMATIVE_PROCEDURE_IDENTITIES"
    )
    UNRANKED_VERIFICATION_PROCEDURE = (
        "UNRANKED_VERIFICATION_PROCEDURE"
    )
    LATEST_TIMESTAMP_TIE = "LATEST_TIMESTAMP_TIE"


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeObservationResolutionConflictResult:
    """Typed logical conflict preventing media-type coverage closure."""

    result_id: str
    result_version: int
    resolution_basis: (
        SecurityAdmissionCandidateMediaTypeObservationResolutionBasis
    )
    reason: (
        SecurityAdmissionMediaTypeObservationResolutionConflictReason
    )
    conflicting_observations: tuple[
        SecurityAdmissionCandidateDetectedMediaTypeObservation, ...
    ]
    determined_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.result_id, str):
            raise TypeError("result_id must be a string")
        if not self.result_id.strip():
            raise ValueError("result_id must not be blank")
        if (
            isinstance(self.result_version, bool)
            or not isinstance(self.result_version, int)
        ):
            raise TypeError("result_version must be an integer")
        if self.result_version <= 0:
            raise ValueError("result_version must be positive")
        if not isinstance(
            self.resolution_basis,
            SecurityAdmissionCandidateMediaTypeObservationResolutionBasis,
        ):
            raise TypeError(
                "resolution_basis must be a "
                "SecurityAdmissionCandidateMediaTypeObservationResolutionBasis"
            )
        if not isinstance(
            self.reason,
            SecurityAdmissionMediaTypeObservationResolutionConflictReason,
        ):
            raise TypeError(
                "reason must be a "
                "SecurityAdmissionMediaTypeObservationResolutionConflictReason"
            )
        if not isinstance(self.conflicting_observations, tuple):
            raise TypeError(
                "conflicting_observations must be an immutable tuple"
            )
        if not self.conflicting_observations:
            raise ValueError(
                "conflicting_observations must not be empty"
            )
        for observation in self.conflicting_observations:
            if not isinstance(
                observation,
                SecurityAdmissionCandidateDetectedMediaTypeObservation,
            ):
                raise TypeError(
                    "conflicting_observations must contain "
                    "SecurityAdmissionCandidateDetectedMediaTypeObservation "
                    "values"
                )
        if not isinstance(self.determined_at, datetime):
            raise TypeError("determined_at must be a datetime")
        if (
            self.determined_at.tzinfo is None
            or self.determined_at.utcoffset() is None
        ):
            raise ValueError("determined_at must be timezone-aware")

        observations = self.resolution_basis.observation_set.observations
        authority_identities = (
            self.resolution_basis
            .authority_order
            .verification_procedure_identities
        )

        identities_by_procedure_id: dict[str, set[object]] = {}
        for observation in observations:
            identity = observation.verification_procedure_identity
            identities_by_procedure_id.setdefault(
                identity.verification_procedure_id,
                set(),
            ).add(identity)

        conflicting_procedure_ids = {
            procedure_id
            for procedure_id, identities
            in identities_by_procedure_id.items()
            if len(identities) > 1
        }
        normative_conflicts = tuple(
            observation
            for observation in observations
            if (
                observation
                .verification_procedure_identity
                .verification_procedure_id
                in conflicting_procedure_ids
            )
        )

        authority_positions = {
            identity: position
            for position, identity in enumerate(authority_identities)
        }
        unranked_observations = tuple(
            observation
            for observation in observations
            if observation.verification_procedure_identity
            not in authority_positions
        )

        latest_ties: tuple[
            SecurityAdmissionCandidateDetectedMediaTypeObservation, ...
        ] = ()
        if not normative_conflicts and not unranked_observations:
            highest_position = min(
                authority_positions[
                    observation.verification_procedure_identity
                ]
                for observation in observations
            )
            highest_authority_observations = tuple(
                observation
                for observation in observations
                if authority_positions[
                    observation.verification_procedure_identity
                ]
                == highest_position
            )
            latest_observed_at = max(
                observation.observed_at
                for observation in highest_authority_observations
            )
            latest = tuple(
                observation
                for observation in highest_authority_observations
                if observation.observed_at == latest_observed_at
            )
            if len(latest) > 1:
                latest_ties = latest

        if normative_conflicts:
            expected_reason = (
                SecurityAdmissionMediaTypeObservationResolutionConflictReason
                .CONFLICTING_NORMATIVE_PROCEDURE_IDENTITIES
            )
            expected_observations = normative_conflicts
        elif unranked_observations:
            expected_reason = (
                SecurityAdmissionMediaTypeObservationResolutionConflictReason
                .UNRANKED_VERIFICATION_PROCEDURE
            )
            expected_observations = unranked_observations
        elif latest_ties:
            expected_reason = (
                SecurityAdmissionMediaTypeObservationResolutionConflictReason
                .LATEST_TIMESTAMP_TIE
            )
            expected_observations = latest_ties
        else:
            raise ValueError(
                "resolution basis contains no logical selection conflict"
            )

        if self.reason is not expected_reason:
            raise ValueError(
                "reason must identify the first applicable logical conflict"
            )
        if self.conflicting_observations != expected_observations:
            raise ValueError(
                "conflicting_observations must exactly identify "
                "the first applicable logical conflict"
            )
        if self.determined_at < max(
            observation.observed_at
            for observation in observations
        ):
            raise ValueError(
                "determined_at must not precede resolution evidence"
            )
