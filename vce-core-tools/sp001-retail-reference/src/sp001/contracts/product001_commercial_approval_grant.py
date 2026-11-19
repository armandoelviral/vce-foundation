from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeSourceScope,
)


class Product001CommercialApprovalOperation(StrEnum):
    APPROVE_PLANOGRAM_VERSION = "APPROVE_PLANOGRAM_VERSION"


@dataclass(frozen=True, slots=True)
class Product001CommercialApprovalGrant:
    """Configured grant; construction establishes no authority."""

    grant_id: str
    principal: AuthenticatedPrincipal
    operation: Product001CommercialApprovalOperation
    scope: KnowledgeSourceScope
    valid_from: int
    expires_at: int

    def __post_init__(self) -> None:
        if not isinstance(self.grant_id, str):
            raise TypeError("grant_id must be a string")
        if not self.grant_id.strip():
            raise ValueError("grant_id must not be empty")

        if not isinstance(self.principal, AuthenticatedPrincipal):
            raise TypeError("principal must be AuthenticatedPrincipal")

        if not isinstance(
            self.operation, Product001CommercialApprovalOperation
        ):
            raise TypeError("invalid commercial approval operation")

        if not isinstance(self.scope, KnowledgeSourceScope):
            raise TypeError("scope must be KnowledgeSourceScope")

        if self.scope.document_type is not KnowledgeDocumentType.PLANOGRAM:
            raise ValueError("commercial grant requires PLANOGRAM")

        for name in ("valid_from", "expires_at"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be integer Unix seconds")
            if value < 0:
                raise ValueError(f"{name} must not be negative")

        if self.valid_from >= self.expires_at:
            raise ValueError("grant validity interval must be nonempty")
