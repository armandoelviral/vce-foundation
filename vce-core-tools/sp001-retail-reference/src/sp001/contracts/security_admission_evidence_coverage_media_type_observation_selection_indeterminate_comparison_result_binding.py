from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_record_media_type_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_indeterminate_media_type_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding:
    """Bind one governed recorded indeterminate media-type result to coverage."""

    evaluation_record_media_type_observation_selection_indeterminate_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding
    )
    evidence_coverage_indeterminate_media_type_comparison_result_binding: (
        SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.evaluation_record_media_type_observation_selection_indeterminate_comparison_result_binding,
            SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_media_type_observation_selection_"
                "indeterminate_comparison_result_binding must be a "
                "SecurityAdmissionEvaluationRecordMediaType"
                "ObservationSelectionIndeterminateComparisonResultBinding"
            )
        if not isinstance(
            self.evidence_coverage_indeterminate_media_type_comparison_result_binding,
            SecurityAdmissionEvidenceCoverageIndeterminateMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "evidence_coverage_indeterminate_media_type_"
                "comparison_result_binding must be a "
                "SecurityAdmissionEvidenceCoverageIndeterminateMediaType"
                "ComparisonResultBinding"
            )
        if (
            self.evaluation_record_media_type_observation_selection_indeterminate_comparison_result_binding
            .evaluation_record_indeterminate_media_type_comparison_result_binding
            != self.evidence_coverage_indeterminate_media_type_comparison_result_binding
            .evaluation_record_indeterminate_media_type_comparison_result_binding
        ):
            raise ValueError(
                "indeterminate media-type evidence coverage must use the "
                "governed recorded comparison result binding"
            )
