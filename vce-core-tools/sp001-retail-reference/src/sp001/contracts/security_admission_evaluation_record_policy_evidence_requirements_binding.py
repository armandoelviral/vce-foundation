from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionPolicyEvidenceRequirements,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding:
    """Bind one recorded evaluation to its exact policy requirements."""

    evaluation_record: SecurityAdmissionEvaluationRecord
    policy_evidence_requirements: SecurityAdmissionPolicyEvidenceRequirements

    def __post_init__(self) -> None:
        if not isinstance(
            self.evaluation_record,
            SecurityAdmissionEvaluationRecord,
        ):
            raise TypeError(
                "evaluation_record must be a "
                "SecurityAdmissionEvaluationRecord"
            )
        if not isinstance(
            self.policy_evidence_requirements,
            SecurityAdmissionPolicyEvidenceRequirements,
        ):
            raise TypeError(
                "policy_evidence_requirements must be a "
                "SecurityAdmissionPolicyEvidenceRequirements"
            )

        record_policy_identity = (
            self.evaluation_record
            .evaluation_identity
            .evaluation_basis
            .admission_policy_identity
        )
        if (
            record_policy_identity
            != self.policy_evidence_requirements.admission_policy_identity
        ):
            raise ValueError(
                "policy evidence requirements must use "
                "evaluation record policy identity"
            )
