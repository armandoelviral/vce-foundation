import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from sp001.contracts.case_access_context import CaseAccessOperation
from sp001.contracts.case_state_read_result import NotFound
from sp001.infrastructure.jwt_case_access_authenticator import (
    JwtCaseAccessAuthenticator,
)
from sp001.infrastructure.authenticated_case_state_http_host import (
    create_authenticated_case_state_app,
)


@pytest.fixture(scope="module")
def key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def claims():
    now = int(time.time())
    return {
        "iss": "https://issuer.example",
        "sub": "subscriber-1",
        "aud": "sp001-coordinator",
        "iat": now - 1,
        "nbf": now - 1,
        "exp": now + 120,
        "case_permissions": [
            {"case_id": "CASE-001", "operation": "READ_STATE"},
        ],
    }


def verifier(key):
    return JwtCaseAccessAuthenticator(
        issuer="https://issuer.example",
        audience="sp001-coordinator",
        public_keys={"key-1": key.public_key()},
        max_lifetime_seconds=300,
        max_token_bytes=8192,
    )


def token(key, payload=None, headers=None):
    return jwt.encode(
        claims() if payload is None else payload,
        key,
        algorithm="RS256",
        headers={"kid": "key-1", "typ": "at+jwt"} if headers is None else headers,
    )


def test_valid_signature_produces_complete_access_context(key):
    access = verifier(key).authenticate(credential=token(key))
    assert access is not None
    assert access.principal.issuer == "https://issuer.example"
    assert access.principal.subject == "subscriber-1"
    assert access.audience == "sp001-coordinator"
    assert access.permissions[0].case_id == "CASE-001"
    assert access.permissions[0].operation is CaseAccessOperation.READ_STATE


def test_signature_from_untrusted_key_is_rejected(key):
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    assert verifier(key).authenticate(credential=token(other)) is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("iss", "https://other.example"),
        ("aud", "sp001-sse"),
        ("aud", ["sp001-coordinator"]),
        ("sub", ""),
        ("sub", 42),
        ("iat", True),
        ("nbf", True),
        ("exp", True),
        ("exp", "9999999999"),
        ("case_permissions", {}),
        ("case_permissions", [{"case_id": "CASE-001", "operation": "ADMIN"}]),
        ("case_permissions", [{"case_id": "", "operation": "READ_STATE"}]),
    ],
)
def test_invalid_claims_are_rejected(key, field, value):
    payload = claims()
    payload[field] = value
    assert verifier(key).authenticate(credential=token(key, payload)) is None


@pytest.mark.parametrize("field", ["iss", "sub", "aud", "iat", "nbf", "exp", "case_permissions"])
def test_required_claims_cannot_be_omitted(key, field):
    payload = claims()
    del payload[field]
    assert verifier(key).authenticate(credential=token(key, payload)) is None


@pytest.mark.parametrize("kind", ["expired", "future", "too_long", "duplicates"])
def test_time_and_permission_constraints_are_enforced(key, kind):
    payload = claims()
    now = int(time.time())
    if kind == "expired":
        payload.update(iat=now - 20, nbf=now - 20, exp=now - 1)
    elif kind == "future":
        payload.update(iat=now + 10, nbf=now + 10, exp=now + 20)
    elif kind == "too_long":
        payload["exp"] = now + 1000
    else:
        payload["case_permissions"] *= 2
    assert verifier(key).authenticate(credential=token(key, payload)) is None


@pytest.mark.parametrize(
    "headers",
    [
        {"kid": "unknown", "typ": "at+jwt"},
        {"kid": "key-1", "typ": "JWT"},
        {"kid": "key-1", "typ": "at+jwt", "jku": "https://untrusted.example/keys"},
        {"kid": "key-1", "typ": "at+jwt", "crit": ["custom"]},
    ],
)
def test_unapproved_headers_are_rejected(key, headers):
    assert verifier(key).authenticate(credential=token(key, headers=headers)) is None


def test_unsigned_and_symmetric_tokens_are_rejected(key):
    unsigned = jwt.encode(
        claims(), key="", algorithm="none",
        headers={"kid": "key-1", "typ": "at+jwt"},
    )
    symmetric = jwt.encode(
        claims(), key=b"x" * 32, algorithm="HS256",
        headers={"kid": "key-1", "typ": "at+jwt"},
    )
    assert verifier(key).authenticate(credential=unsigned) is None
    assert verifier(key).authenticate(credential=symmetric) is None


@pytest.mark.parametrize("credential", ["", "broken", "a" * 8193, "ñ"])
def test_malformed_or_oversized_credentials_are_rejected(key, credential):
    assert verifier(key).authenticate(credential=credential) is None


def test_config_requires_public_key_not_private_key(key):
    with pytest.raises(TypeError):
        JwtCaseAccessAuthenticator(
            issuer="issuer", audience="audience", public_keys={"key-1": key},
            max_lifetime_seconds=300, max_token_bytes=8192,
        )


def test_signed_token_passes_host_but_permission_remains_case_specific(key):
    calls = []

    class Reader:
        def read(self, *, case_id):
            calls.append(case_id)
            return NotFound(case_id)

    class Authorizer:
        def can_read_case(self, *, access, case_id):
            return True

    app = create_authenticated_case_state_app(
        reader=Reader(), authenticator=verifier(key), authorizer=Authorizer(),
        expected_audience="sp001-coordinator",
    )
    headers = {"Authorization": "Bearer " + token(key)}
    with TestClient(app) as client:
        allowed = client.get(
            "/v1/cases/CASE-001/state", headers=headers,
        )
        denied = client.get(
            "/v1/cases/OTHER/state", headers=headers,
        )
        invalid = client.get(
            "/v1/cases/CASE-001/state",
            headers={"Authorization": "Bearer broken"},
        )
    assert allowed.status_code == 404
    assert allowed.json()["code"] == "CASE_NOT_FOUND"
    assert denied.status_code == 403
    assert invalid.status_code == 401
    assert calls == ["CASE-001"]
