from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    load_der_public_key,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity_derivation import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes,
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding:
    """Bind one signing-key identity to its canonical public key."""

    signing_key_identity: (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
    )
    public_key_bytes: bytes

    def __post_init__(self) -> None:
        if not isinstance(
            self.signing_key_identity,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
        ):
            raise TypeError(
                "signing_key_identity must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity"
            )
        if type(self.public_key_bytes) is not bytes:
            raise TypeError(
                "public_key_bytes must be bytes"
            )
        if not self.public_key_bytes:
            raise ValueError(
                "public_key_bytes must not be empty"
            )

        try:
            public_key = load_der_public_key(
                self.public_key_bytes
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                "public_key_bytes must contain a DER-SPKI public key"
            ) from error

        if not isinstance(
            public_key,
            ec.EllipticCurvePublicKey,
        ):
            raise ValueError(
                "public_key_bytes must contain an "
                "elliptic-curve public key"
            )
        if not isinstance(
            public_key.curve,
            ec.SECP256R1,
        ):
            raise ValueError(
                "public_key_bytes must contain a "
                "SECP256R1 public key"
            )

        canonical_bytes = (
            canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
                public_key=public_key,
            )
        )
        if self.public_key_bytes != canonical_bytes:
            raise ValueError(
                "public_key_bytes must use canonical "
                "DER-SPKI encoding"
            )

        derived_identity = (
            derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
                key_id=self.signing_key_identity.key_id,
                public_key=public_key,
            )
        )
        if self.signing_key_identity != derived_identity:
            raise ValueError(
                "signing_key_identity must match "
                "public_key_bytes"
            )
