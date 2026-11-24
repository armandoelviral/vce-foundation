"""D5.4A: signed context only; not an execution admission."""
from dataclasses import dataclass
import hashlib
import json
import re
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from sp001.contracts.product001_documentary_commitment import Product001DocumentaryCommitmentKey

DOMAIN = "SP001/PRODUCT001/MVP1/CONTEXTUAL_AUTHORIZATION/V1"
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z", re.ASCII)
_DIGEST = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)


def documentary_binding_from_key(key: Product001DocumentaryCommitmentKey) -> tuple[str, str, str, str, str]:
    """Bind the existing documentary identity AND its content digest."""
    if not isinstance(key, Product001DocumentaryCommitmentKey):
        raise TypeError("documentary commitment key required")
    source = key.source_identity
    digest = source.source_content_digest
    if digest.algorithm != "SHA-256" or _DIGEST.fullmatch(digest.value) is None:
        raise ValueError("unsupported documentary digest")
    return (key.organization_id, source.source_id, source.source_version,
            digest.algorithm, digest.value)


@dataclass(frozen=True, slots=True)
class ContextualAuthorizationV1:
    operation_id: str
    decision_digest: str
    issuer_id: str
    authority_sequence: int
    materialize_deadline: int
    documentary_binding: tuple[str, str, str, str, str]
    signature: bytes

    def __post_init__(self) -> None:
        for name in ("operation_id", "issuer_id"):
            value = getattr(self, name)
            if type(value) is not str or _ID.fullmatch(value) is None:
                raise ValueError(f"invalid {name}")
        if type(self.decision_digest) is not str or _DIGEST.fullmatch(self.decision_digest) is None:
            raise ValueError("invalid decision digest")
        if type(self.authority_sequence) is not int or self.authority_sequence < 0:
            raise ValueError("invalid authority sequence")
        if type(self.materialize_deadline) is not int or self.materialize_deadline < 0:
            raise ValueError("invalid materialize deadline")
        binding = self.documentary_binding
        if type(binding) is not tuple or len(binding) != 5:
            raise ValueError("invalid documentary binding")
        if any(type(value) is not str or not value for value in binding):
            raise ValueError("invalid documentary binding value")
        if binding[3] != "SHA-256" or _DIGEST.fullmatch(binding[4]) is None:
            raise ValueError("invalid documentary digest")
        if type(self.signature) is not bytes or len(self.signature) != 64:
            raise ValueError("invalid signature")


def authorization_signing_payload(cert: ContextualAuthorizationV1) -> bytes:
    if type(cert) is not ContextualAuthorizationV1:
        raise TypeError("invalid certificate")
    body = {"domain": DOMAIN, "operation_id": cert.operation_id,
            "decision_digest": cert.decision_digest, "issuer_id": cert.issuer_id,
            "authority_sequence": cert.authority_sequence,
            "materialize_deadline": cert.materialize_deadline,
            "documentary_binding": list(cert.documentary_binding)}
    return json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def decision_digest_from_canonical_bytes(value: bytes) -> str:
    """Hashes caller-supplied bytes; canonicality/provenance are not established here."""
    if type(value) is not bytes or not value:
        raise ValueError("nonempty decision bytes required")
    return hashlib.sha256(value).hexdigest()


def verify_contextual_authorization_signature(
    cert: ContextualAuthorizationV1, *, trusted_issuer_id: str,
    trusted_public_key: Ed25519PublicKey, expected_operation_id: str,
    expected_decision_digest: str,
    expected_documentary_key: Product001DocumentaryCommitmentKey,
) -> None:
    """Signature and exact context only; never checks admission or consumption."""
    if type(cert) is not ContextualAuthorizationV1:
        raise TypeError("invalid certificate")
    if not isinstance(trusted_public_key, Ed25519PublicKey):
        raise TypeError("trusted public key required")
    expected_binding = documentary_binding_from_key(expected_documentary_key)
    if (cert.issuer_id != trusted_issuer_id or
        cert.operation_id != expected_operation_id or
        cert.decision_digest != expected_decision_digest or
        cert.documentary_binding != expected_binding):
        raise PermissionError("authorization context mismatch")
    try:
        trusted_public_key.verify(cert.signature, authorization_signing_payload(cert))
    except (InvalidSignature, ValueError) as exc:
        raise PermissionError("invalid authorization signature") from exc
