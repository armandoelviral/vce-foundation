import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from test_federated_case_access_issuance_integration import flow
from test_federated_jwks_https import jwks_host, resolver, primary
from sp001.infrastructure.configured_access_token_keys import ConfiguredAccessTokenKeys
from sp001.infrastructure.case_access_issuer_composition import compose_case_access_issuer
from sp001.infrastructure.sqlite_case_access_issuance_completions import (
    SqliteCaseAccessIssuanceCompletions,
)
from sp001.services.authenticated_case_access_issuance import (
    IssuanceAuthenticationRejected, IssuanceIdentityRejected,
)


@pytest.fixture
def configuration(tmp_path):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return {
        "primary_issuer": "external",
        "primary_audience": "issuance-service",
        "primary_key_resolver": ConfiguredAccessTokenKeys(
            issuer="external", public_keys={"PRIMARY-1": key.public_key()},
        ),
        "max_primary_lifetime_seconds": 300,
        "max_primary_token_bytes": 8192,
        "access_issuer": "access",
        "access_audience": "coordinator",
        "max_access_lifetime_seconds": 120,
        "signing_key_id": "KEY-1",
        "signing_private_key": key,
        "protection_key_id": "PROTECTION-1",
        "protection_key": b"x" * 32,
        "authorization_database_path": tmp_path / "new-authorization.sqlite3",
    }


@pytest.mark.parametrize("change", [
    {"primary_audience": ""},
    {"max_access_lifetime_seconds": 0},
    {"max_primary_lifetime_seconds": True},
    {"signing_key_id": ""},
    {"protection_key": b"short"},
    {"authorization_database_path": "relative.sqlite3"},
    {"clock": 123},
])
def test_invalid_configuration_creates_no_database(configuration, change):
    path = configuration["authorization_database_path"]
    configuration.update(change)
    with pytest.raises((TypeError, ValueError)):
        compose_case_access_issuer(**configuration)
    assert not path.exists()


def test_composition_creates_no_default_authorization(configuration):
    service = compose_case_access_issuer(**configuration)
    store = SqliteCaseAccessIssuanceCompletions(
        database_path=configuration["authorization_database_path"],
    )
    assert store.read_audit() == ()
    assert store.read_prepared(request_id="MISSING") is None
    with pytest.raises(IssuanceAuthenticationRejected):
        service.complete(credential="invalid", request_id="MISSING")

    now = int(time.time())
    credential = jwt.encode(
        {
            "iss": "external", "sub": "subject", "aud": "issuance-service",
            "iat": now - 1, "nbf": now - 1, "exp": now + 120,
        },
        configuration["signing_private_key"], algorithm="RS256",
        headers={"kid": "PRIMARY-1", "typ": "at+jwt"},
    )
    with pytest.raises(IssuanceIdentityRejected):
        service.complete(credential=credential, request_id="MISSING")


def test_composed_issuer_uses_real_https_jwks_and_persistent_recovery(
    configuration, jwks_host, flow, tmp_path,
):
    store, _, preparation, _, _, access_key = flow
    _, _, primary_key, state = jwks_host
    configuration.update(
        primary_key_resolver=resolver(jwks_host),
        signing_private_key=access_key,
        authorization_database_path=tmp_path / "authorization.sqlite3",
    )
    service = compose_case_access_issuer(**configuration)
    credential = primary(primary_key)
    from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest
    preparation = service.prepare_request(
        credential=credential,
        request=CaseAccessIssuanceRequest(
            preparation.request_id,
            preparation.payload.permissions[0].case_id,
            preparation.payload.permissions[0].operation,
        ),
    )
    token = service.complete(
        credential=credential, request_id=preparation.request_id,
    )
    assert jwt.decode(
        token.credential, access_key.public_key(), algorithms=["RS256"],
        issuer="access", audience="coordinator",
    ) == preparation.payload.to_claims()
    historical = store.read_completed(request_id=preparation.request_id)
    assert historical is not None
    assert len(state["requests"]) == 1

    # New composition reopens durable records and establishes its own trust cache.
    reopened = compose_case_access_issuer(**configuration)
    assert reopened.complete(
        credential=credential, request_id=preparation.request_id,
    ) == token
    assert store.read_completed(request_id=preparation.request_id) == historical
    # The explicitly injected resolver remains shared across these compositions.
    assert len(state["requests"]) == 1


def test_composed_boundary_builds_from_limited_request_and_recovers(
    configuration, jwks_host, flow, tmp_path,
):
    from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest

    store, _, template, _, _, access_key = flow
    _, _, primary_key, state = jwks_host
    configuration.update(
        primary_key_resolver=resolver(jwks_host),
        signing_private_key=access_key,
        authorization_database_path=tmp_path / "authorization.sqlite3",
    )
    service = compose_case_access_issuer(**configuration)
    request = CaseAccessIssuanceRequest(
        "LIMITED-COMPOSED", "CASE-001", template.payload.permissions[0].operation,
    )
    credential = primary(primary_key)
    prepared = service.prepare_request(credential=credential, request=request)
    assert prepared.payload.subject == "internal"
    assert prepared.payload.audience == "coordinator"
    assert prepared.payload.permissions == (request.permission,)
    assert prepared.payload.expires_at - prepared.payload.issued_at <= 120
    token = service.complete(credential=credential, request_id=request.request_id)
    assert jwt.decode(
        token.credential, access_key.public_key(), algorithms=["RS256"],
        issuer="access", audience="coordinator",
    ) == prepared.payload.to_claims()

    assert service.prepare_request(credential=credential, request=request) == prepared
    assert service.complete(
        credential=credential, request_id=request.request_id,
    ) == token
    assert store.read_completed(request_id=request.request_id) is not None
    assert len(state["requests"]) == 1
