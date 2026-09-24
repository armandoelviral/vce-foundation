from dataclasses import dataclass

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
