from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_media_type_comparison_result_binding import (
    SecurityAdmissionCandidateMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_candidate_media_type_observation_selection_comparison_basis_binding import (
    SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonBasisBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonResultBinding:
    """Bind governed media-type lineage to one conclusive result."""

    observation_selection_comparison_basis_binding: (
        SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonBasisBinding
    )
    media_type_comparison_result_binding: (
        SecurityAdmissionCandidateMediaTypeComparisonResultBinding
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_selection_comparison_basis_binding,
            SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonBasisBinding,
        ):
            raise TypeError(
                "observation_selection_comparison_basis_binding must be a "
                "SecurityAdmissionCandidateMediaTypeObservationSelection"
                "ComparisonBasisBinding"
            )
        if not isinstance(
            self.media_type_comparison_result_binding,
            SecurityAdmissionCandidateMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "media_type_comparison_result_binding must be a "
                "SecurityAdmissionCandidateMediaTypeComparisonResultBinding"
            )

        governed_basis = (
            self.observation_selection_comparison_basis_binding
            .comparison_basis
        )
        result_basis = (
            self.media_type_comparison_result_binding
            .media_type_comparison_result
            .comparison_basis
        )
        if governed_basis != result_basis:
            raise ValueError(
                "media-type comparison result must use the governed "
                "comparison basis"
            )
