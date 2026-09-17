from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_media_type_comparison_result_binding import (
    SecurityAdmissionCandidateMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvaluationRecordMediaTypeComparisonResultBinding:
    """Bind one recorded evaluation to its conclusive media-type evidence."""

    evaluation_record: SecurityAdmissionEvaluationRecord
    media_type_comparison_result_binding: (
        SecurityAdmissionCandidateMediaTypeComparisonResultBinding
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
            self.media_type_comparison_result_binding,
            SecurityAdmissionCandidateMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "media_type_comparison_result_binding must be a "
                "SecurityAdmissionCandidateMediaTypeComparisonResultBinding"
            )

        if (
            self.evaluation_record
            .evaluation_identity
            .evaluation_basis
            != self.media_type_comparison_result_binding.evaluation_basis
        ):
            raise ValueError(
                "media-type result binding must use evaluation record basis"
            )
