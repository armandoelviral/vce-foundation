from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_indeterminate_media_type_comparison_result_binding import (
    SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding,
)
from sp001.contracts.security_admission_candidate_media_type_observation_selection_comparison_basis_binding import (
    SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonBasisBinding,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeObservationSelectionIndeterminateComparisonResultBinding:
    """Bind governed media-type lineage to one indeterminate result."""

    observation_selection_comparison_basis_binding: (
        SecurityAdmissionCandidateMediaTypeObservationSelectionComparisonBasisBinding
    )
    indeterminate_media_type_comparison_result_binding: (
        SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding
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
            self.indeterminate_media_type_comparison_result_binding,
            SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResultBinding,
        ):
            raise TypeError(
                "indeterminate_media_type_comparison_result_binding must be a "
                "SecurityAdmissionCandidateIndeterminateMediaType"
                "ComparisonResultBinding"
            )

        governed_basis = (
            self.observation_selection_comparison_basis_binding
            .comparison_basis
        )
        result_basis = (
            self.indeterminate_media_type_comparison_result_binding
            .indeterminate_media_type_comparison_result
            .comparison_basis
        )
        if governed_basis != result_basis:
            raise ValueError(
                "indeterminate media-type comparison result must use "
                "the governed comparison basis"
            )
