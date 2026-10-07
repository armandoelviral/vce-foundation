import re
from dataclasses import dataclass

from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


_SUPPORTED_STORAGE_SCHEMA_VERSION = 1
_FINGERPRINT_PATTERN = re.compile(
    r"[0-9a-f]{64}"
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredIntent:
    """Preserve one portable signed checkpoint-publication intent."""

    storage_schema_version: int
    publication_id: str
    checkpoint_serialization: str
    signing_key_id: str
    signing_algorithm: str
    public_key_encoding: str
    public_key_fingerprint: str
    signature_encoding: str
    signature: bytes

    def __post_init__(self) -> None:
        validate_security_admission_positive_uint64(
            value=self.storage_schema_version,
            field="storage_schema_version",
        )
        if (
            self.storage_schema_version
            != _SUPPORTED_STORAGE_SCHEMA_VERSION
        ):
            raise ValueError(
                "storage_schema_version is not supported"
            )

        for field, value in (
            (
                "publication_id",
                self.publication_id,
            ),
            (
                "checkpoint_serialization",
                self.checkpoint_serialization,
            ),
            (
                "signing_key_id",
                self.signing_key_id,
            ),
            (
                "signing_algorithm",
                self.signing_algorithm,
            ),
            (
                "public_key_encoding",
                self.public_key_encoding,
            ),
            (
                "signature_encoding",
                self.signature_encoding,
            ),
        ):
            self._validate_nonempty_text(
                value=value,
                field=field,
            )

        if type(self.public_key_fingerprint) is not str:
            raise TypeError(
                "public_key_fingerprint must be a string"
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

        if type(self.signature) is not bytes:
            raise TypeError(
                "signature must be bytes"
            )
        if not self.signature:
            raise ValueError(
                "signature must not be empty"
            )

    @staticmethod
    def _validate_nonempty_text(
        *,
        value: object,
        field: str,
    ) -> None:
        if type(value) is not str:
            raise TypeError(
                f"{field} must be a string"
            )
        if not value:
            raise ValueError(
                f"{field} must not be empty"
            )
