from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ENCODING,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity_derivation import (
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity,
)


def sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
    *,
    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
    key_id: str,
    private_key: ec.EllipticCurvePrivateKey,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature:
    """Sign exact checkpoint payload bytes with one injected P-256 key."""

    if not isinstance(
        checkpoint,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
    ):
        raise TypeError(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        )

    if not isinstance(
        private_key,
        ec.EllipticCurvePrivateKey,
    ):
        raise TypeError(
            "private_key must be an EllipticCurvePrivateKey"
        )

    if not isinstance(
        private_key.curve,
        ec.SECP256R1,
    ):
        raise ValueError(
            "private_key curve must be SECP256R1"
        )

    signing_key_identity = (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
            key_id=key_id,
            public_key=private_key.public_key(),
        )
    )

    payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )

    signature = private_key.sign(
        payload,
        ec.ECDSA(hashes.SHA256()),
    )

    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=checkpoint,
            signing_key_identity=signing_key_identity,
            signature_encoding=(
                SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ENCODING
            ),
            signature=signature,
        )
    )
