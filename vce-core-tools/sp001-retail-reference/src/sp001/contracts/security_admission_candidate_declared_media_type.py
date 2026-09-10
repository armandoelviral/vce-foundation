from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_metadata_identity import (
    SecurityAdmissionCandidateMetadataIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateDeclaredMediaType:
    """Unverified media-type declaration from exact candidate metadata."""

    metadata_identity: SecurityAdmissionCandidateMetadataIdentity
    declared_media_type: str

    def __post_init__(self) -> None:
        if not isinstance(
            self.metadata_identity,
            SecurityAdmissionCandidateMetadataIdentity,
        ):
            raise TypeError(
                "metadata_identity must be a "
                "SecurityAdmissionCandidateMetadataIdentity"
            )
        if not isinstance(self.declared_media_type, str):
            raise TypeError("declared_media_type must be a string")
        if not self.declared_media_type.strip():
            raise ValueError("declared_media_type must not be blank")
