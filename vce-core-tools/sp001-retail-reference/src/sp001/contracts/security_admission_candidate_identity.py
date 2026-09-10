from dataclasses import dataclass

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateIdentity:
    """Versioned identity of exact untrusted candidate content bytes."""

    candidate_id: str
    candidate_version: int
    customer_id: str
    content_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        text_fields = {
            "candidate_id": self.candidate_id,
            "customer_id": self.customer_id,
        }
        for field, value in text_fields.items():
            if not isinstance(value, str):
                raise TypeError(f"{field} must be a string")
            if not value.strip():
                raise ValueError(f"{field} must not be blank")
        if (
            isinstance(self.candidate_version, bool)
            or not isinstance(self.candidate_version, int)
        ):
            raise TypeError("candidate_version must be an integer")
        if self.candidate_version <= 0:
            raise ValueError("candidate_version must be positive")
        if not isinstance(
            self.content_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "content_digest must be a KnowledgeContentDigest"
            )
