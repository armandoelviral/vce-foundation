from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_indeterminate_media_type_comparison_result import (
    SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResult,
)
from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding:
    """Bind one indeterminate media-type result to its evaluation basis."""

    evaluation_basis: SecurityAdmissionEvaluationBasis
    indeterminate_media_type_comparison_result: (
        SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResult
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.evaluation_basis,
            SecurityAdmissionEvaluationBasis,
        ):
            raise TypeError(
                "evaluation_basis must be a "
                "SecurityAdmissionEvaluationBasis"
            )
        if not isinstance(
            self.indeterminate_media_type_comparison_result,
            SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResult,
        ):
            raise TypeError(
                "indeterminate_media_type_comparison_result must be a "
                "SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResult"
            )

        result_candidate_identity = (
            self.indeterminate_media_type_comparison_result
            .comparison_basis
            .declared_media_type
            .metadata_identity
            .candidate_identity
        )
        if (
            result_candidate_identity
            != self.evaluation_basis.candidate_identity
        ):
            raise ValueError(
                "indeterminate media-type comparison result "
                "candidate_identity does not match evaluation_basis"
            )
