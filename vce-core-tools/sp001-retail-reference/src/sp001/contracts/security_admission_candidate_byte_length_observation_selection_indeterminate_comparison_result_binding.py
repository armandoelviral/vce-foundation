from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_comparison_basis_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthObservationSelectionIndeterminateComparisonResultBinding:
    """Bind governed byte-length lineage to one indeterminate result."""

    observation_selection_comparison_basis_binding: (
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding
    )
    indeterminate_byte_length_comparison_result_binding: (
        SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_comparison_basis_binding,
            SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding,
        ):
            raise TypeError(
                "observation_selection_comparison_basis_binding must be a "
                "SecurityAdmissionCandidateByteLengthObservationSelection"
                "ComparisonBasisBinding"
            )
        if not isinstance(
            self.indeterminate_byte_length_comparison_result_binding,
            SecurityAdmissionCandidateIndeterminateByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "indeterminate_byte_length_comparison_result_binding must be a "
                "SecurityAdmissionCandidateIndeterminateByteLength"
                "ComparisonResultBinding"
            )

        governed_basis = (
            self.observation_selection_comparison_basis_binding
            .comparison_basis
        )
        result_basis = (
            self.indeterminate_byte_length_comparison_result_binding
            .indeterminate_byte_length_comparison_result
            .comparison_basis
        )
        if governed_basis != result_basis:
            raise ValueError(
                "indeterminate byte-length comparison result must use "
                "the governed comparison basis"
            )
