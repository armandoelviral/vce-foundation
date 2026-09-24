from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_closure_resolution import (
    SecurityAdmissionEvidenceCoverageClosureResolution,
)
from sp001.contracts.security_admission_evidence_coverage_domain_closure_state import (
    SecurityAdmissionEvidenceCoverageDomainClosureState,
    SecurityAdmissionEvidenceCoverageDomainClosureStatus,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateRecord:
    """Bind one terminal closure result to its ordered canonical domain states."""

    closure_resolution: SecurityAdmissionEvidenceCoverageClosureResolution
    domain_states: tuple[
        SecurityAdmissionEvidenceCoverageDomainClosureState,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.closure_resolution,
            SecurityAdmissionEvidenceCoverageClosureResolution,
        ):
            raise TypeError(
                "closure_resolution must be a "
                "SecurityAdmissionEvidenceCoverageClosureResolution"
            )
        if not isinstance(self.domain_states, tuple):
            raise TypeError(
                "domain_states must be an immutable tuple"
            )

        required_domains = (
            self.closure_resolution
            .coverage_identity
            .evaluation_record_policy_evidence_requirements_binding
            .policy_evidence_requirements
            .required_evidence_domains
        )
        if len(self.domain_states) != len(required_domains):
            raise ValueError(
                "domain_states must contain exactly one state "
                "for each required evidence domain"
            )

        for state in self.domain_states:
            if not isinstance(
                state,
                SecurityAdmissionEvidenceCoverageDomainClosureState,
            ):
                raise TypeError(
                    "domain_states must contain "
                    "SecurityAdmissionEvidenceCoverageDomainClosureState "
                    "values"
                )

        recorded_domains = tuple(
            state.domain
            for state in self.domain_states
        )
        if recorded_domains != required_domains:
            raise ValueError(
                "domain_states must preserve required evidence domain order"
            )

        if isinstance(
            self.closure_resolution.outcome,
            SecurityAdmissionEvidenceCoverageClosure,
        ):
            expected_statuses = (
                SecurityAdmissionEvidenceCoverageDomainClosureStatus.RESOLVED,
            ) * len(required_domains)
        else:
            resolved_count = len(
                self.closure_resolution.outcome.resolved_prefix
            )
            expected_statuses = (
                (
                    SecurityAdmissionEvidenceCoverageDomainClosureStatus.RESOLVED,
                )
                * resolved_count
                + (
                    SecurityAdmissionEvidenceCoverageDomainClosureStatus.IMPEDED,
                )
                + (
                    (
                        SecurityAdmissionEvidenceCoverageDomainClosureStatus.NOT_EVALUATED,
                    )
                    * (
                        len(required_domains)
                        - resolved_count
                        - 1
                    )
                )
            )

        recorded_statuses = tuple(
            state.status
            for state in self.domain_states
        )
        if recorded_statuses != expected_statuses:
            raise ValueError(
                "domain_states must exactly represent "
                "the terminal closure result"
            )
