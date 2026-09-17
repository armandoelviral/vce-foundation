from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_indeterminate_media_type_comparison_result_binding import (
    SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordIndeterminateMediaTypeComparisonResultBinding:
    """Bind one recorded evaluation to indeterminate media-type evidence."""

    evaluation_record: SecurityAdmissionEvaluationRecord
    indeterminate_media_type_comparison_result_binding: (
        SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding
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
            self.indeterminate_media_type_comparison_result_binding,
            SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "indeterminate_media_type_comparison_result_binding must be a "
                "SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding"
            )

        if (
            self.evaluation_record
            .evaluation_identity
            .evaluation_basis
            != self.indeterminate_media_type_comparison_result_binding.evaluation_basis
        ):
            raise ValueError(
                "indeterminate media-type result binding must use evaluation record basis"
            )
