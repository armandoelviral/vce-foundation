from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)


SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ENCODING = (
    "ASN.1-DER"
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature:
    """Bind one checkpoint to one public-key identity and ECDSA signature."""

    checkpoint: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint
    signing_key_identity: SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
    signature_encoding: str
    signature: bytes

    def __post_init__(self) -> None:
        if not isinstance(
            self.checkpoint,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint,
        ):
            raise TypeError(
                "checkpoint must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
            )

        if not isinstance(
            self.signing_key_identity,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
        ):
            raise TypeError(
                "signing_key_identity must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity"
            )

        if not isinstance(self.signature_encoding, str):
            raise TypeError(
                "signature_encoding must be a str"
            )
        if (
            self.signature_encoding
            != SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ENCODING
        ):
            raise ValueError(
                "signature_encoding must be ASN.1-DER"
            )

        if type(self.signature) is not bytes:
            raise TypeError("signature must be bytes")
        if not self.signature:
            raise ValueError("signature must not be empty")

        try:
            r_value, s_value = decode_dss_signature(
                self.signature
            )
        except ValueError as error:
            raise ValueError(
                "signature must be a valid ASN.1-DER "
                "ECDSA signature"
            ) from error

        if (
            r_value <= 0
            or s_value <= 0
            or encode_dss_signature(
                r_value,
                s_value,
            )
            != self.signature
        ):
            raise ValueError(
                "signature must be a canonical ASN.1-DER "
                "ECDSA signature"
            )
