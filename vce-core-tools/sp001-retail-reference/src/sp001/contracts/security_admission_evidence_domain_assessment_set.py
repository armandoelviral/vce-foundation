from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_domain_assessment import (
    SecurityAdmissionEvidenceDomainAssessment,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceDomainAssessmentSet:
    """Exhaustive policy-ordered assessments for one complete coverage closure."""

    coverage_closure: SecurityAdmissionEvidenceCoverageClosure
    assessments: tuple[
        SecurityAdmissionEvidenceDomainAssessment,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.coverage_closure,
            SecurityAdmissionEvidenceCoverageClosure,
        ):
            raise TypeError(
                "coverage_closure must be a "
                "SecurityAdmissionEvidenceCoverageClosure"
            )
        if not isinstance(self.assessments, tuple):
            raise TypeError(
                "assessments must be an immutable tuple"
            )
        if not self.assessments:
            raise ValueError("assessments must not be empty")

        outcome_set = self.coverage_closure.resolution_outcome_set
        required_domains = (
            outcome_set.coverage_identity
            .evaluation_record_policy_evidence_requirements_binding
            .policy_evidence_requirements
            .required_evidence_domains
        )

        if len(self.assessments) != len(required_domains):
            raise ValueError(
                "assessments must contain exactly one assessment "
                "for every required evidence domain"
            )

        for assessment in self.assessments:
            if not isinstance(
                assessment,
                SecurityAdmissionEvidenceDomainAssessment,
            ):
                raise TypeError(
                    "assessments must contain "
                    "SecurityAdmissionEvidenceDomainAssessment values"
                )

        assessment_domains = tuple(
            assessment.domain
            for assessment in self.assessments
        )
        if assessment_domains != required_domains:
            raise ValueError(
                "assessments must preserve required evidence domain order"
            )

        for assessment, resolution_outcome in zip(
            self.assessments,
            outcome_set.outcomes,
        ):
            if assessment.coverage_closure is not self.coverage_closure:
                raise ValueError(
                    "each assessment must use the exact coverage closure"
                )
            if assessment.resolution_outcome is not resolution_outcome:
                raise ValueError(
                    "each assessment must use the corresponding "
                    "resolution outcome"
                )
