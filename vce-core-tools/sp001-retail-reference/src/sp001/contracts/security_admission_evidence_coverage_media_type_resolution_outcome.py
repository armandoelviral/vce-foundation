from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_closure_impediment import (
    SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
)


SecurityAdmissionEvidenceCoverageMediaTypeOutcomeValue = (
    SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding
    | SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding
    | SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome:
    """Exactly one media-type result or closure impediment for one coverage."""

    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity
    outcome: SecurityAdmissionEvidenceCoverageMediaTypeOutcomeValue

    def __post_init__(self) -> None:
        if not isinstance(
            self.coverage_identity,
            SecurityAdmissionEvidenceCoverageIdentity,
        ):
            raise TypeError(
                "coverage_identity must be a "
                "SecurityAdmissionEvidenceCoverageIdentity"
            )
        if not isinstance(
            self.outcome,
            (
                SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
                SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
                SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
            ),
        ):
            raise TypeError(
                "outcome must be one media-type conclusive result, "
                "indeterminate result or closure impediment"
            )
        if isinstance(
            self.outcome,
            SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
        ):
            outcome_coverage_identity = (
                self.outcome
                .evidence_coverage_media_type_comparison_result_binding
                .coverage_identity
            )
        elif isinstance(
            self.outcome,
            SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
        ):
            outcome_coverage_identity = (
                self.outcome
                .evidence_coverage_indeterminate_media_type_comparison_result_binding
                .coverage_identity
            )
        else:
            outcome_coverage_identity = self.outcome.coverage_identity
        if self.coverage_identity != outcome_coverage_identity:
            raise ValueError(
                "media-type outcome must use the exact coverage identity"
            )
