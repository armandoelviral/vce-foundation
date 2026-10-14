import json

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from sp001.infrastructure import jwks_access_token_keys as module


@pytest.fixture(scope="module")
def jwk():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    value = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    value.update(kid="key-1", alg="RS256", use="sig")
    return value


def setup(monkeypatch, jwk):
    clock = {"now": 0.0}
    monkeypatch.setattr(module.time, "monotonic", lambda: clock["now"])
    resolver = module.JwksAccessTokenKeys(
        issuer="issuer-A", jwks_url="https://keys.example/jwks",
        cache_ttl_seconds=60, min_refresh_interval_seconds=10,
        timeout_seconds=1, max_response_bytes=8192, max_keys=10,
    )
    calls = []
    response = {"body": json.dumps({"keys": [jwk]}).encode(), "error": None}

    def fetch():
        calls.append("fetch")
        if response["error"] is not None:
            raise response["error"]
        return response["body"]

    monkeypatch.setattr(resolver, "_fetch", fetch)
    return resolver, clock, calls, response


def resolve(resolver, kid="key-1"):
    return resolver.resolve(issuer="issuer-A", key_id=kid, algorithm="RS256")


def test_known_key_uses_fresh_cache_without_network(monkeypatch, jwk):
    resolver, clock, calls, response = setup(monkeypatch, jwk)
    first = resolve(resolver)
    assert resolve(resolver) is first
    assert calls == ["fetch"]


def test_unknown_key_refresh_is_bounded(monkeypatch, jwk):
    resolver, clock, calls, response = setup(monkeypatch, jwk)
    resolve(resolver)
    assert resolve(resolver, "unknown") is None
    assert calls == ["fetch"]
    clock["now"] = 10
    assert resolve(resolver, "unknown") is None
    assert resolve(resolver, "another-unknown") is None
    assert calls == ["fetch", "fetch"]


def test_rotation_replaces_snapshot_and_removes_retired_key(monkeypatch, jwk):
    resolver, clock, calls, response = setup(monkeypatch, jwk)
    resolve(resolver)
    rotated = dict(jwk, kid="key-2")
    response["body"] = json.dumps({"keys": [rotated]}).encode()
    clock["now"] = 10
    assert resolve(resolver, "key-2") is not None
    assert resolve(resolver, "key-1") is None


def test_expired_cache_is_not_used_on_refresh_failure(monkeypatch, jwk):
    resolver, clock, calls, response = setup(monkeypatch, jwk)
    resolve(resolver)
    clock["now"] = 60
    response["error"] = OSError("endpoint unavailable")
    with pytest.raises(OSError):
        resolve(resolver)
    with pytest.raises(RuntimeError, match="rate limited"):
        resolve(resolver)
    assert calls == ["fetch", "fetch"]


def test_failed_refresh_does_not_corrupt_still_fresh_known_key(monkeypatch, jwk):
    resolver, clock, calls, response = setup(monkeypatch, jwk)
    original = resolve(resolver)
    clock["now"] = 10
    response["body"] = b"invalid JSON"
    with pytest.raises(ValueError):
        resolve(resolver, "new-key")
    assert resolve(resolver) is original


@pytest.mark.parametrize("change", ["duplicate", "private", "wrong_shape"])
def test_invalid_jwks_is_rejected(monkeypatch, jwk, change):
    resolver, clock, calls, response = setup(monkeypatch, jwk)
    document = {"keys": [jwk]}
    if change == "duplicate":
        document["keys"] *= 2
    elif change == "private":
        document["keys"] = [dict(jwk, d="private")]
    else:
        document = {"keys": {}}
    response["body"] = json.dumps(document).encode()
    with pytest.raises(ValueError):
        resolve(resolver)


def test_untrusted_issuer_or_algorithm_never_fetches(monkeypatch, jwk):
    resolver, clock, calls, response = setup(monkeypatch, jwk)
    assert resolver.resolve(issuer="other", key_id="key-1", algorithm="RS256") is None
    assert resolver.resolve(issuer="issuer-A", key_id="key-1", algorithm="HS256") is None
    assert calls == []
