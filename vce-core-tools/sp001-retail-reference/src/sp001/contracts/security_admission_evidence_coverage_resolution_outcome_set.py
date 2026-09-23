from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_byte_length_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)


SecurityAdmissionEvidenceCoverageResolutionOutcome = (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome
    | SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageResolutionOutcomeSet:
    """Preserve exactly one ordered resolution outcome per required domain."""

    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity
    outcomes: tuple[
        SecurityAdmissionEvidenceCoverageResolutionOutcome,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.coverage_identity,
            SecurityAdmissionEvidenceCoverageIdentity,
        ):
            raise TypeError(
                "coverage_identity must be a "
                "SecurityAdmissionEvidenceCoverageIdentity"
            )
        if not isinstance(self.outcomes, tuple):
            raise TypeError("outcomes must be an immutable tuple")
        if not self.outcomes:
            raise ValueError("outcomes must not be empty")

        actual_domains: list[SecurityAdmissionEvidenceDomain] = []
        for outcome in self.outcomes:
            if isinstance(
                outcome,
                SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
            ):
                domain = SecurityAdmissionEvidenceDomain.MEDIA_TYPE
            elif isinstance(
                outcome,
                SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
            ):
                domain = SecurityAdmissionEvidenceDomain.BYTE_LENGTH
            else:
                raise TypeError(
                    "outcomes must contain "
                    "SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome "
                    "or "
                    "SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome "
                    "values"
                )

            if outcome.coverage_identity != self.coverage_identity:
                raise ValueError(
                    "each outcome must use the coverage identity"
                )

            actual_domains.append(domain)

        required_domains = (
            self.coverage_identity
            .evaluation_record_policy_evidence_requirements_binding
            .policy_evidence_requirements
            .required_evidence_domains
        )
        if tuple(actual_domains) != required_domains:
            raise ValueError(
                "outcome domains must exactly match required evidence domains"
            )
