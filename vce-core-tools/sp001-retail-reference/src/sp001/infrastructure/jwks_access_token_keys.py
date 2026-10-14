import http.client
import json
import math
import ssl
import threading
import time
from urllib.parse import urlsplit

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


class JwksAccessTokenKeys:
    """Configured HTTPS JWKS source; no discovery, redirects or stale-key fallback."""

    def __init__(
        self, *, issuer: str, jwks_url: str,
        cache_ttl_seconds: float, min_refresh_interval_seconds: float,
        timeout_seconds: float, max_response_bytes: int, max_keys: int,
        ca_file: str | None = None,
    ) -> None:
        if not isinstance(issuer, str) or not issuer.strip():
            raise ValueError("issuer must be a nonempty string")
        if not isinstance(jwks_url, str):
            raise TypeError("jwks_url must be a string")
        parts = urlsplit(jwks_url)
        if (
            parts.scheme != "https" or not parts.hostname
            or parts.username is not None or parts.password is not None
            or parts.fragment
            or any(ord(char) <= 32 or ord(char) == 127 for char in jwks_url)
        ):
            raise ValueError("jwks_url must be a configured HTTPS URL")
        for name, value in (
            ("cache_ttl_seconds", cache_ttl_seconds),
            ("min_refresh_interval_seconds", min_refresh_interval_seconds),
            ("timeout_seconds", timeout_seconds),
        ):
            if (
                isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or value <= 0
            ):
                raise ValueError(f"{name} must be finite and positive")
        if min_refresh_interval_seconds > cache_ttl_seconds:
            raise ValueError("refresh interval must not exceed cache TTL")
        for name, value in (
            ("max_response_bytes", max_response_bytes), ("max_keys", max_keys),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer")

        self._issuer = issuer
        self._host = parts.hostname
        self._port = parts.port
        self._target = parts.path or "/"
        if parts.query:
            self._target += "?" + parts.query
        self._tls = ssl.create_default_context(cafile=ca_file)
        self._ttl = cache_ttl_seconds
        self._interval = min_refresh_interval_seconds
        self._timeout = timeout_seconds
        self._limit = max_response_bytes
        self._max_keys = max_keys
        self._keys = {}
        self._loaded_at = None
        self._attempted_at = float("-inf")
        self._lock = threading.Lock()

    def _fetch(self) -> bytes:
        connection = http.client.HTTPSConnection(
            self._host, port=self._port, timeout=self._timeout, context=self._tls
        )
        try:
            connection.request("GET", self._target, headers={
                "Accept": "application/json", "Accept-Encoding": "identity",
            })
            response = connection.getresponse()
            if response.status != 200:
                raise RuntimeError("JWKS endpoint did not return 200")
            media_type = response.getheader("Content-Type", "")
            if media_type.split(";", 1)[0].strip().lower() != "application/json":
                raise ValueError("invalid JWKS content type")
            if response.getheader("Content-Encoding", "identity") != "identity":
                raise ValueError("unsupported JWKS content encoding")
            body = response.read(self._limit + 1)
            if len(body) > self._limit:
                raise ValueError("JWKS response size limit exceeded")
            return body
        finally:
            connection.close()

    def _parse(self, body: bytes):
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate JWKS JSON field")
                result[key] = value
            return result

        def invalid_constant(value):
            raise ValueError("invalid JSON constant")

        document = json.loads(
            body.decode("utf-8"), object_pairs_hook=unique,
            parse_constant=invalid_constant,
        )
        if not isinstance(document, dict) or not isinstance(document.get("keys"), list):
            raise ValueError("JWKS must contain a keys array")
        if len(document["keys"]) > self._max_keys:
            raise ValueError("JWKS key count limit exceeded")
        keys = {}
        identifiers = set()
        for entry in document["keys"]:
            if not isinstance(entry, dict):
                raise ValueError("invalid JWK entry")
            kid = entry.get("kid")
            if not isinstance(kid, str) or not kid.strip():
                raise ValueError("JWK must have a nonempty kid")
            if kid in identifiers:
                raise ValueError("duplicate JWK kid")
            identifiers.add(kid)
            if any(name in entry for name in ("d", "p", "q", "dp", "dq", "qi", "oth", "k")):
                raise ValueError("JWKS must contain public keys only")
            if entry.get("kty") != "RSA":
                continue
            if entry.get("alg", "RS256") != "RS256":
                continue
            if entry.get("use", "sig") != "sig":
                continue
            if "key_ops" in entry and entry["key_ops"] != ["verify"]:
                continue
            key = jwt.PyJWK.from_dict(entry, algorithm="RS256").key
            if not isinstance(key, RSAPublicKey) or key.key_size < 2048:
                raise ValueError("invalid RS256 public key")
            keys[kid] = key
        return keys

    def resolve(self, *, issuer: str, key_id: str, algorithm: str):
        if issuer != self._issuer or algorithm != "RS256":
            return None
        if not isinstance(key_id, str) or not key_id.strip():
            return None
        with self._lock:
            now = time.monotonic()
            fresh = self._loaded_at is not None and now - self._loaded_at < self._ttl
            if fresh and key_id in self._keys:
                return self._keys[key_id]
            if now - self._attempted_at < self._interval:
                if fresh:
                    return None
                raise RuntimeError("JWKS cache unavailable; refresh is rate limited")
            self._attempted_at = now
            # Replace the entire snapshot only after successful retrieval and parsing.
            keys = self._parse(self._fetch())
            self._keys = keys
            self._loaded_at = time.monotonic()
            return keys.get(key_id)
