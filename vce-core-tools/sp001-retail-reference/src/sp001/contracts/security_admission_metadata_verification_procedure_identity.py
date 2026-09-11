from dataclasses import dataclass

from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionMetadataVerificationProcedureIdentity:
    """Versioned verifier and exact configuration-byte identity."""

    verification_procedure_id: str
    verifier_id: str
    verifier_version: str
    configuration_digest: KnowledgeContentDigest

    def __post_init__(self) -> None:
        string_fields = {
            "verification_procedure_id": self.verification_procedure_id,
            "verifier_id": self.verifier_id,
            "verifier_version": self.verifier_version,
        }
        for field, value in string_fields.items():
            if not isinstance(value, str):
                raise TypeError(f"{field} must be a string")
            if not value.strip():
                raise ValueError(f"{field} must not be blank")
        if not isinstance(
            self.configuration_digest,
            KnowledgeContentDigest,
        ):
            raise TypeError(
                "configuration_digest must be a "
                "KnowledgeContentDigest"
            )
