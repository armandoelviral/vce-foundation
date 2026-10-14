import base64
import json
import re

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from sp001.contracts.access_token_key_resolver import AccessTokenKeyResolver
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)
from sp001.infrastructure.jwt_case_access_authenticator import (
    AccessTokenKeyResolutionError,
)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


def _document(segment):
    raw = base64.b64decode(
        segment + "=" * (-len(segment) % 4), altchars=b"-_", validate=True,
    )
    result = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    if not isinstance(result, dict):
        raise ValueError("JWT document must be an object")
    return result


class JwtFederatedIssuanceAuthenticator:
    """Verify a configured RS256 primary access-token profile."""

    def __init__(
        self, *, issuer: str, audience: str,
        key_resolver: AccessTokenKeyResolver,
        max_lifetime_seconds: int, max_token_bytes: int,
    ):
        for name, value in (("issuer", issuer), ("audience", audience)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")
        for name, value in (
            ("max_lifetime_seconds", max_lifetime_seconds),
            ("max_token_bytes", max_token_bytes),
        ):
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if not isinstance(key_resolver, AccessTokenKeyResolver):
            raise TypeError("key_resolver must implement AccessTokenKeyResolver")
        self._issuer = issuer
        self._audience = audience
        self._resolver = key_resolver
        self._max_lifetime = max_lifetime_seconds
        self._max_bytes = max_token_bytes

    def authenticate(self, *, credential):
        if not isinstance(credential, str):
            raise TypeError("credential must be a string")
        try:
            if not credential or len(credential.encode("ascii")) > self._max_bytes:
                return None
            segments = credential.split(".")
            if len(segments) != 3 or any(
                re.fullmatch(r"[A-Za-z0-9_-]+", part) is None
                for part in segments
            ):
                return None
            header = _document(segments[0])
            # Parse untrusted claims only to reject ambiguous JSON structure.
            _document(segments[1])
            if set(header) != {"alg", "kid", "typ"}:
                return None
            if header["alg"] != "RS256" or header["typ"] != "at+jwt":
                return None
            kid = header["kid"]
            if not isinstance(kid, str) or not kid.strip():
                return None

            try:
                key = self._resolver.resolve(
                    issuer=self._issuer, key_id=kid, algorithm="RS256",
                )
            except Exception as error:
                raise AccessTokenKeyResolutionError(
                    "trusted key resolution failed"
                ) from error
            if key is None:
                return None
            if not isinstance(key, RSAPublicKey) or key.key_size < 2048:
                raise RuntimeError("key resolver returned an invalid RS256 key")

            claims = jwt.decode(
                credential, key=key, algorithms=["RS256"],
                issuer=self._issuer, audience=self._audience, leeway=0,
                options={
                    "require": ["iss", "sub", "aud", "iat", "nbf", "exp"],
                    "strict_aud": True,
                },
            )
            if claims["iss"] != self._issuer or claims["aud"] != self._audience:
                return None
            if any(type(claims[name]) is not int for name in ("iat", "nbf", "exp")):
                return None
            if claims["exp"] - claims["iat"] > self._max_lifetime:
                return None
            return ValidatedFederatedIssuanceContext(
                principal=AuthenticatedPrincipal(claims["iss"], claims["sub"]),
                audience=claims["aud"],
                issued_at=claims["iat"], not_before=claims["nbf"],
                expires_at=claims["exp"],
            )
        except (jwt.InvalidTokenError, UnicodeError, ValueError, TypeError):
            return None
