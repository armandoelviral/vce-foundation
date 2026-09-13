from dataclasses import dataclass

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionPolicyIdentity:
    """Exact reusable identity of one admission policy configuration."""

    admission_policy_id: str
    admission_policy_version: int
    configuration_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        if not isinstance(self.admission_policy_id, str):
            raise TypeError("admission_policy_id must be a string")
        if not self.admission_policy_id.strip():
            raise ValueError("admission_policy_id must not be blank")
        if (
            isinstance(self.admission_policy_version, bool)
            or not isinstance(self.admission_policy_version, int)
        ):
            raise TypeError(
                "admission_policy_version must be an integer"
            )
        if self.admission_policy_version <= 0:
            raise ValueError(
                "admission_policy_version must be positive"
            )
        if not isinstance(
            self.configuration_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "configuration_digest must be a KnowledgeContentDigest"
            )
