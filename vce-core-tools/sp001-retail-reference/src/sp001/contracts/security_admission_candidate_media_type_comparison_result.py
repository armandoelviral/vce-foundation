from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.security_admission_candidate_media_type_comparison_basis import (
    SecurityAdmissionCandidateMediaTypeComparisonBasis,
)


class SecurityAdmissionMediaTypeComparisonStatus(StrEnum):
    """Conclusive outcome of one declared media comparison scheme."""

    MATCHES = "MATCHES"
    DOES_NOT_MATCH = "DOES_NOT_MATCH"


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeComparisonResult:
    """Conclusive media-type comparison for one complete basis."""

    result_id: str
    result_version: int
    comparison_basis: SecurityAdmissionCandidateMediaTypeComparisonBasis
    match_status: SecurityAdmissionMediaTypeComparisonStatus
    compared_at: datetime

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
            self.comparison_basis,
            SecurityAdmissionCandidateMediaTypeComparisonBasis,
        ):
            raise TypeError(
                "comparison_basis must be a "
                "SecurityAdmissionCandidateMediaTypeComparisonBasis"
            )
        if not isinstance(
            self.match_status,
            SecurityAdmissionMediaTypeComparisonStatus,
        ):
            raise TypeError(
                "match_status must be a "
                "SecurityAdmissionMediaTypeComparisonStatus"
            )
        if not isinstance(self.compared_at, datetime):
            raise TypeError("compared_at must be a datetime")
        if (
            self.compared_at.tzinfo is None
            or self.compared_at.utcoffset() is None
        ):
            raise ValueError("compared_at must be timezone-aware")
