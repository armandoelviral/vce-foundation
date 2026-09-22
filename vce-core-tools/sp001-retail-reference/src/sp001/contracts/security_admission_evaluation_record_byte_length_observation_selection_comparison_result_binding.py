from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record_byte_length_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordByteLengthComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding:
    """Bind one governed byte-length result to its recorded evaluation."""

    observation_selection_comparison_result_binding: (
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonResultBinding
    )
    evaluation_record_byte_length_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordByteLengthComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_comparison_result_binding,
            SecurityAdmissionCandidateByteLengthObservationSelectionComparisonResultBinding,
        ):
            raise TypeError(
                "observation_selection_comparison_result_binding must be a "
                "SecurityAdmissionCandidateByteLengthObservationSelection"
                "ComparisonResultBinding"
            )
        if not isinstance(
            self.evaluation_record_byte_length_comparison_result_binding,
            SecurityAdmissionEvaluationRecordByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_byte_length_comparison_result_binding "
                "must be a "
                "SecurityAdmissionEvaluationRecordByteLength"
                "ComparisonResultBinding"
            )
        if (
            self.observation_selection_comparison_result_binding
            .byte_length_comparison_result_binding
            != self.evaluation_record_byte_length_comparison_result_binding
            .byte_length_comparison_result_binding
        ):
            raise ValueError(
                "recorded byte-length result must use the governed "
                "comparison result binding"
            )
