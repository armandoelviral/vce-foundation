from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result import (
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult,
)
from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding:
    """Bind one indeterminate byte-length result to its evaluation basis."""

    evaluation_basis: SecurityAdmissionEvaluationBasis
    indeterminate_byte_length_comparison_result: (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult
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
            self.indeterminate_byte_length_comparison_result,
            SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult,
        ):
            raise TypeError(
                "indeterminate_byte_length_comparison_result must be a "
                "SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult"
            )

        result_candidate_identity = (
            self.indeterminate_byte_length_comparison_result
            .comparison_basis
            .declared_byte_length
            .metadata_identity
            .candidate_identity
        )
        if (
            result_candidate_identity
            != self.evaluation_basis.candidate_identity
        ):
            raise ValueError(
                "indeterminate byte-length comparison result "
                "candidate_identity does not match evaluation_basis"
            )
