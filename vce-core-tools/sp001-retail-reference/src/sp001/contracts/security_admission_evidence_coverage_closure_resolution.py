from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_closure_blockage import (
    SecurityAdmissionEvidenceCoverageClosureBlockage,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)


SecurityAdmissionEvidenceCoverageClosureResolutionValue = (
    SecurityAdmissionEvidenceCoverageClosure
    | SecurityAdmissionEvidenceCoverageClosureBlockage
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureResolution:
    """Preserve one exhaustive terminal result of evidence coverage closure."""

    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity
    outcome: SecurityAdmissionEvidenceCoverageClosureResolutionValue

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
                SecurityAdmissionEvidenceCoverageClosure,
                SecurityAdmissionEvidenceCoverageClosureBlockage,
            ),
        ):
            raise TypeError(
                "outcome must be one complete coverage closure "
                "or closure blockage"
            )

        outcome_coverage_identity = (
            self.outcome.resolution_outcome_set.coverage_identity
            if isinstance(
                self.outcome,
                SecurityAdmissionEvidenceCoverageClosure,
            )
            else self.outcome.coverage_identity
        )
        if outcome_coverage_identity != self.coverage_identity:
            raise ValueError(
                "closure outcome must use the exact coverage identity"
            )
