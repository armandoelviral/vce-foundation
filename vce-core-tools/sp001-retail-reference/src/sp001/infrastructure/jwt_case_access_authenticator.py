from sp001.contracts.access_token_key_resolver import AccessTokenKeyResolver
from sp001.infrastructure.configured_access_token_keys import ConfiguredAccessTokenKeys
from collections.abc import Mapping

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)


class AccessTokenKeyResolutionError(RuntimeError):
    """Trusted key provider failure, distinct from invalid credentials."""


class JwtCaseAccessAuthenticator:
    """Verify the configured RS256 case-access profile without network calls."""

    def __init__(
        self,
        *,
        issuer: str,
        audience: str,
        public_keys: Mapping[str, RSAPublicKey] | None = None,
        key_resolver: AccessTokenKeyResolver | None = None,
        max_lifetime_seconds: int,
        max_token_bytes: int,
    ) -> None:
        for name, value in (("issuer", issuer), ("audience", audience)):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if not value.strip():
                raise ValueError(f"{name} must not be empty")
        for name, value in (
            ("max_lifetime_seconds", max_lifetime_seconds),
            ("max_token_bytes", max_token_bytes),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if (public_keys is None) == (key_resolver is None):
            raise ValueError("configure exactly one key source")
        if key_resolver is None:
            key_resolver = ConfiguredAccessTokenKeys(
                issuer=issuer, public_keys=public_keys
            )
        if not isinstance(key_resolver, AccessTokenKeyResolver):
            raise TypeError("key_resolver must implement AccessTokenKeyResolver")

        self._issuer = issuer
        self._audience = audience
        self._key_resolver = key_resolver
        self._max_lifetime = max_lifetime_seconds
        self._max_bytes = max_token_bytes

    def authenticate(
        self, *, credential: str
    ) -> ValidatedCaseAccessContext | None:
        if not isinstance(credential, str):
            raise TypeError("credential must be a string")
        try:
            if not credential or len(credential.encode("ascii")) > self._max_bytes:
                return None
            header = jwt.get_unverified_header(credential)
            # Header is untrusted and used only to select a configured key.
            if set(header) != {"alg", "kid", "typ"}:
                return None
            if header["alg"] != "RS256" or header["typ"] != "at+jwt":
                return None
            kid = header["kid"]
            if not isinstance(kid, str) or not kid.strip():
                return None
            try:
                key = self._key_resolver.resolve(
                    issuer=self._issuer, key_id=kid, algorithm="RS256"
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
                credential,
                key=key,
                algorithms=["RS256"],
                issuer=self._issuer,
                audience=self._audience,
                leeway=0,
                options={
                    "require": [
                        "iss", "sub", "aud", "iat", "nbf", "exp",
                        "case_permissions",
                    ],
                    "strict_aud": True,
                },
            )
            if claims["iss"] != self._issuer or claims["aud"] != self._audience:
                return None
            for name in ("iat", "nbf", "exp"):
                if isinstance(claims[name], bool) or not isinstance(claims[name], int):
                    return None
            if claims["exp"] - claims["iat"] > self._max_lifetime:
                return None

            raw_permissions = claims["case_permissions"]
            if not isinstance(raw_permissions, list):
                return None
            permissions = []
            for value in raw_permissions:
                if not isinstance(value, dict) or set(value) != {
                    "case_id", "operation",
                }:
                    return None
                if not isinstance(value["operation"], str):
                    return None
                permissions.append(CaseAccessPermission(
                    case_id=value["case_id"],
                    operation=CaseAccessOperation(value["operation"]),
                ))
            return ValidatedCaseAccessContext(
                principal=AuthenticatedPrincipal(
                    issuer=claims["iss"], subject=claims["sub"],
                ),
                audience=claims["aud"],
                issued_at=claims["iat"],
                not_before=claims["nbf"],
                expires_at=claims["exp"],
                permissions=tuple(permissions),
            )
        except (jwt.InvalidTokenError, UnicodeError, ValueError, TypeError):
            return None
