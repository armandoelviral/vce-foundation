"""MVP1-F.4B.2D: transaction and request isolation tests."""

from dataclasses import replace

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from sp001.infrastructure.product001_mvp1_protected_composition import (
    compose_product001_mvp1_protected_approval,
)
from sp001.services.product001_mvp1_execution_gate import (
    MVP1Authorization,
    MVP1CommitmentAdmission,
    authorization_payload,
)
from sp001.services.product001_commercial_document_verification import (
    CommercialDocumentVerificationRejected,
)

from test_authenticated_product001_commercial_approval import (
    StubAuthenticator,
    context,
    grant,
)
from test_authenticated_product001_commercial_document_integration import (
    build_environment,
    decision_counts,
    publish,
)
from test_product001_mvp1_gate_integration import signed_commitment
from test_product001_commercial_document_verification import (
    matching_decision,
)


def authorize(authority, decision):
    return MVP1Authorization(
        signature=authority.sign(authorization_payload(decision))
    )


def test_document_rejection_inside_transaction_rolls_back(tmp_path):
    decision = matching_decision()
    calls = [0]

    class ChangingVerifier:
        def verify(self, *, decision):
            calls[0] += 1
            if calls[0] == 2:
                raise CommercialDocumentVerificationRejected("INVALID")

    database, authenticated = build_environment(
        tmp_path,
        verifier=ChangingVerifier(),
    )
    authority = Ed25519PrivateKey.generate()

    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=authenticated,
        authority_public_key=authority.public_key(),
    )

    with pytest.raises(CommercialDocumentVerificationRejected):
        protected.record(
            credential="valid",
            decision=decision,
            authorization=authorize(authority, decision),
        )

    assert calls[0] == 2
    assert decision_counts(database) == (0, 0)


def test_authorization_cannot_cross_decisions(tmp_path):
    database, authenticated = build_environment(tmp_path)
    authority = Ed25519PrivateKey.generate()

    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=authenticated,
        authority_public_key=authority.public_key(),
    )

    first = matching_decision()
    second = replace(
        first,
        decision_id="decision-2",
        evidence_reference="evidence-2",
    )

    first_authorization = authorize(authority, first)
    second_authorization = authorize(authority, second)

    with pytest.raises(PermissionError):
        protected.record(
            credential="valid",
            decision=second,
            authorization=first_authorization,
        )

    with pytest.raises(PermissionError):
        protected.record(
            credential="valid",
            decision=first,
            authorization=second_authorization,
        )

    assert decision_counts(database) == (0, 0)



def test_protected_entry_requires_commitment_before_authenticated_write(tmp_path):
    database, authenticated = build_environment(tmp_path)
    authority = Ed25519PrivateKey.generate()
    decision = matching_decision()
    publish(tmp_path, decision)
    certificate = signed_commitment(authority, decision)
    protected = compose_product001_mvp1_protected_approval(
        authenticated_service=authenticated,
        commitment_admission=MVP1CommitmentAdmission(
            public_key=authority.public_key(),
            resolve_context=lambda org, operation: certificate.context,
            clock=lambda: 150,
        ),
    )
    with pytest.raises(PermissionError, match="durable commitment certificate required"):
        protected.record(
            credential="valid", decision=decision, authorization=authorize(authority, decision),
        )
    assert decision_counts(database) == (0, 0)
    assert protected.record(credential="valid", decision=decision, authorization=certificate)
    assert decision_counts(database) == (1, 1)
