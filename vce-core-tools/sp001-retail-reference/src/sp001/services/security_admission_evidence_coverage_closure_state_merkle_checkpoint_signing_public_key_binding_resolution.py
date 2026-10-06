from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding_set import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
)


def resolve_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding(
    *,
    binding_set: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet
    ),
    signing_key_identity: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
    ),
) -> (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding
    | None
):
    """Resolve an exact signing-key identity from one binding set."""

    if not isinstance(
        binding_set,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet,
    ):
        raise TypeError(
            "binding_set must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBindingSet"
        )
    if not isinstance(
        signing_key_identity,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
    ):
        raise TypeError(
            "signing_key_identity must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity"
        )

    for binding in binding_set.bindings:
        if (
            binding.signing_key_identity
            == signing_key_identity
        ):
            return binding

    return None
