from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    load_der_public_key,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
)


def verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
    *,
    checkpoint_signature: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
    ),
    public_key_binding: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding
    ),
) -> bool:
    """Verify one checkpoint signature with a canonical key binding."""

    if not isinstance(
        checkpoint_signature,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
    ):
        raise TypeError(
            "checkpoint_signature must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature"
        )
    if not isinstance(
        public_key_binding,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
    ):
        raise TypeError(
            "public_key_binding must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding"
        )

    public_key = load_der_public_key(
        public_key_binding.public_key_bytes
    )
    if not isinstance(
        public_key,
        ec.EllipticCurvePublicKey,
    ):
        return False
    if not isinstance(
        public_key.curve,
        ec.SECP256R1,
    ):
        return False

    return verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature(
        checkpoint_signature=checkpoint_signature,
        expected_key_id=(
            public_key_binding
            .signing_key_identity
            .key_id
        ),
        public_key=public_key,
    )
