from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationRequirements:
    """Quantitative requirements for a knowledge-state transition."""

    minimum_evidence: int = 0
    minimum_independent_validations: int = 0
    minimum_destruction_attempts: int = 0

    def __post_init__(self) -> None:
        values = (
            self.minimum_evidence,
            self.minimum_independent_validations,
            self.minimum_destruction_attempts,
        )

        if any(value < 0 for value in values):
            raise ValueError(
                "evaluation requirements cannot be negative"
            )
