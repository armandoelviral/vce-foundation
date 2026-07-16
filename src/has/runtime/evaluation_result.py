from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Explainable result of evaluating a knowledge artifact."""

    eligible: bool
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.eligible and self.reasons:
            raise ValueError(
                "eligible evaluation cannot contain rejection reasons"
            )
