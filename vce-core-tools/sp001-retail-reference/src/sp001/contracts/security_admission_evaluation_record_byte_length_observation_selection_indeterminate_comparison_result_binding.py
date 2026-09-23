from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordByteLengthObservationSelectionIndeterminateComparisonResultBinding:
    """Bind one governed indeterminate byte-length result to its evaluation."""

    observation_selection_indeterminate_comparison_result_binding: (
        SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding
    )
    evaluation_record_indeterminate_byte_length_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_indeterminate_comparison_result_binding,
            SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding,
        ):
            raise TypeError(
                "observation_selection_indeterminate_comparison_result_binding "
                "must be a "
                "SecurityAdmissionCandidateByteLengthObservationSelection"
                "IndeterminateComparisonResultBinding"
            )
        if not isinstance(
            self.evaluation_record_indeterminate_byte_length_comparison_result_binding,
            SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_indeterminate_byte_length_comparison_result_binding "
                "must be a "
                "SecurityAdmissionEvaluationRecordIndeterminateByteLength"
                "ComparisonResultBinding"
            )
        if (
            self.observation_selection_indeterminate_comparison_result_binding
            .indeterminate_byte_length_comparison_result_binding
            != self.evaluation_record_indeterminate_byte_length_comparison_result_binding
            .indeterminate_byte_length_comparison_result_binding
        ):
            raise ValueError(
                "recorded indeterminate byte-length result must use the governed "
                "comparison result binding"
            )
