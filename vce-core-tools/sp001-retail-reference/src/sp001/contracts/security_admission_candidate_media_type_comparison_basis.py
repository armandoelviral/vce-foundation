from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_declared_media_type import (
    SecurityAdmissionCandidateDeclaredMediaType,
)
from sp001.contracts.security_admission_candidate_detected_media_type_observation import (
    SecurityAdmissionCandidateDetectedMediaTypeObservation,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeComparisonBasis:
    """Declared and detected media-type evidence for later comparison."""

    declared_media_type: SecurityAdmissionCandidateDeclaredMediaType
    detected_media_type_observation: (
        SecurityAdmissionCandidateDetectedMediaTypeObservation
    )
    comparison_scheme_id: str
    comparison_scheme_version: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.declared_media_type,
            SecurityAdmissionCandidateDeclaredMediaType,
        ):
            raise TypeError(
                "declared_media_type must be a "
                "SecurityAdmissionCandidateDeclaredMediaType"
            )
        if not isinstance(
            self.detected_media_type_observation,
            SecurityAdmissionCandidateDetectedMediaTypeObservation,
        ):
            raise TypeError(
                "detected_media_type_observation must be a "
                "SecurityAdmissionCandidateDetectedMediaTypeObservation"
            )
        declared_candidate_identity = (
            self.declared_media_type
            .metadata_identity
            .candidate_identity
        )
        detected_candidate_identity = (
            self.detected_media_type_observation
            .candidate_identity
        )
        if declared_candidate_identity != detected_candidate_identity:
            raise ValueError(
                "declared and detected media types must reference "
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
