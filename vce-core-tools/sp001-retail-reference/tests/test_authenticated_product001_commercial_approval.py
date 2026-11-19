from dataclasses import replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
    Product001CommercialDecision,
)
from sp001.contracts.product001_commercial_approval_grant import (
    Product001CommercialApprovalGrant,
    Product001CommercialApprovalOperation,
)
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    SqliteProduct001CommercialApproval,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    CommercialDecisionDenied,
    SqliteProduct001CommercialDecisionWriter,
)
from sp001.services.authenticated_product001_commercial_approval import (
    AuthenticatedProduct001CommercialApproval,
    CommercialAuthenticationRejected,
    CommercialIdentityRejected,
)


PRINCIPAL = AuthenticatedPrincipal(
    issuer="issuer", subject="approver"
)


def scope():
    return KnowledgeSourceScope(
        organization_id="org",
        customer_id="customer",
        jurisdiction="MX",
        commercial_channel_id="retail",
        document_type=KnowledgeDocumentType.PLANOGRAM,
        point_of_sale_scope=KnowledgeScopeSelection(
            KnowledgeScopeMode.EXPLICIT, ("pos-1",)
        ),
        department_scope=KnowledgeScopeSelection(
            KnowledgeScopeMode.ALL, ()
        ),
        campaign_id="campaign",
    )


def decision():
    return Product001CommercialApprovalDecision(
        decision_id="decision-1",
        document_identity=KnowledgeSourceIdentity(
            source_id="source-1",
            source_version="v1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value="a" * 64,
            ),
        ),
        document_scope=scope(),
        version_binding=Product001DocumentVersionBinding(
            source_id="source-1",
            commercial_version=1,
            document_version="v1",
            point_of_sale_id="pos-1",
            campaign_id="campaign",
        ),
        principal=PRINCIPAL,
        authorization_grant_id="grant-1",
        decision=Product001CommercialDecision.APPROVED,
        decided_at=150,
        evidence_reference="evidence-1",
    )


def grant():
    return Product001CommercialApprovalGrant(
        grant_id="grant-1",
        principal=PRINCIPAL,
        operation=(
            Product001CommercialApprovalOperation
            .APPROVE_PLANOGRAM_VERSION
        ),
        scope=scope(),
        valid_from=100,
        expires_at=200,
    )


class StubAuthenticator:
    def __init__(self, context):
        self.context = context
        self.failure = None

    def authenticate(self, *, credential):
        if self.failure is not None:
            raise self.failure
        return self.context


def context(*, audience="commercial", expires_at=200):
    return ValidatedFederatedIssuanceContext(
        principal=PRINCIPAL,
        audience=audience,
        issued_at=100,
        not_before=100,
        expires_at=expires_at,
    )


class AcceptingDocumentVerifier:
    """Controlled document verifier for authentication-only tests."""

    def verify(self, *, decision):
        return None


@pytest.fixture
def environment(tmp_path):
    path = tmp_path / "commercial.sqlite"
    grants = SqliteProduct001CommercialApproval(
        database_path=path
    )
    grants.register_grant(event_id="g1", grant=grant())

    now = [150]
    authenticator = StubAuthenticator(context())
    writer = SqliteProduct001CommercialDecisionWriter(
        database_path=path, clock=lambda: now[0]
    )
    service = AuthenticatedProduct001CommercialApproval(
        authenticator=authenticator,
        writer=writer,
        document_verifier=AcceptingDocumentVerifier(),
        expected_audience="commercial",
        clock=lambda: now[0],
    )
    return grants, authenticator, writer, service, now


def test_authenticated_decision(environment):
    _, _, _, service, _ = environment
    assert service.record(
        credential="valid", decision=decision()
    )


def test_authenticated_replay(environment):
    _, _, _, service, _ = environment
    assert service.record(
        credential="valid", decision=decision()
    )
    assert not service.record(
        credential="valid", decision=decision()
    )


def test_missing_credential(environment):
    _, _, _, service, _ = environment
    with pytest.raises(CommercialAuthenticationRejected):
        service.record(credential="", decision=decision())


def test_rejected_credential(environment):
    _, authenticator, _, service, _ = environment
    authenticator.context = None
    with pytest.raises(CommercialAuthenticationRejected):
        service.record(credential="invalid", decision=decision())


def test_wrong_audience(environment):
    _, authenticator, _, service, _ = environment
    authenticator.context = context(audience="other")
    with pytest.raises(CommercialAuthenticationRejected):
        service.record(credential="valid", decision=decision())


def test_expired_credential(environment):
    _, authenticator, _, service, _ = environment
    authenticator.context = context(expires_at=150)
    with pytest.raises(CommercialAuthenticationRejected):
        service.record(credential="valid", decision=decision())


def test_identity_spoofing_rejected(environment):
    _, _, _, service, _ = environment
    forged = replace(
        decision(),
        principal=AuthenticatedPrincipal(
            issuer="issuer", subject="other"
        ),
    )
    with pytest.raises(CommercialIdentityRejected):
        service.record(credential="valid", decision=forged)


def test_revoked_grant_rejected(environment):
    grants, _, _, service, _ = environment
    grants.revoke_grant(event_id="g2", grant=grant())
    with pytest.raises(CommercialDecisionDenied):
        service.record(credential="valid", decision=decision())


def test_authenticator_failure_propagates(environment):
    _, authenticator, _, service, _ = environment
    authenticator.failure = RuntimeError("provider unavailable")
    with pytest.raises(RuntimeError, match="provider unavailable"):
        service.record(credential="valid", decision=decision())


def test_expiry_inside_transaction_rejected(environment):
    grants, _, writer, _, now = environment

    # Keep the commercial grant valid when the credential expires.
    grants.revoke_grant(event_id="g2", grant=grant())
    extended_grant = replace(
        grant(), grant_id="grant-extended", expires_at=300
    )
    grants.register_grant(
        event_id="g3", grant=extended_grant
    )

    class AdvancingWriter:
        def save_decision(self, **kwargs):
            now[0] = 200
            return writer.save_decision(**kwargs)

    service = AuthenticatedProduct001CommercialApproval(
        authenticator=StubAuthenticator(context()),
        writer=AdvancingWriter(),
        document_verifier=AcceptingDocumentVerifier(),
        expected_audience="commercial",
        clock=lambda: now[0],
    )

    extended_decision = replace(
        decision(), authorization_grant_id="grant-extended"
    )
    with pytest.raises(CommercialAuthenticationRejected):
        service.record(
            credential="valid", decision=extended_decision
        )


def test_invalid_authenticator_result(environment):
    _, authenticator, _, service, _ = environment
    authenticator.context = object()
    with pytest.raises(TypeError):
        service.record(credential="valid", decision=decision())
