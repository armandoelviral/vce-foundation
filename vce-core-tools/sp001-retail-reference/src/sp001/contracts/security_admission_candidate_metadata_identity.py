from dataclasses import dataclass

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMetadataIdentity:
    """Identity of canonical metadata bytes for one admission candidate."""

    candidate_identity: SecurityAdmissionCandidateIdentity
    metadata_schema_id: str
    metadata_schema_version: int
    metadata_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        if not isinstance(
            self.candidate_identity,
            SecurityAdmissionCandidateIdentity,
        ):
            raise TypeError(
                "candidate_identity must be a "
                "SecurityAdmissionCandidateIdentity"
            )
        if not isinstance(self.metadata_schema_id, str):
            raise TypeError("metadata_schema_id must be a string")
        if not self.metadata_schema_id.strip():
            raise ValueError("metadata_schema_id must not be blank")
        if (
            isinstance(self.metadata_schema_version, bool)
            or not isinstance(self.metadata_schema_version, int)
        ):
            raise TypeError(
                "metadata_schema_version must be an integer"
            )
        if self.metadata_schema_version <= 0:
            raise ValueError(
                "metadata_schema_version must be positive"
            )
        if not isinstance(
            self.metadata_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "metadata_digest must be a KnowledgeContentDigest"
            )
