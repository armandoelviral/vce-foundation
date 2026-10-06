from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_binding_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_resolution import (
    resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
)


def verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding_set(
    *,
    checkpoint_signature: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
    ),
    binding_set: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet
    ),
) -> bool:
    """Resolve and verify one checkpoint signature from a binding set."""

    if not isinstance(
        checkpoint_signature,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
    ):
        raise TypeError(
            "checkpoint_signature must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature"
        )
    if not isinstance(
        binding_set,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
    ):
        raise TypeError(
            "binding_set must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet"
        )

    binding = (
        resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
            binding_set=binding_set,
            signing_key_identity=(
                checkpoint_signature
                .signing_key_identity
            ),
        )
    )
    if binding is None:
        return False

    return verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
        checkpoint_signature=checkpoint_signature,
        public_key_binding=binding,
    )
