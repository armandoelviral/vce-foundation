from dataclasses import dataclass

from sp001.contracts.security_admission_evaluation_record_byte_length_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvaluationRecordByteLengthObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageIndeterminateByteLengthComparisonResultBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionIndeterminateComparisonResultBinding:
    """Bind one governed recorded indeterminate byte-length result to coverage."""

    evaluation_record_byte_length_observation_selection_indeterminate_comparison_result_binding: (
        SecurityAdmissionEvaluationRecordByteLengthObservationSelectionIndeterminateComparisonResultBinding
    )
    evidence_coverage_indeterminate_byte_length_comparison_result_binding: (
        SecurityAdmissionEvidenceCoverageIndeterminateByteLengthComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.evaluation_record_byte_length_observation_selection_indeterminate_comparison_result_binding,
            SecurityAdmissionEvaluationRecordByteLengthObservationSelectionIndeterminateComparisonResultBinding,
        ):
            raise TypeError(
                "evaluation_record_byte_length_observation_selection_"
                "indeterminate_comparison_result_binding must be a "
                "SecurityAdmissionEvaluationRecordByteLength"
                "ObservationSelectionIndeterminateComparisonResultBinding"
            )
        if not isinstance(
            self.evidence_coverage_indeterminate_byte_length_comparison_result_binding,
            SecurityAdmissionEvidenceCoverageIndeterminateByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "evidence_coverage_indeterminate_byte_length_"
                "comparison_result_binding must be a "
                "SecurityAdmissionEvidenceCoverageIndeterminateByteLength"
                "ComparisonResultBinding"
            )
        if (
            self.evaluation_record_byte_length_observation_selection_indeterminate_comparison_result_binding
            .evaluation_record_indeterminate_byte_length_comparison_result_binding
            != self.evidence_coverage_indeterminate_byte_length_comparison_result_binding
            .evaluation_record_indeterminate_byte_length_comparison_result_binding
        ):
            raise ValueError(
                "indeterminate byte-length evidence coverage must use the "
                "governed recorded comparison result binding"
            )
