import base64
import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from sp001.infrastructure.configured_access_token_keys import ConfiguredAccessTokenKeys
from sp001.infrastructure.jwt_case_access_authenticator import AccessTokenKeyResolutionError
from sp001.infrastructure.jwt_federated_issuance_authenticator import (
    JwtFederatedIssuanceAuthenticator,
)


@pytest.fixture(scope="module")
def key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def verifier(key, resolver=None):
    return JwtFederatedIssuanceAuthenticator(
        issuer="external", audience="issuance-service",
        key_resolver=resolver if resolver is not None else ConfiguredAccessTokenKeys(
            issuer="external", public_keys={"KEY-1": key.public_key()},
        ),
        max_lifetime_seconds=300, max_token_bytes=8192,
    )


def claims():
    now = int(time.time())
    return {
        "iss": "external", "sub": "subject", "aud": "issuance-service",
        "iat": now - 10, "nbf": now - 10, "exp": now + 120,
    }


def token(key, payload=None, **headers):
    return jwt.encode(
        claims() if payload is None else payload, key, algorithm="RS256",
        headers={"kid": "KEY-1", "typ": "at+jwt", **headers},
    )


def test_verified_token_produces_federated_context(key):
    payload = claims()
    result = verifier(key).authenticate(credential=token(key, payload))
    assert result.principal.issuer == "external"
    assert result.principal.subject == "subject"
    assert result.audience == "issuance-service"
    assert result.expires_at == payload["exp"]


@pytest.mark.parametrize("change", [
    {"iss": "other"}, {"sub": ""}, {"aud": "coordinator"},
    {"aud": ["issuance-service"]}, {"iat": True},
    {"exp": int(time.time()) - 1},
    {"nbf": int(time.time()) + 60},
    {"exp": int(time.time()) + 600},
])
def test_invalid_claims_are_rejected(key, change):
    payload = claims()
    payload.update(change)
    assert verifier(key).authenticate(credential=token(key, payload)) is None


@pytest.mark.parametrize("field", ["iss", "sub", "aud", "iat", "nbf", "exp"])
def test_missing_required_claim_is_rejected(key, field):
    payload = claims()
    del payload[field]
    assert verifier(key).authenticate(credential=token(key, payload)) is None


@pytest.mark.parametrize("headers", [
    {"typ": "JWT"}, {"kid": "UNKNOWN"},
    {"jku": "https://untrusted.example/keys"}, {"crit": ["unexpected"]},
])
def test_unaccepted_headers_are_rejected(key, headers):
    assert verifier(key).authenticate(credential=token(key, **headers)) is None


def test_wrong_signature_is_rejected(key):
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    assert verifier(key).authenticate(credential=token(other)) is None


def test_provider_failure_is_not_invalid_token(key):
    class FailedProvider:
        def resolve(self, **kwargs):
            raise TimeoutError("unavailable")

    with pytest.raises(AccessTokenKeyResolutionError):
        verifier(key, FailedProvider()).authenticate(credential=token(key))


def test_invalid_provider_key_is_a_provider_error(key):
    class InvalidProvider:
        def resolve(self, **kwargs):
            return "untrusted key material"

    with pytest.raises(RuntimeError, match="invalid RS256 key"):
        verifier(key, InvalidProvider()).authenticate(credential=token(key))


def test_duplicate_json_is_rejected_before_key_resolution(key):
    valid = token(key)
    parts = valid.split(".")
    raw = b'{"alg":"RS256","kid":"KEY-1","typ":"at+jwt","kid":"OTHER"}'
    parts[0] = base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

    class ForbiddenProvider:
        def resolve(self, **kwargs):
            raise AssertionError("ambiguous token reached provider")

    assert verifier(key, ForbiddenProvider()).authenticate(
        credential=".".join(parts),
    ) is None
