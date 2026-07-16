from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """Explainable result of verifying a runtime event."""

    valid: bool
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.valid and self.reasons:
            raise ValueError(
                "valid verification cannot contain rejection reasons"
            )
