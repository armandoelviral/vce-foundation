"""Unverified binding between an evaluation record and assertion content."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HostFactEvaluationContentBinding:
    """Declared content reference; grants no trust or authority."""

    evaluation_record_id: str
    assertion_id: str
    assertion_digest: bytes

    def __post_init__(self) -> None:
        for field in ("evaluation_record_id", "assertion_id"):
            value = getattr(self, field)
            if type(value) is not str or not value.strip():
                raise ValueError(f"{field} must be a nonempty string")

        if type(self.assertion_digest) is not bytes:
            raise TypeError("assertion_digest must be bytes")

        if len(self.assertion_digest) != 32:
            raise ValueError("assertion_digest must contain 32 bytes")
