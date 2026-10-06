from dataclasses import dataclass
import re

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_publication_phase import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_positive_uint64,
)


SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION = 1

_FINGERPRINT_PATTERN = re.compile(r"[0-9a-f]{64}")
_ALLOWED_PHASE_VALUES = frozenset(
    phase.value
    for phase in (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationPhase
    )
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointPublicationStoredState:
    """Portable primitive representation of one durable publication state."""

    storage_schema_version: int
    publication_id: str
    checkpoint_serialization: str
    signing_key_id: str
    signing_algorithm: str
    public_key_encoding: str
    public_key_fingerprint: str
    signature_encoding: str
    signature: bytes
    phase: str
    revision: int

    def __post_init__(self) -> None:
        validate_security_admission_positive_uint64(
            value=self.storage_schema_version,
            field="storage_schema_version",
        )
        if (
            self.storage_schema_version
            != SECURITY_ADMISSION_CHECKPOINT_PUBLICATION_STORAGE_SCHEMA_VERSION
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
            _validate_non_empty_string(
                value=value,
                field=field,
            )

        if (
            type(self.public_key_fingerprint) is not str
            or _FINGERPRINT_PATTERN.fullmatch(
                self.public_key_fingerprint
            )
            is None
        ):
            raise ValueError(
                "public_key_fingerprint must contain "
                "64 lowercase hexadecimal characters"
            )

        if type(self.signature) is not bytes:
            raise TypeError("signature must be bytes")
        if not self.signature:
            raise ValueError("signature must not be empty")

        if type(self.phase) is not str:
            raise TypeError("phase must be a string")
        if self.phase not in _ALLOWED_PHASE_VALUES:
            raise ValueError(
                "phase must be a supported publication phase"
            )

        validate_security_admission_positive_uint64(
            value=self.revision,
            field="revision",
        )


def _validate_non_empty_string(
    *,
    value: object,
    field: str,
) -> None:
    if type(value) is not str:
        raise TypeError(f"{field} must be a string")
    if not value:
        raise ValueError(f"{field} must not be empty")
