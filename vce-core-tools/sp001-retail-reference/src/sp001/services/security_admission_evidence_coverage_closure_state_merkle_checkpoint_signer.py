from typing import Protocol, runtime_checkable

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)


@runtime_checkable
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigner(
    Protocol
):
    """Port for signing canonical checkpoint payload bytes."""

    @property
    def signing_key_identity(
        self,
    ) -> (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
    ):
        ...

    def sign(
        self,
        *,
        payload: bytes,
    ) -> bytes:
        ...
