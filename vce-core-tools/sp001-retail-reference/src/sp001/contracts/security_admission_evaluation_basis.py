from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationBasis:
    """Exact candidate and policy selected for one admission evaluation."""

    candidate_identity: SecurityAdmissionCandidateIdentity
    admission_policy_identity: SecurityAdmissionPolicyIdentity

    def __post_init__(self) -> None:
        if not isinstance(
            self.candidate_identity,
            SecurityAdmissionCandidateIdentity,
        ):
            raise TypeError(
                "candidate_identity must be a "
                "SecurityAdmissionCandidateIdentity"
            )
        if not isinstance(
            self.admission_policy_identity,
            SecurityAdmissionPolicyIdentity,
        ):
            raise TypeError(
                "admission_policy_identity must be a "
                "SecurityAdmissionPolicyIdentity"
            )
