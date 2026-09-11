from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_metadata_verification_procedure_identity import (
    SecurityAdmissionMetadataVerificationProcedureIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMeasuredByteLengthObservation:
    """Exact byte length measured for untrusted candidate content."""

    observation_id: str
    observation_version: int
    candidate_identity: SecurityAdmissionCandidateIdentity
    verification_procedure_identity: (
        SecurityAdmissionMetadataVerificationProcedureIdentity
    )
    measured_byte_length: int
    observed_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.observation_id, str):
            raise TypeError("observation_id must be a string")
        if not self.observation_id.strip():
            raise ValueError("observation_id must not be blank")
        if (
            isinstance(self.observation_version, bool)
            or not isinstance(self.observation_version, int)
        ):
            raise TypeError("observation_version must be an integer")
        if self.observation_version <= 0:
            raise ValueError("observation_version must be positive")
        if not isinstance(
            self.candidate_identity,
            SecurityAdmissionCandidateIdentity,
        ):
            raise TypeError(
                "candidate_identity must be a "
                "SecurityAdmissionCandidateIdentity"
            )
        if not isinstance(
            self.verification_procedure_identity,
            SecurityAdmissionMetadataVerificationProcedureIdentity,
        ):
            raise TypeError(
                "verification_procedure_identity must be a "
                "SecurityAdmissionMetadataVerificationProcedureIdentity"
            )
        if (
            isinstance(self.measured_byte_length, bool)
            or not isinstance(self.measured_byte_length, int)
        ):
            raise TypeError("measured_byte_length must be an integer")
        if self.measured_byte_length < 0:
            raise ValueError(
                "measured_byte_length must not be negative"
            )
        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        if (
            self.observed_at.tzinfo is None
            or self.observed_at.utcoffset() is None
        ):
            raise ValueError("observed_at must be timezone-aware")
