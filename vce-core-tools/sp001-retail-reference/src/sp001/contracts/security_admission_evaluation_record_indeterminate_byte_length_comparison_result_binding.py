from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordIndeterminateByteLengthComparisonResultBinding:
    """Bind one recorded evaluation to indeterminate byte-length evidence."""

    evaluation_record: SecurityAdmissionEvaluationRecord
    indeterminate_byte_length_comparison_result_binding: (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
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
            self.indeterminate_byte_length_comparison_result_binding,
            SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "indeterminate_byte_length_comparison_result_binding must be a "
                "SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding"
            )

        if (
            self.evaluation_record
            .evaluation_identity
            .evaluation_basis
            != self.indeterminate_byte_length_comparison_result_binding.evaluation_basis
        ):
            raise ValueError(
                "indeterminate byte-length result binding must use evaluation record basis"
            )
