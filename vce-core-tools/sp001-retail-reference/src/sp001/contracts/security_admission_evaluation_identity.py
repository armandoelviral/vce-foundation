from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationIdentity:
    """Exact versioned identity of one admission evaluation attempt."""

    evaluation_id: str
    evaluation_version: int
    evaluation_basis: SecurityAdmissionEvaluationBasis

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation_id, str):
            raise TypeError("evaluation_id must be a string")
        if not self.evaluation_id.strip():
            raise ValueError("evaluation_id must not be blank")
        if (
            isinstance(self.evaluation_version, bool)
            or not isinstance(self.evaluation_version, int)
        ):
            raise TypeError(
                "evaluation_version must be an integer"
            )
        if self.evaluation_version <= 0:
            raise ValueError(
                "evaluation_version must be positive"
            )
        if not isinstance(
            self.evaluation_basis,
            SecurityAdmissionEvaluationBasis,
        ):
            raise TypeError(
                "evaluation_basis must be a "
                "SecurityAdmissionEvaluationBasis"
            )
