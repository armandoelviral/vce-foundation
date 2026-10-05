import hashlib

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_ENCODING,
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ALGORITHM,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)


def canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
    *,
    public_key: ec.EllipticCurvePublicKey,
) -> bytes:
    """Return canonical DER-SPKI bytes for one P-256 public key."""

    _validate_p256_public_key(public_key)

    return public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
    *,
    key_id: str,
    public_key: ec.EllipticCurvePublicKey,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity:
    """Derive the nominal identity bound to one exact P-256 public key."""

    public_key_bytes = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
            public_key=public_key,
        )
    )

    fingerprint = hashlib.sha256(
        public_key_bytes
    ).hexdigest()

    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id=key_id,
            algorithm=(
                SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ALGORITHM
            ),
            public_key_encoding=(
                SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_ENCODING
            ),
            public_key_fingerprint=fingerprint,
        )
    )


def _validate_p256_public_key(
    public_key: object,
) -> None:
    if not isinstance(
        public_key,
        ec.EllipticCurvePublicKey,
    ):
        raise TypeError(
            "public_key must be an EllipticCurvePublicKey"
        )

    if not isinstance(
        public_key.curve,
        ec.SECP256R1,
    ):
        raise ValueError(
            "public_key curve must be SECP256R1"
        )
