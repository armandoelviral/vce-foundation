from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordByteLengthComparisonResultBinding:
    """Bind one recorded evaluation to its conclusive byte-length evidence."""

    evaluation_record: SecurityAdmissionEvaluationRecord
    byte_length_comparison_result_binding: (
        SecurityAdmissionCandidateByteLengthComparisonResultBinding
    )

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
            self.byte_length_comparison_result_binding,
            SecurityAdmissionCandidateByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "byte_length_comparison_result_binding must be a "
                "SecurityAdmissionCandidateByteLengthComparisonResultBinding"
            )

        if (
            self.evaluation_record
            .evaluation_identity
            .evaluation_basis
            != self.byte_length_comparison_result_binding.evaluation_basis
        ):
            raise ValueError(
                "byte-length result binding must use evaluation record basis"
            )
