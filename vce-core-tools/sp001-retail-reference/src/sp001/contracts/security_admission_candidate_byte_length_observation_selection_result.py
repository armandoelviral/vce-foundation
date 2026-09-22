from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_basis import (
    SecurityAdmissionCandidateByteLengthObservationResolutionBasis,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthObservationSelectionResult:
    """Unique policy-governed byte-length observation selected for comparison."""

    result_id: str
    result_version: int
    resolution_basis: (
        SecurityAdmissionCandidateByteLengthObservationResolutionBasis
    )
    selected_observation: (
        SecurityAdmissionCandidateMeasuredByteLengthObservation
    )
    resolved_at: datetime

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
            SecurityAdmissionCandidateByteLengthObservationResolutionBasis,
        ):
            raise TypeError(
                "resolution_basis must be a "
                "SecurityAdmissionCandidateByteLengthObservationResolutionBasis"
            )
        if not isinstance(
            self.selected_observation,
            SecurityAdmissionCandidateMeasuredByteLengthObservation,
        ):
            raise TypeError(
                "selected_observation must be a "
                "SecurityAdmissionCandidateMeasuredByteLengthObservation"
            )
        if not isinstance(self.resolved_at, datetime):
            raise TypeError("resolved_at must be a datetime")
        if (
            self.resolved_at.tzinfo is None
            or self.resolved_at.utcoffset() is None
        ):
            raise ValueError("resolved_at must be timezone-aware")

        observations = self.resolution_basis.observation_set.observations
        authority_identities = (
            self.resolution_basis
            .authority_order
            .verification_procedure_identities
        )

        if self.selected_observation not in observations:
            raise ValueError(
                "selected_observation must belong to the resolution basis"
            )

        identities_by_procedure_id: dict[str, set[object]] = {}
        for observation in observations:
            identity = observation.verification_procedure_identity
            identities_by_procedure_id.setdefault(
                identity.verification_procedure_id,
                set(),
            ).add(identity)

        if any(
            len(identities) > 1
            for identities in identities_by_procedure_id.values()
        ):
            raise ValueError(
                "resolution basis contains conflicting normative "
                "procedure identities"
            )

        authority_positions = {
            identity: position
            for position, identity in enumerate(authority_identities)
        }
        if any(
            observation.verification_procedure_identity
            not in authority_positions
            for observation in observations
        ):
            raise ValueError(
                "resolution basis contains an unranked "
                "verification procedure"
            )

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
        latest_observations = tuple(
            observation
            for observation in highest_authority_observations
            if observation.observed_at == latest_observed_at
        )

        if len(latest_observations) != 1:
            raise ValueError(
                "highest-authority latest observation must be unique"
            )
        if self.selected_observation != latest_observations[0]:
            raise ValueError(
                "selected_observation must be the highest-authority "
                "latest observation"
            )
        if self.resolved_at < self.selected_observation.observed_at:
            raise ValueError(
                "resolved_at must not precede selected observation"
            )
