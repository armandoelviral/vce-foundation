from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthObservationSet:
    """Preserve granular media-type observations for one candidate."""

    observation_set_id: str
    observation_set_version: int
    candidate_identity: SecurityAdmissionCandidateIdentity
    observations: tuple[
        SecurityAdmissionCandidateMeasuredByteLengthObservation, ...
    ]

    def __post_init__(self) -> None:
        if not isinstance(self.observation_set_id, str):
            raise TypeError("observation_set_id must be a string")
        if not self.observation_set_id.strip():
            raise ValueError("observation_set_id must not be blank")
        if (
            isinstance(self.observation_set_version, bool)
            or not isinstance(self.observation_set_version, int)
        ):
            raise TypeError("observation_set_version must be an integer")
        if self.observation_set_version <= 0:
            raise ValueError("observation_set_version must be positive")
        if not isinstance(self.candidate_identity, SecurityAdmissionCandidateIdentity):
            raise TypeError(
                "candidate_identity must be a SecurityAdmissionCandidateIdentity"
            )
        if not isinstance(self.observations, tuple):
            raise TypeError("observations must be an immutable tuple")
        if not self.observations:
            raise ValueError("observations must not be empty")

        identities: list[tuple[str, int]] = []
        for observation in self.observations:
            if not isinstance(
                observation,
                SecurityAdmissionCandidateMeasuredByteLengthObservation,
            ):
                raise TypeError(
                    "observations must contain "
                    "SecurityAdmissionCandidateMeasuredByteLengthObservation values"
                )
            if observation.candidate_identity != self.candidate_identity:
                raise ValueError(
                    "observations must reference the set candidate_identity"
                )
            identities.append(
                (observation.observation_id, observation.observation_version)
            )

        if len(identities) != len(set(identities)):
            raise ValueError("duplicate observation identity")
        if identities != sorted(identities):
            raise ValueError("observations must use canonical identity order")
