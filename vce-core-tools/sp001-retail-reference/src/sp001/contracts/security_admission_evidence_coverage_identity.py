from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_record_policy_evidence_requirements_binding import (
    SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageIdentity:
    """Exact versioned identity of one admission evidence coverage attempt."""

    coverage_id: str
    coverage_version: int
    evaluation_record_policy_evidence_requirements_binding: (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(self.coverage_id, str):
            raise TypeError("coverage_id must be a string")
        if not self.coverage_id.strip():
            raise ValueError("coverage_id must not be blank")
        if (
            isinstance(self.coverage_version, bool)
            or not isinstance(self.coverage_version, int)
        ):
            raise TypeError("coverage_version must be an integer")
        if self.coverage_version <= 0:
            raise ValueError("coverage_version must be positive")
        if not isinstance(
            self.evaluation_record_policy_evidence_requirements_binding,
            SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
        ):
            raise TypeError(
                "evaluation_record_policy_evidence_requirements_binding "
                "must be a "
                "SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding"
            )
