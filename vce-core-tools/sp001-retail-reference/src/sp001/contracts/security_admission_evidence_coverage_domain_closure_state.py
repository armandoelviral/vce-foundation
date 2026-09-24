from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)


class SecurityAdmissionEvidenceCoverageDomainClosureStatus(StrEnum):
    """Closed state vocabulary for one required evidence domain."""

    RESOLVED = "RESOLVED"
    IMPEDED = "IMPEDED"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageDomainClosureState:
    """Record the terminal closure state of one required evidence domain."""

    domain: SecurityAdmissionEvidenceDomain
    status: SecurityAdmissionEvidenceCoverageDomainClosureStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.domain,
            SecurityAdmissionEvidenceDomain,
        ):
            raise TypeError(
                "domain must be a SecurityAdmissionEvidenceDomain"
            )
        if not isinstance(
            self.status,
            SecurityAdmissionEvidenceCoverageDomainClosureStatus,
        ):
            raise TypeError(
                "status must be a "
                "SecurityAdmissionEvidenceCoverageDomainClosureStatus"
            )
