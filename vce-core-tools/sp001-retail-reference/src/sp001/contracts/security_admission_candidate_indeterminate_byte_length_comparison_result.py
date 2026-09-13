from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from sp001.contracts.security_admission_candidate_byte_length_comparison_basis import (
    SecurityAdmissionCandidateByteLengthComparisonBasis,
)


class SecurityAdmissionByteLengthComparisonIndeterminacyReason(StrEnum):
    """Closed reasons why one complete basis produced no comparison."""

    UNSUPPORTED_COMPARISON_SCHEME = "UNSUPPORTED_COMPARISON_SCHEME"


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult:
    """Typed absence of a conclusive result for one complete basis."""

    result_id: str
    result_version: int
    comparison_basis: SecurityAdmissionCandidateByteLengthComparisonBasis
    reason: SecurityAdmissionByteLengthComparisonIndeterminacyReason
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
            self.comparison_basis,
            SecurityAdmissionCandidateByteLengthComparisonBasis,
        ):
            raise TypeError(
                "comparison_basis must be a "
                "SecurityAdmissionCandidateByteLengthComparisonBasis"
            )
        if not isinstance(
            self.reason,
            SecurityAdmissionByteLengthComparisonIndeterminacyReason,
        ):
            raise TypeError(
                "reason must be a "
                "SecurityAdmissionByteLengthComparisonIndeterminacyReason"
            )
        if not isinstance(self.determined_at, datetime):
            raise TypeError("determined_at must be a datetime")
        if (
            self.determined_at.tzinfo is None
            or self.determined_at.utcoffset() is None
        ):
            raise ValueError("determined_at must be timezone-aware")
