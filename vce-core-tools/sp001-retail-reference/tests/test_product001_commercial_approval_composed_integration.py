"""Real JWT, documentary storage and SQLite composition integration."""

from dataclasses import replace
import sqlite3
import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from sp001.infrastructure.configured_access_token_keys import (
    ConfiguredAccessTokenKeys,
)
from sp001.infrastructure.product001_commercial_approval_composition import (
    compose_product001_commercial_approval,
)
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    SqliteProduct001CommercialApproval,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    CommercialDecisionDenied,
)
from sp001.services.authenticated_product001_commercial_approval import (
    CommercialAuthenticationRejected,
)
from sp001.services.product001_commercial_document_verification import (
    CommercialDocumentVerificationRejected,
)

from test_authenticated_product001_commercial_approval import grant
from test_authenticated_product001_commercial_document_integration import (
    decision_counts,
    publish,
)
from test_product001_commercial_document_verification import (
    matching_decision,
)


@pytest.fixture
def environment(tmp_path):
    now = int(time.time())

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    database = tmp_path / "commercial.sqlite"
    documents = tmp_path / "documents"
    documents.mkdir()

    resolver = ConfiguredAccessTokenKeys(
        issuer="issuer",
        public_keys={"KEY-1": private_key.public_key()},
    )

    service = compose_product001_commercial_approval(
        issuer="issuer",
        audience="commercial",
        key_resolver=resolver,
        max_lifetime_seconds=300,
        max_token_bytes=8192,
        database_path=database,
        documentary_storage_root=documents,
        clock=lambda: int(time.time()),
    )

    grants = SqliteProduct001CommercialApproval(
        database_path=database,
    )

    current_grant = replace(
        grant(),
        valid_from=now - 60,
        expires_at=now + 180,
    )

    grants.register_grant(
        event_id="g1",
        grant=current_grant,
    )

    claims = {
        "iss": "issuer",
        "sub": "approver",
        "aud": "commercial",
        "iat": now - 10,
        "nbf": now - 10,
        "exp": now + 120,
    }

    def credential(payload=None, signing_key=None):
        return jwt.encode(
            claims if payload is None else payload,
            private_key if signing_key is None else signing_key,
            algorithm="RS256",
            headers={"kid": "KEY-1", "typ": "at+jwt"},
        )

    return {
        "service": service,
        "database": database,
        "grants": grants,
        "grant": current_grant,
        "credential": credential,
        "tmp_path": tmp_path,
    }


def assert_no_decision(environment):
    assert decision_counts(environment["database"]) == (0, 0)


def test_valid_jwt_grant_and_document_commit_decision(environment):
    document = matching_decision()
    publish(environment["tmp_path"], document)

    assert environment["service"].record(
        credential=environment["credential"](),
        decision=document,
    ) is True

    assert decision_counts(environment["database"]) == (1, 1)


def test_invalid_signature_persists_nothing(environment):
    document = matching_decision()
    publish(environment["tmp_path"], document)

    other_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    with pytest.raises(CommercialAuthenticationRejected):
        environment["service"].record(
            credential=environment["credential"](
                signing_key=other_key
            ),
            decision=document,
        )

    assert_no_decision(environment)


def test_wrong_audience_persists_nothing(environment):
    document = matching_decision()
    publish(environment["tmp_path"], document)

    now = int(time.time())
    claims = {
        "iss": "issuer",
        "sub": "approver",
        "aud": "wrong-audience",
        "iat": now - 10,
        "nbf": now - 10,
        "exp": now + 120,
    }

    with pytest.raises(CommercialAuthenticationRejected):
        environment["service"].record(
            credential=environment["credential"](payload=claims),
            decision=document,
        )

    assert_no_decision(environment)


def test_missing_document_persists_nothing(environment):
    with pytest.raises(
        CommercialDocumentVerificationRejected
    ) as error:
        environment["service"].record(
            credential=environment["credential"](),
            decision=matching_decision(),
        )

    assert error.value.status == "ABSENT"
    assert_no_decision(environment)


def test_revoked_grant_persists_nothing(environment):
    document = matching_decision()
    publish(environment["tmp_path"], document)

    environment["grants"].revoke_grant(
        event_id="g2",
        grant=environment["grant"],
    )

    with pytest.raises(CommercialDecisionDenied):
        environment["service"].record(
            credential=environment["credential"](),
            decision=document,
        )

    assert_no_decision(environment)
