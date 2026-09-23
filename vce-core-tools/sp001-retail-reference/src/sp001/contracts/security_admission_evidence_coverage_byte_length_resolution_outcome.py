from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_closure_impediment import (
    SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionIndeterminateComparisonResultBinding,
)


SecurityAdmissionEvidenceCoverageByteLengthOutcomeValue = (
    SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding
    | SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionIndeterminateComparisonResultBinding
    | SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome:
    """Exactly one byte-length result or closure impediment for one coverage."""

    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity
    outcome: SecurityAdmissionEvidenceCoverageByteLengthOutcomeValue

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
                SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding,
                SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionIndeterminateComparisonResultBinding,
                SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
            ),
        ):
            raise TypeError(
                "outcome must be one byte-length conclusive result, "
                "indeterminate result or closure impediment"
            )
        if isinstance(
            self.outcome,
            SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding,
        ):
            outcome_coverage_identity = (
                self.outcome
                .evidence_coverage_byte_length_comparison_result_binding
                .coverage_identity
            )
        elif isinstance(
            self.outcome,
            SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionIndeterminateComparisonResultBinding,
        ):
            outcome_coverage_identity = (
                self.outcome
                .evidence_coverage_indeterminate_byte_length_comparison_result_binding
                .coverage_identity
            )
        else:
            outcome_coverage_identity = self.outcome.coverage_identity
        if self.coverage_identity != outcome_coverage_identity:
            raise ValueError(
                "byte-length outcome must use the exact coverage identity"
            )
