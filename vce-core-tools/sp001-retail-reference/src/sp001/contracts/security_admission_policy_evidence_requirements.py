from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)


class SecurityAdmissionEvidenceDomain(StrEnum):
    """Closed evidence domains understood by admission policy requirements."""

    MEDIA_TYPE = "MEDIA_TYPE"
    BYTE_LENGTH = "BYTE_LENGTH"


@dataclass(frozen=True, slots=True)
class SecurityAdmissionPolicyEvidenceRequirements:
    """Evidence domains required by one exact admission policy identity."""

    admission_policy_identity: SecurityAdmissionPolicyIdentity
    required_evidence_domains: tuple[SecurityAdmissionEvidenceDomain, ...]

    def __post_init__(self) -> None:
        if not isinstance(
            self.admission_policy_identity,
            SecurityAdmissionPolicyIdentity,
        ):
            raise TypeError(
                "admission_policy_identity must be a "
                "SecurityAdmissionPolicyIdentity"
            )
        if not isinstance(self.required_evidence_domains, tuple):
            raise TypeError(
                "required_evidence_domains must be an immutable tuple"
            )
        if not self.required_evidence_domains:
            raise ValueError(
                "required_evidence_domains must not be empty"
            )

        seen_domains: set[SecurityAdmissionEvidenceDomain] = set()
        for domain in self.required_evidence_domains:
            if not isinstance(domain, SecurityAdmissionEvidenceDomain):
                raise TypeError(
                    "required_evidence_domains must contain "
                    "SecurityAdmissionEvidenceDomain values"
                )
            if domain in seen_domains:
                raise ValueError(
                    f"duplicate required evidence domain: {domain}"
                )
            seen_domains.add(domain)
