from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_comparison_basis import (
    SecurityAdmissionCandidateByteLengthComparisonBasis,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_result import (
    SecurityAdmissionCandidateByteLengthObservationSelectionResult,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthObservationSelectionComparisonBasisBinding:
    """Bind a governed byte-length selection to its comparison basis."""

    observation_selection_result: (
        SecurityAdmissionCandidateByteLengthObservationSelectionResult
    )
    comparison_basis: SecurityAdmissionCandidateByteLengthComparisonBasis

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_result,
            SecurityAdmissionCandidateByteLengthObservationSelectionResult,
        ):
            raise TypeError(
                "observation_selection_result must be a "
                "SecurityAdmissionCandidateByteLengthObservationSelectionResult"
            )
        if not isinstance(
            self.comparison_basis,
            SecurityAdmissionCandidateByteLengthComparisonBasis,
        ):
            raise TypeError(
                "comparison_basis must be a "
                "SecurityAdmissionCandidateByteLengthComparisonBasis"
            )
        if (
            self.comparison_basis.measured_byte_length_observation
            != self.observation_selection_result.selected_observation
        ):
            raise ValueError(
                "comparison basis must use the selected "
                "byte-length observation"
            )
