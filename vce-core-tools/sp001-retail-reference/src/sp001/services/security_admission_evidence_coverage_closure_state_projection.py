from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_closure_resolution import (
    SecurityAdmissionEvidenceCoverageClosureResolution,
)
from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.contracts.security_admission_evidence_coverage_domain_closure_state import (
    SecurityAdmissionEvidenceCoverageDomainClosureState,
    SecurityAdmissionEvidenceCoverageDomainClosureStatus,
)


def project_security_admission_evidence_coverage_closure_state(
    closure_resolution: SecurityAdmissionEvidenceCoverageClosureResolution,
) -> SecurityAdmissionEvidenceCoverageClosureStateRecord:
    """Project one terminal closure result into ordered canonical domain states."""

    if not isinstance(
        closure_resolution,
        SecurityAdmissionEvidenceCoverageClosureResolution,
    ):
        raise TypeError(
            "closure_resolution must be a "
            "SecurityAdmissionEvidenceCoverageClosureResolution"
        )

    required_domains = (
        closure_resolution
        .coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
        .required_evidence_domains
    )

    if isinstance(
        closure_resolution.outcome,
        SecurityAdmissionEvidenceCoverageClosure,
    ):
        statuses = (
            SecurityAdmissionEvidenceCoverageDomainClosureStatus.RESOLVED,
        ) * len(required_domains)
    else:
        resolved_count = len(
            closure_resolution.outcome.resolved_prefix
        )
        statuses = (
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

    domain_states = tuple(
        SecurityAdmissionEvidenceCoverageDomainClosureState(
            domain=domain,
            status=status,
        )
        for domain, status in zip(
            required_domains,
            statuses,
            strict=True,
        )
    )

    return SecurityAdmissionEvidenceCoverageClosureStateRecord(
        closure_resolution=closure_resolution,
        domain_states=domain_states,
    )
