import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from sp001.infrastructure.jwt_case_access_authenticator import (
    JwtCaseAccessAuthenticator, AccessTokenKeyResolutionError,
)
from sp001.infrastructure.authenticated_case_state_http_host import (
    create_authenticated_case_state_app,
)


@pytest.fixture(scope="module")
def credential():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    now = int(time.time())
    return jwt.encode(
        {
            "iss": "issuer-A", "sub": "subscriber-1", "aud": "coordinator",
            "iat": now - 1, "nbf": now - 1, "exp": now + 120,
            "case_permissions": [],
        },
        key, algorithm="RS256", headers={"kid": "key-1", "typ": "at+jwt"},
    )


def verifier(resolver):
    return JwtCaseAccessAuthenticator(
        issuer="issuer-A", audience="coordinator", key_resolver=resolver,
        max_lifetime_seconds=300, max_token_bytes=8192,
    )


@pytest.mark.parametrize("error", [
    ValueError("invalid provider document"),
    TypeError("invalid provider configuration"),
    OSError("provider unavailable"),
    RuntimeError("provider failed"),
])
def test_provider_errors_are_not_credential_rejection(credential, error):
    class Resolver:
        def resolve(self, **kwargs):
            raise error

    with pytest.raises(AccessTokenKeyResolutionError) as caught:
        verifier(Resolver()).authenticate(credential=credential)
    assert caught.value.__cause__ is error


def test_unknown_key_remains_explicit_rejection(credential):
    class Resolver:
        def resolve(self, **kwargs):
            return None

    assert verifier(Resolver()).authenticate(credential=credential) is None


def test_malformed_token_does_not_invoke_resolver():
    class Resolver:
        def resolve(self, **kwargs):
            raise AssertionError("malformed token must not resolve keys")

    assert verifier(Resolver()).authenticate(credential="broken") is None


def test_host_provider_failure_is_500_without_authorization_or_read(credential):
    calls = []

    class Resolver:
        def resolve(self, **kwargs):
            raise ValueError("private provider detail")

    class Authorizer:
        def can_read_case(self, **kwargs):
            calls.append("authorize")
            return True

    class Reader:
        def read(self, **kwargs):
            calls.append("read")
            raise AssertionError("must not read")

    app = create_authenticated_case_state_app(
        reader=Reader(), authenticator=verifier(Resolver()),
        authorizer=Authorizer(), expected_audience="coordinator",
    )
    with TestClient(app) as client:
        response = client.get(
            "/v1/cases/CASE-001/state",
            headers={"Authorization": "Bearer " + credential},
        )
    assert response.status_code == 500
    assert response.json()["code"] == "AUTHENTICATION_PROVIDER_FAILED"
    assert "private" not in response.text
    assert calls == []
