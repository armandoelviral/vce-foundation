from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_media_type_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionCandidateMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_indeterminate_media_type_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionIndeterminateComparisonResultBinding:
    """Bind one governed indeterminate media-type result to its evaluation."""

    observation_selection_indeterminate_comparison_result_binding: (
        SecurityAdmissionCandidateMediaTypeObservationSelectionIndeterminateComparisonResultBinding
    )
    evaluation_record_indeterminate_media_type_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_indeterminate_comparison_result_binding,
            SecurityAdmissionCandidateMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
        ):
            raise TypeError(
                "observation_selection_indeterminate_comparison_result_binding "
                "must be a "
                "SecurityAdmissionCandidateMediaTypeObservationSelection"
                "IndeterminateComparisonResultBinding"
            )
        if not isinstance(
            self.evaluation_record_indeterminate_media_type_comparison_result_binding,
            SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_indeterminate_media_type_comparison_result_binding "
                "must be a "
                "SecurityAdmissionEvaluationRecordIndeterminateMediaType"
                "ComparisonResultBinding"
            )
        if (
            self.observation_selection_indeterminate_comparison_result_binding
            .indeterminate_media_type_comparison_result_binding
            != self.evaluation_record_indeterminate_media_type_comparison_result_binding
            .indeterminate_media_type_comparison_result_binding
        ):
            raise ValueError(
                "recorded indeterminate media-type result must use the governed "
                "comparison result binding"
            )
