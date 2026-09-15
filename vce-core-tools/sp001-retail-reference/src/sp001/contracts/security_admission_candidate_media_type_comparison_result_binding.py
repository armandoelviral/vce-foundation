from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_media_type_comparison_result import (
    SecurityAdmissionCandidateMediaTypeComparisonResult,
)
from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeComparisonResultBinding:
    """Bind one conclusive media-type result to its evaluation basis."""

    evaluation_basis: SecurityAdmissionEvaluationBasis
    media_type_comparison_result: (
        SecurityAdmissionCandidateMediaTypeComparisonResult
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
            self.media_type_comparison_result,
            SecurityAdmissionCandidateMediaTypeComparisonResult,
        ):
            raise TypeError(
                "media_type_comparison_result must be a "
                "SecurityAdmissionCandidateMediaTypeComparisonResult"
            )

        result_candidate_identity = (
            self.media_type_comparison_result
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
                "media-type comparison result candidate_identity "
                "does not match evaluation_basis"
            )
