from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_declared_byte_length import (
    SecurityAdmissionCandidateDeclaredByteLength,
)
from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthComparisonBasis:
    """Declared and measured byte-length evidence for later comparison."""

    declared_byte_length: SecurityAdmissionCandidateDeclaredByteLength
    measured_byte_length_observation: (
        SecurityAdmissionCandidateMeasuredByteLengthObservation
    )
    comparison_scheme_id: str
    comparison_scheme_version: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.declared_byte_length,
            SecurityAdmissionCandidateDeclaredByteLength,
        ):
            raise TypeError(
                "declared_byte_length must be a "
                "SecurityAdmissionCandidateDeclaredByteLength"
            )
        if not isinstance(
            self.measured_byte_length_observation,
            SecurityAdmissionCandidateMeasuredByteLengthObservation,
        ):
            raise TypeError(
                "measured_byte_length_observation must be a "
                "SecurityAdmissionCandidateMeasuredByteLengthObservation"
            )
        declared_candidate_identity = (
            self.declared_byte_length
            .metadata_identity
            .candidate_identity
        )
        measured_candidate_identity = (
            self.measured_byte_length_observation
            .candidate_identity
        )
        if declared_candidate_identity != measured_candidate_identity:
            raise ValueError(
                "declared and measured byte lengths must reference "
                "the same candidate_identity"
            )
        if not isinstance(self.comparison_scheme_id, str):
            raise TypeError("comparison_scheme_id must be a string")
        if not self.comparison_scheme_id.strip():
            raise ValueError(
                "comparison_scheme_id must not be blank"
            )
        if (
            isinstance(self.comparison_scheme_version, bool)
            or not isinstance(self.comparison_scheme_version, int)
        ):
            raise TypeError(
                "comparison_scheme_version must be an integer"
            )
        if self.comparison_scheme_version <= 0:
            raise ValueError(
                "comparison_scheme_version must be positive"
            )
