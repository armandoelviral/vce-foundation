from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_record_media_type_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding:
    """Bind conclusive recorded media-type evidence to one coverage identity."""

    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity
    evaluation_record_media_type_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.coverage_identity,
            SecurityAdmissionEvidenceCoverageIdentity,
        ):
            raise TypeError(
                "coverage_identity must be a "
                "SecurityAdmissionEvidenceCoverageIdentity"
            )
        if not isinstance(
            self.evaluation_record_media_type_comparison_result_binding,
            SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_media_type_comparison_result_binding must be a "
                "SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding"
            )

        coverage_record = (
            self.coverage_identity
            .evaluation_record_policy_evidence_requirements_binding
            .evaluation_record
        )
        if (
            coverage_record
            != self.evaluation_record_media_type_comparison_result_binding
            .evaluation_record
        ):
            raise ValueError(
                "media-type result binding must use coverage evaluation record"
            )
