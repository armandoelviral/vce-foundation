from dataclasses import dataclass

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_root import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
)


SECURITY_ADMISSION_MERKLE_CHECKPOINT_DOMAIN = (
    "SP001-SECURITY-ADMISSION-CLOSURE-STATE-MERKLE-CHECKPOINT"
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint:
    """Bind one named transparency-log origin to one Merkle tree state."""

    origin: str
    root: SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot

    def __post_init__(self) -> None:
        if not isinstance(self.origin, str):
            raise TypeError("origin must be a str")
        if not self.origin:
            raise ValueError("origin must not be empty")
        if self.origin != self.origin.strip():
            raise ValueError(
                "origin must not contain surrounding whitespace"
            )
        if not isinstance(
            self.root,
            SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot,
        ):
            raise TypeError(
                "root must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateMerkleRoot"
            )
