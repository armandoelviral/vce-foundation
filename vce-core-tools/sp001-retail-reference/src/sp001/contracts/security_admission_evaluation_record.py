from dataclasses import dataclass
from datetime import datetime

from sp001.contracts.security_admission_evaluation_identity import (
    SecurityAdmissionEvaluationIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecord:
    """Recorded occurrence of one identified admission evaluation."""

    evaluation_identity: SecurityAdmissionEvaluationIdentity
    evaluated_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(
            self.evaluation_identity,
            SecurityAdmissionEvaluationIdentity,
        ):
            raise TypeError(
                "evaluation_identity must be a "
                "SecurityAdmissionEvaluationIdentity"
            )
        if not isinstance(self.evaluated_at, datetime):
            raise TypeError("evaluated_at must be a datetime")
        if (
            self.evaluated_at.tzinfo is None
            or self.evaluated_at.utcoffset() is None
        ):
            raise ValueError(
                "evaluated_at must be timezone-aware"
            )
