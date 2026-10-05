from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity,
)


def verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
    *,
    checkpoint_signature: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
    ),
    expected_key_id: str,
    public_key: ec.EllipticCurvePublicKey,
) -> bool:
    """Verify a checkpoint signature against an expected signing key."""

    if not isinstance(
        checkpoint_signature,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
    ):
        raise TypeError(
            "checkpoint_signature must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature"
        )
    if not isinstance(expected_key_id, str):
        raise TypeError("expected_key_id must be a string")
    if not expected_key_id:
        raise ValueError("expected_key_id must not be empty")
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise TypeError(
            "public_key must be an EllipticCurvePublicKey"
        )
    if not isinstance(public_key.curve, ec.SECP256R1):
        raise ValueError(
            "public_key must use the SECP256R1 curve"
        )

    expected_identity = (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
            key_id=expected_key_id,
            public_key=public_key,
        )
    )
    if expected_identity != checkpoint_signature.signing_key_identity:
        return False

    payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint_signature.checkpoint,
        )
    )

    try:
        public_key.verify(
            checkpoint_signature.signature,
            payload,
            ec.ECDSA(hashes.SHA256()),
        )
    except (InvalidSignature, ValueError):
        return False

    return True
