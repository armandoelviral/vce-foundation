from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_byte_length_closure_impediment import (
    SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_closure_impediment import (
    SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_resolution_outcome_set import (
    SecurityAdmissionEvidenceCoverageResolutionOutcomeSet,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosure:
    """Close exhaustive technical coverage without unresolved impediments."""

    resolution_outcome_set: (
        SecurityAdmissionEvidenceCoverageResolutionOutcomeSet
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.resolution_outcome_set,
            SecurityAdmissionEvidenceCoverageResolutionOutcomeSet,
        ):
            raise TypeError(
                "resolution_outcome_set must be a "
                "SecurityAdmissionEvidenceCoverageResolutionOutcomeSet"
            )

        impediment_types = (
            SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
            SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
        )
        if any(
            isinstance(outcome.outcome, impediment_types)
            for outcome in self.resolution_outcome_set.outcomes
        ):
            raise ValueError(
                "resolution_outcome_set must not contain "
                "closure impediments"
            )
