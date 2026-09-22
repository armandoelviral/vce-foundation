from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_media_type_comparison_basis import (
    SecurityAdmissionCandidateMediaTypeComparisonBasis,
)
from sp001.contracts.security_admission_candidate_media_type_observation_selection_result import (
    SecurityAdmissionCandidateMediaTypeObservationSelectionResult,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonBasisBinding:
    """Bind a governed media-type selection to its comparison basis."""

    observation_selection_result: (
        SecurityAdmissionCandidateMediaTypeObservationSelectionResult
    )
    comparison_basis: SecurityAdmissionCandidateMediaTypeComparisonBasis

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_result,
            SecurityAdmissionCandidateMediaTypeObservationSelectionResult,
        ):
            raise TypeError(
                "observation_selection_result must be a "
                "SecurityAdmissionCandidateMediaTypeObservationSelectionResult"
            )
        if not isinstance(
            self.comparison_basis,
            SecurityAdmissionCandidateMediaTypeComparisonBasis,
        ):
            raise TypeError(
                "comparison_basis must be a "
                "SecurityAdmissionCandidateMediaTypeComparisonBasis"
            )
        if (
            self.comparison_basis.detected_media_type_observation
            != self.observation_selection_result.selected_observation
        ):
            raise ValueError(
                "comparison basis must use the selected "
                "media-type observation"
            )
