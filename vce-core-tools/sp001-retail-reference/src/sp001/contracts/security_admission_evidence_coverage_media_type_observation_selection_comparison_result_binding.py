from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_record_media_type_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding:
    """Bind one governed recorded media-type result to evidence coverage."""

    evaluation_record_media_type_observation_selection_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionComparisonResultBinding
    )
    evidence_coverage_media_type_comparison_result_binding: (
        SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.evaluation_record_media_type_observation_selection_comparison_result_binding,
            SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_media_type_observation_selection_"
                "comparison_result_binding must be a "
                "SecurityAdmissionEvaluationRecordMediaType"
                "ObservationSelectionComparisonResultBinding"
            )
        if not isinstance(
            self.evidence_coverage_media_type_comparison_result_binding,
            SecurityAdmissionEvidenceCoverageMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "evidence_coverage_media_type_comparison_result_binding "
                "must be a "
                "SecurityAdmissionEvidenceCoverageMediaType"
                "ComparisonResultBinding"
            )
        if (
            self.evaluation_record_media_type_observation_selection_comparison_result_binding
            .evaluation_record_media_type_comparison_result_binding
            != self.evidence_coverage_media_type_comparison_result_binding
            .evaluation_record_media_type_comparison_result_binding
        ):
            raise ValueError(
                "media-type evidence coverage must use the governed "
                "recorded comparison result binding"
            )
