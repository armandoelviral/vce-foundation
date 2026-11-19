from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.knowledge_source_identity import KnowledgeSourceIdentity
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeSourceScope,
)
from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)


class Product001CommercialDecision(StrEnum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class Product001CommercialApprovalDecision:
    """Declared decision; construction establishes no approval authority."""

    decision_id: str
    document_identity: KnowledgeSourceIdentity
    document_scope: KnowledgeSourceScope
    version_binding: Product001DocumentVersionBinding
    principal: AuthenticatedPrincipal
    authorization_grant_id: str
    decision: Product001CommercialDecision
    decided_at: int
    evidence_reference: str

    def __post_init__(self) -> None:
        for name in (
            "decision_id",
            "authorization_grant_id",
            "evidence_reference",
        ):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")

        if not isinstance(self.document_identity, KnowledgeSourceIdentity):
            raise TypeError("invalid document identity")

        if not isinstance(self.document_scope, KnowledgeSourceScope):
            raise TypeError("invalid document scope")

        if self.document_scope.document_type is not KnowledgeDocumentType.PLANOGRAM:
            raise ValueError("decision requires PLANOGRAM")

        if not isinstance(
            self.version_binding, Product001DocumentVersionBinding
        ):
            raise TypeError("invalid document version binding")

        if not isinstance(self.principal, AuthenticatedPrincipal):
            raise TypeError("invalid principal")

        if not isinstance(self.decision, Product001CommercialDecision):
            raise TypeError("invalid commercial decision")

        if type(self.decided_at) is not int:
            raise TypeError("decided_at must be integer Unix seconds")

        if self.decided_at < 0:
            raise ValueError("decided_at must not be negative")

        if (
            self.document_identity.source_id
            != self.version_binding.source_id
        ):
            raise ValueError("source identity mismatch")

        if (
            self.document_identity.source_version
            != self.version_binding.document_version
        ):
            raise ValueError("document version mismatch")

        if (
            self.document_scope.campaign_id
            != self.version_binding.campaign_id
        ):
            raise ValueError("campaign mismatch")

        pos_scope = self.document_scope.point_of_sale_scope
        if (
            pos_scope.mode is KnowledgeScopeMode.EXPLICIT
            and self.version_binding.point_of_sale_id not in pos_scope.ids
        ):
            raise ValueError("point of sale outside document scope")
