"""MVP1: protected logical composition for PRODUCT-001 approval.

Experimental in-process composition.
Not an OS privilege boundary or commercial admission guarantee.
"""

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PublicKey,
)

from sp001.contracts.product001_mvp1_commitment_certificate import CommitmentCertificateV1
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
)
from sp001.services.authenticated_product001_commercial_approval import (
    AuthenticatedProduct001CommercialApproval,
)
from sp001.services.product001_mvp1_execution_gate import (
    MVP1Authorization,
    MVP1CommitmentAdmission,
    configure_mvp1_admission,
)


class Product001MVP1ProtectedApproval:
    __slots__ = (
        "__authenticated_service", "__verify_authorization", "__requires_commitment",
    )

    def __init__(
        self,
        *,
        authenticated_service: AuthenticatedProduct001CommercialApproval,
        authority_public_key: Ed25519PublicKey | None = None,
        commitment_admission: MVP1CommitmentAdmission | None = None,
    ):
        if not isinstance(
            authenticated_service,
            AuthenticatedProduct001CommercialApproval,
        ):
            raise TypeError("invalid authenticated approval service")

        self.__verify_authorization = configure_mvp1_admission(
            authority_public_key=authority_public_key,
            commitment_admission=commitment_admission,
        )
        self.__authenticated_service = authenticated_service
        self.__requires_commitment = commitment_admission is not None

    @property
    def requires_commitment_certificate(self) -> bool:
        return self.__requires_commitment

    def record(
        self,
        *,
        credential: str,
        decision: Product001CommercialApprovalDecision,
        authorization: MVP1Authorization | CommitmentCertificateV1,
    ) -> bool:
        if not isinstance(decision, Product001CommercialApprovalDecision):
            raise TypeError("invalid commercial decision")

        self.__verify_authorization(authorization=authorization, decision=decision)
        return self.__authenticated_service.record(
            credential=credential,
            decision=decision,
        )


def compose_product001_mvp1_protected_approval(
    *,
    authenticated_service: AuthenticatedProduct001CommercialApproval,
    authority_public_key: Ed25519PublicKey | None = None,
    commitment_admission: MVP1CommitmentAdmission | None = None,
) -> Product001MVP1ProtectedApproval:
    return Product001MVP1ProtectedApproval(
        authenticated_service=authenticated_service,
        commitment_admission=commitment_admission,
        authority_public_key=authority_public_key,
    )
