from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_comparison_result import (
    SecurityAdmissionCandidateByteLengthComparisonResult,
)
from sp001.contracts.security_admission_evaluation_basis import (
    SecurityAdmissionEvaluationBasis,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthComparisonResultBinding:
    """Bind one conclusive byte-length result to its evaluation basis."""

    evaluation_basis: SecurityAdmissionEvaluationBasis
    byte_length_comparison_result: (
        SecurityAdmissionCandidateByteLengthComparisonResult
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
            self.byte_length_comparison_result,
            SecurityAdmissionCandidateByteLengthComparisonResult,
        ):
            raise TypeError(
                "byte_length_comparison_result must be a "
                "SecurityAdmissionCandidateByteLengthComparisonResult"
            )

        result_candidate_identity = (
            self.byte_length_comparison_result
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
                "byte-length comparison result candidate_identity "
                "does not match evaluation_basis"
            )
