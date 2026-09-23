from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_record_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageByteLengthComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding:
    """Bind one governed recorded byte-length result to evidence coverage."""

    evaluation_record_byte_length_observation_selection_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding
    )
    evidence_coverage_byte_length_comparison_result_binding: (
        SecurityAdmissionEvidenceCoverageByteLengthComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.evaluation_record_byte_length_observation_selection_comparison_result_binding,
            SecurityAdmissionEvaluationRecordByteLengthObservationSelectionComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_byte_length_observation_selection_"
                "comparison_result_binding must be a "
                "SecurityAdmissionEvaluationRecordByteLength"
                "ObservationSelectionComparisonResultBinding"
            )
        if not isinstance(
            self.evidence_coverage_byte_length_comparison_result_binding,
            SecurityAdmissionEvidenceCoverageByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "evidence_coverage_byte_length_comparison_result_binding "
                "must be a "
                "SecurityAdmissionEvidenceCoverageByteLength"
                "ComparisonResultBinding"
            )
        if (
            self.evaluation_record_byte_length_observation_selection_comparison_result_binding
            .evaluation_record_byte_length_comparison_result_binding
            != self.evidence_coverage_byte_length_comparison_result_binding
            .evaluation_record_byte_length_comparison_result_binding
        ):
            raise ValueError(
                "byte-length evidence coverage must use the governed "
                "recorded comparison result binding"
            )
