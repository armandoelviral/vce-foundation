from dataclasses import asdict, dataclass, field
import json
import os

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from sp001.contracts.case_access_issuance_preparation import (
    CaseAccessIssuancePreparation,
)
from sp001.contracts.case_access_token_issuance import IssuedCaseAccessToken


def _associated_data(preparation: CaseAccessIssuancePreparation) -> bytes:
    if not isinstance(preparation, CaseAccessIssuancePreparation):
        raise TypeError("preparation must be a CaseAccessIssuancePreparation")
    document = json.dumps(
        asdict(preparation), sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    )
    return b"sp001.prepared-credential.v1:" + document.encode("ascii")


@dataclass(frozen=True, slots=True)
class ProtectedCaseAccessCredential:
    protection_key_id: str
    nonce: bytes = field(repr=False)
    ciphertext: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.protection_key_id, str) or not self.protection_key_id.strip():
            raise ValueError("protection_key_id must be a nonempty string")
        if not isinstance(self.nonce, bytes) or len(self.nonce) != 12:
            raise ValueError("nonce must contain exactly 12 bytes")
        if not isinstance(self.ciphertext, bytes) or len(self.ciphertext) <= 16:
            raise ValueError("ciphertext must contain encrypted credential and tag")


class PreparedCaseAccessSigner:
    """Sign exact prepared claims; this capability does not authorize issuance."""

    def __init__(
        self, *, signing_key_id: str, private_key: RSAPrivateKey,
        issuer: str, audience: str,
    ) -> None:
        for name, value in (
            ("signing_key_id", signing_key_id), ("issuer", issuer), ("audience", audience),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")
        if not isinstance(private_key, RSAPrivateKey):
            raise TypeError("private_key must be an RSA private key")
        if private_key.key_size < 2048:
            raise ValueError("RSA private key must be at least 2048 bits")
        self._kid = signing_key_id
        self._key = private_key
        self._issuer = issuer
        self._audience = audience

    def sign(
        self, *, preparation: CaseAccessIssuancePreparation
    ) -> IssuedCaseAccessToken:
        if not isinstance(preparation, CaseAccessIssuancePreparation):
            raise TypeError("preparation must be a CaseAccessIssuancePreparation")
        if preparation.signing_key_id != self._kid:
            raise ValueError("prepared signing key does not match configured key")
        if (
            preparation.payload.issuer != self._issuer
            or preparation.payload.audience != self._audience
        ):
            raise ValueError("prepared issuer or audience does not match signer")
        credential = jwt.encode(
            preparation.payload.to_claims(), self._key, algorithm="RS256",
            headers={"kid": self._kid, "typ": "at+jwt"},
        )
        return IssuedCaseAccessToken(credential)


class PreparedCredentialProtector:
    """AES-256-GCM credential protection bound to the complete preparation."""

    def __init__(self, *, protection_key_id: str, key: bytes) -> None:
        if not isinstance(protection_key_id, str) or not protection_key_id.strip():
            raise ValueError("protection_key_id must be a nonempty string")
        if not isinstance(key, bytes) or len(key) != 32:
            raise ValueError("protection key must contain exactly 32 bytes")
        self._kid = protection_key_id
        self._cipher = AESGCM(key)

    def protect(
        self, *, preparation: CaseAccessIssuancePreparation,
        token: IssuedCaseAccessToken,
    ) -> ProtectedCaseAccessCredential:
        if not isinstance(token, IssuedCaseAccessToken):
            raise TypeError("token must be an IssuedCaseAccessToken")
        nonce = os.urandom(12)
        ciphertext = self._cipher.encrypt(
            nonce, token.credential.encode("utf-8"), _associated_data(preparation),
        )
        return ProtectedCaseAccessCredential(self._kid, nonce, ciphertext)

    def recover(
        self, *, preparation: CaseAccessIssuancePreparation,
        protected: ProtectedCaseAccessCredential,
    ) -> IssuedCaseAccessToken:
        if not isinstance(protected, ProtectedCaseAccessCredential):
            raise TypeError("protected must be a ProtectedCaseAccessCredential")
        if protected.protection_key_id != self._kid:
            raise ValueError("unknown protection key identifier")
        plaintext = self._cipher.decrypt(
            protected.nonce, protected.ciphertext, _associated_data(preparation),
        )
        return IssuedCaseAccessToken(plaintext.decode("utf-8"))
