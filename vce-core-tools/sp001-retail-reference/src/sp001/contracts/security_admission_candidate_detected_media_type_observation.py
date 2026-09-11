from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_metadata_verification_procedure_identity import (
    SecurityAdmissionMetadataVerificationProcedureIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateDetectedMediaTypeObservation:
    """Media type detected for exact untrusted candidate content."""

    observation_id: str
    observation_version: int
    candidate_identity: SecurityAdmissionCandidateIdentity
    verification_procedure_identity: (
        SecurityAdmissionMetadataVerificationProcedureIdentity
    )
    detected_media_type: str
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
        if not isinstance(self.detected_media_type, str):
            raise TypeError("detected_media_type must be a string")
        if not self.detected_media_type.strip():
            raise ValueError("detected_media_type must not be blank")
        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        if (
            self.observed_at.tzinfo is None
            or self.observed_at.utcoffset() is None
        ):
            raise ValueError("observed_at must be timezone-aware")
