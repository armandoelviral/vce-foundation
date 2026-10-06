from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_binding_verification import (
    verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signer import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
)


def sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint_with_external_signer(
    *,
    checkpoint: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint
    ),
    signer: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner
    ),
    public_key_binding: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding
    ),
) -> (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature
):
    """Sign and verify one checkpoint through an injected signer port."""

    if not isinstance(
        checkpoint,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
    ):
        raise TypeError(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        )
    if not isinstance(
        signer,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner,
    ):
        raise TypeError(
            "signer must implement "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner"
        )
    if not isinstance(
        public_key_binding,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
    ):
        raise TypeError(
            "public_key_binding must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding"
        )

    signing_key_identity = signer.signing_key_identity
    if not isinstance(
        signing_key_identity,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
    ):
        raise TypeError(
            "signer.signing_key_identity must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity"
        )
    if (
        signing_key_identity
        != public_key_binding.signing_key_identity
    ):
        raise ValueError(
            "signer identity must match public_key_binding"
        )

    payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )
    signature_bytes = signer.sign(
        payload=payload,
    )
    if type(signature_bytes) is not bytes:
        raise TypeError(
            "signer.sign must return bytes"
        )
    if not signature_bytes:
        raise ValueError(
            "signer.sign must return a non-empty signature"
        )

    checkpoint_signature = (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature(
            checkpoint=checkpoint,
            signing_key_identity=signing_key_identity,
            signature_encoding="ASN.1-DER",
            signature=signature_bytes,
        )
    )

    if not (
        verify_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature_with_public_key_binding(
            checkpoint_signature=checkpoint_signature,
            public_key_binding=public_key_binding,
        )
    ):
        raise ValueError(
            "external signer returned an invalid checkpoint signature"
        )

    return checkpoint_signature
