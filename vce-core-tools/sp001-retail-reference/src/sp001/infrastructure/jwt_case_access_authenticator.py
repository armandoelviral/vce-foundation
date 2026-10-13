from collections.abc import Mapping
from types import MappingProxyType

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import (
    CaseAccessOperation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)


class JwtCaseAccessAuthenticator:
    """Verify the configured RS256 case-access profile without network calls."""

    def __init__(
        self,
        *,
        issuer: str,
        audience: str,
        public_keys: Mapping[str, RSAPublicKey],
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
        if not isinstance(public_keys, Mapping) or not public_keys:
            raise ValueError("public_keys must be a nonempty mapping")
        keys = dict(public_keys)
        for kid, key in keys.items():
            if not isinstance(kid, str) or not kid.strip():
                raise ValueError("key identifiers must be nonempty strings")
            if not isinstance(key, RSAPublicKey):
                raise TypeError("keys must be RSA public keys")
            if key.key_size < 2048:
                raise ValueError("RSA keys must be at least 2048 bits")

        self._issuer = issuer
        self._audience = audience
        self._keys = MappingProxyType(keys)
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
            if not isinstance(kid, str) or kid not in self._keys:
                return None

            claims = jwt.decode(
                credential,
                key=self._keys[kid],
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
