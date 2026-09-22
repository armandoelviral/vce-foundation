from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_comparison_result_binding import (
    SecurityAdmissionCandidateByteLengthComparisonResultBinding,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_comparison_basis_binding import (
    SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthObservationSelectionComparisonResultBinding:
    """Bind governed byte-length lineage to one conclusive result."""

    observation_selection_comparison_basis_binding: (
        SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding
    )
    byte_length_comparison_result_binding: (
        SecurityAdmissionCandidateByteLengthComparisonResultBinding
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
            self.byte_length_comparison_result_binding,
            SecurityAdmissionCandidateByteLengthComparisonResultBinding,
        ):
            raise TypeError(
                "byte_length_comparison_result_binding must be a "
                "SecurityAdmissionCandidateByteLengthComparisonResultBinding"
            )

        governed_basis = (
            self.observation_selection_comparison_basis_binding
            .comparison_basis
        )
        result_basis = (
            self.byte_length_comparison_result_binding
            .byte_length_comparison_result
            .comparison_basis
        )
        if governed_basis != result_basis:
            raise ValueError(
                "byte-length comparison result must use the governed "
                "comparison basis"
            )
