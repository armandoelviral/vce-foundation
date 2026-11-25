"""MVP1-C: real PRODUCT-001 SQLite integration."""

from dataclasses import replace
import sqlite3

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)

from test_sqlite_product001_commercial_decisions import (
    PRINCIPAL,
    decision,
    grant,
)
from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    CommitmentContextV1,
    commitment_signing_payload,
)
from sp001.contracts.product001_mvp1_contextual_authorization import (
    decision_digest_from_canonical_bytes,
)
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    SqliteProduct001CommercialApproval,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    SqliteProduct001CommercialDecisionWriter,
)
from sp001.services.product001_mvp1_execution_gate import (
    MVP1Authorization,
    MVP1CommitmentAdmission,
    Product001MVP1ExecutionGate,
    authorization_payload,
)


def counts(path):
    with sqlite3.connect(path) as db:
        return tuple(
            db.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            for table in (
                "product001_commercial_decisions",
                "product001_commercial_decision_audit",
            )
        )


@pytest.fixture
def environment(tmp_path):
    path = tmp_path / "product001-mvp1.sqlite"
    grants = SqliteProduct001CommercialApproval(
        database_path=path,
    )
    grants.register_grant(
        event_id="mvp1-grant",
        grant=grant(),
    )
    writer = SqliteProduct001CommercialDecisionWriter(
        database_path=path,
        clock=lambda: 150,
    )
    authority = Ed25519PrivateKey.generate()
    gate = Product001MVP1ExecutionGate(
        writer=writer,
        authority_public_key=authority.public_key(),
    )
    return path, authority, gate


def authorize(authority, value):
    return MVP1Authorization(
        signature=authority.sign(
            authorization_payload(value)
        )
    )


def record(gate, authorization, value=None):
    return gate.record(
        authorization=authorization,
        decision=value if value is not None else decision(),
        authenticated_principal=PRINCIPAL,
    )


def test_missing_authorization_denied(environment):
    path, _, gate = environment
    with pytest.raises(PermissionError):
        record(gate, None)
    assert counts(path) == (0, 0)


def test_signed_authorization_creates_real_effect(environment):
    path, authority, gate = environment
    value = decision()
    token = authorize(authority, value)

    assert record(gate, token, value) is True
    assert counts(path) == (1, 1)


def test_forged_authorization_denied(environment):
    path, _, gate = environment
    attacker = Ed25519PrivateKey.generate()
    forged = authorize(attacker, decision())

    with pytest.raises(PermissionError):
        record(gate, forged)

    assert counts(path) == (0, 0)


def test_modified_decision_denied(environment):
    path, authority, gate = environment
    original = decision()
    token = authorize(authority, original)
    modified = replace(
        original,
        evidence_reference="tampered-evidence",
    )

    with pytest.raises(PermissionError):
        record(gate, token, modified)

    assert counts(path) == (0, 0)


def test_replay_is_idempotent(environment):
    path, authority, gate = environment
    value = decision()
    token = authorize(authority, value)

    assert record(gate, token, value) is True
    assert record(gate, token, value) is False
    assert counts(path) == (1, 1)


def test_wrong_trust_root_denied(environment):
    path, authority, gate = environment
    other_authority = Ed25519PrivateKey.generate()
    token = authorize(other_authority, decision())

    with pytest.raises(PermissionError):
        record(gate, token)

    assert counts(path) == (0, 0)



def signed_commitment(authority, value):
    context = CommitmentContextV1(
        issuer_id="external-issuer",
        organization_id=value.document_scope.organization_id,
        operation_id=value.decision_id,
        authorization_digest="a" * 64,
        decision_digest=decision_digest_from_canonical_bytes(authorization_payload(value)),
        materialize_deadline=160,
    )
    return CommitmentCertificateV1(
        context, authority.sign(commitment_signing_payload(context)),
    )


def test_commitment_gate_checks_independent_configuration_before_writing(environment):
    path, authority, _ = environment
    value = decision()
    certificate = signed_commitment(authority, value)
    contexts = {}
    now = 150
    admission = MVP1CommitmentAdmission(
        public_key=authority.public_key(),
        resolve_context=lambda org, operation: contexts.get((org, operation)),
        clock=lambda: now,
    )
    gate = Product001MVP1ExecutionGate(
        writer=SqliteProduct001CommercialDecisionWriter(
            database_path=path, clock=lambda: 150,
        ),
        commitment_admission=admission,
    )

    with pytest.raises(PermissionError, match="context unavailable"):
        record(gate, certificate, value)
    contexts[("org", value.decision_id)] = certificate.context

    attacker = Ed25519PrivateKey.generate()
    for token, candidate in (
        (None, value),
        (authorize(authority, value), value),
        (signed_commitment(attacker, value), value),
        (certificate, replace(value, evidence_reference="different")),
    ):
        with pytest.raises(PermissionError):
            record(gate, token, candidate)
    assert counts(path) == (0, 0)

    assert record(gate, certificate, value) is True
    assert record(gate, certificate, value) is False
    now = certificate.context.materialize_deadline
    with pytest.raises(PermissionError, match="deadline expired"):
        record(gate, certificate, value)
    assert counts(path) == (1, 1)
