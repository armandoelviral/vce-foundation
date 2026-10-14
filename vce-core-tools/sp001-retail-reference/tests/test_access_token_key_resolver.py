import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from sp001.infrastructure.configured_access_token_keys import ConfiguredAccessTokenKeys
from sp001.infrastructure.jwt_case_access_authenticator import JwtCaseAccessAuthenticator


@pytest.fixture(scope="module")
def key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def token(key):
    now = int(time.time())
    return jwt.encode(
        {
            "iss": "issuer-A", "sub": "subscriber-1", "aud": "coordinator",
            "iat": now - 1, "nbf": now - 1, "exp": now + 60,
            "case_permissions": [],
        },
        key, algorithm="RS256", headers={"kid": "key-1", "typ": "at+jwt"},
    )


@pytest.mark.parametrize("issuer,kid,algorithm", [
    ("issuer-B", "key-1", "RS256"),
    ("issuer-A", "unknown", "RS256"),
    ("issuer-A", "key-1", "HS256"),
])
def test_resolution_requires_exact_trust_tuple(key, issuer, kid, algorithm):
    resolver = ConfiguredAccessTokenKeys(
        issuer="issuer-A", public_keys={"key-1": key.public_key()}
    )
    assert resolver.resolve(
        issuer=issuer, key_id=kid, algorithm=algorithm
    ) is None


def test_configured_snapshot_does_not_follow_mapping_mutations(key):
    public = key.public_key()
    mapping = {"key-1": public}
    resolver = ConfiguredAccessTokenKeys(issuer="issuer-A", public_keys=mapping)
    mapping.clear()
    assert resolver.resolve(
        issuer="issuer-A", key_id="key-1", algorithm="RS256"
    ) is public


def test_verifier_uses_configured_issuer_for_resolution(key):
    calls = []

    class Resolver:
        def resolve(self, *, issuer, key_id, algorithm):
            calls.append((issuer, key_id, algorithm))
            return key.public_key()

    verifier = JwtCaseAccessAuthenticator(
        issuer="issuer-A", audience="coordinator", key_resolver=Resolver(),
        max_lifetime_seconds=120, max_token_bytes=8192,
    )
    assert verifier.authenticate(credential=token(key)) is not None
    assert calls == [("issuer-A", "key-1", "RS256")]


def test_resolver_unavailability_propagates(key):
    class Resolver:
        def resolve(self, **kwargs):
            raise RuntimeError("key source unavailable")

    verifier = JwtCaseAccessAuthenticator(
        issuer="issuer-A", audience="coordinator", key_resolver=Resolver(),
        max_lifetime_seconds=120, max_token_bytes=8192,
    )
    with pytest.raises(RuntimeError):
        verifier.authenticate(credential=token(key))


def test_invalid_resolver_key_is_provider_failure(key):
    class Resolver:
        def resolve(self, **kwargs):
            return "not a trusted public key"

    verifier = JwtCaseAccessAuthenticator(
        issuer="issuer-A", audience="coordinator", key_resolver=Resolver(),
        max_lifetime_seconds=120, max_token_bytes=8192,
    )
    with pytest.raises(RuntimeError):
        verifier.authenticate(credential=token(key))


def test_ambiguous_or_missing_key_configuration_is_rejected(key):
    options = dict(
        issuer="issuer-A", audience="coordinator",
        max_lifetime_seconds=120, max_token_bytes=8192,
    )
    with pytest.raises(ValueError):
        JwtCaseAccessAuthenticator(**options)
    with pytest.raises(ValueError):
        JwtCaseAccessAuthenticator(
            **options, public_keys={"key-1": key.public_key()},
            key_resolver=ConfiguredAccessTokenKeys(
                issuer="issuer-A", public_keys={"key-1": key.public_key()}
            ),
        )
