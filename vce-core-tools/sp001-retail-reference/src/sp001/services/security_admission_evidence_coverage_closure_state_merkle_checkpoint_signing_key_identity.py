from dataclasses import dataclass
import re


SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ALGORITHM = (
    "ECDSA-P256-SHA256"
)
SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_ENCODING = (
    "DER-SPKI"
)
SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_FINGERPRINT_ALGORITHM = (
    "SHA-256"
)

_FINGERPRINT_PATTERN = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity:
    """Identify one public signing key without containing private material."""

    key_id: str
    algorithm: str
    public_key_encoding: str
    public_key_fingerprint: str

    def __post_init__(self) -> None:
        if not isinstance(self.key_id, str):
            raise TypeError("key_id must be a str")
        if not self.key_id:
            raise ValueError("key_id must not be empty")
        if self.key_id != self.key_id.strip():
            raise ValueError(
                "key_id must not contain surrounding whitespace"
            )

        if not isinstance(self.algorithm, str):
            raise TypeError("algorithm must be a str")
        if (
            self.algorithm
            != SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ALGORITHM
        ):
            raise ValueError(
                "algorithm must be ECDSA-P256-SHA256"
            )

        if not isinstance(self.public_key_encoding, str):
            raise TypeError(
                "public_key_encoding must be a str"
            )
        if (
            self.public_key_encoding
            != SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_ENCODING
        ):
            raise ValueError(
                "public_key_encoding must be DER-SPKI"
            )

        if not isinstance(
            self.public_key_fingerprint,
            str,
        ):
            raise TypeError(
                "public_key_fingerprint must be a str"
            )
        if (
            _FINGERPRINT_PATTERN.fullmatch(
                self.public_key_fingerprint
            )
            is None
        ):
            raise ValueError(
                "public_key_fingerprint must contain "
                "64 lowercase hexadecimal characters"
            )
