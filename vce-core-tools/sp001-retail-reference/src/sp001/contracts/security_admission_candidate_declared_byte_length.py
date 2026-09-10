from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_metadata_identity import (
    SecurityAdmissionCandidateMetadataIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateDeclaredByteLength:
    """Unverified byte-length declaration from exact candidate metadata."""

    metadata_identity: SecurityAdmissionCandidateMetadataIdentity
    declared_byte_length: int

    def __post_init__(self) -> None:
        if not isinstance(
            self.metadata_identity,
            SecurityAdmissionCandidateMetadataIdentity,
        ):
            raise TypeError(
                "metadata_identity must be a "
                "SecurityAdmissionCandidateMetadataIdentity"
            )
        if (
            isinstance(self.declared_byte_length, bool)
            or not isinstance(self.declared_byte_length, int)
        ):
            raise TypeError("declared_byte_length must be an integer")
        if self.declared_byte_length < 0:
            raise ValueError(
                "declared_byte_length must not be negative"
            )
