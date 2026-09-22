from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_media_type_observation_selection_comparison_result_binding import (
    SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_media_type_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordMediaTypeObservationSelectionComparisonResultBinding:
    """Bind one governed media-type result to its recorded evaluation."""

    observation_selection_comparison_result_binding: (
        SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonResultBinding
    )
    evaluation_record_media_type_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_comparison_result_binding,
            SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonResultBinding,
        ):
            raise TypeError(
                "observation_selection_comparison_result_binding must be a "
                "SecurityAdmissionCandidateMediaTypeObservationSelection"
                "ComparisonResultBinding"
            )
        if not isinstance(
            self.evaluation_record_media_type_comparison_result_binding,
            SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_media_type_comparison_result_binding "
                "must be a "
                "SecurityAdmissionEvaluationRecordMediaType"
                "ComparisonResultBinding"
            )
        if (
            self.observation_selection_comparison_result_binding
            .media_type_comparison_result_binding
            != self.evaluation_record_media_type_comparison_result_binding
            .media_type_comparison_result_binding
        ):
            raise ValueError(
                "recorded media-type result must use the governed "
                "comparison result binding"
            )
