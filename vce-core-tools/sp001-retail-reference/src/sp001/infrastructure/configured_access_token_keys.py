from collections.abc import Mapping
from types import MappingProxyType

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


class ConfiguredAccessTokenKeys:
    """Local RS256 key snapshot bound to one explicitly trusted issuer."""

    def __init__(
        self, *, issuer: str, public_keys: Mapping[str, RSAPublicKey]
    ) -> None:
        if not isinstance(issuer, str) or not issuer.strip():
            raise ValueError("issuer must be a nonempty string")
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
        self._keys = MappingProxyType(keys)

    def resolve(self, *, issuer: str, key_id: str, algorithm: str):
        if issuer != self._issuer or algorithm != "RS256":
            return None
        return self._keys.get(key_id)
