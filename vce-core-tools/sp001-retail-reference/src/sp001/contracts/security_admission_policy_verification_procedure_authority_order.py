from dataclasses import dataclass

from sp001.contracts.security_admission_metadata_verification_procedure_identity import (
    SecurityAdmissionMetadataVerificationProcedureIdentity,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionPolicyVerificationProcedureAuthorityOrder:
    """Policy-defined highest-to-lowest procedure authority for one domain."""

    admission_policy_identity: SecurityAdmissionPolicyIdentity
    evidence_domain: SecurityAdmissionEvidenceDomain
    verification_procedure_identities: tuple[
        SecurityAdmissionMetadataVerificationProcedureIdentity, ...
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.admission_policy_identity,
            SecurityAdmissionPolicyIdentity,
        ):
            raise TypeError(
                "admission_policy_identity must be a "
                "SecurityAdmissionPolicyIdentity"
            )
        if not isinstance(
            self.evidence_domain,
            SecurityAdmissionEvidenceDomain,
        ):
            raise TypeError(
                "evidence_domain must be a "
                "SecurityAdmissionEvidenceDomain"
            )
        if not isinstance(
            self.verification_procedure_identities,
            tuple,
        ):
            raise TypeError(
                "verification_procedure_identities must be an immutable tuple"
            )
        if not self.verification_procedure_identities:
            raise ValueError(
                "verification_procedure_identities must not be empty"
            )

        seen_identities: set[
            SecurityAdmissionMetadataVerificationProcedureIdentity
        ] = set()
        for identity in self.verification_procedure_identities:
            if not isinstance(
                identity,
                SecurityAdmissionMetadataVerificationProcedureIdentity,
            ):
                raise TypeError(
                    "verification_procedure_identities must contain "
                    "SecurityAdmissionMetadataVerificationProcedureIdentity "
                    "values"
                )
            if identity in seen_identities:
                raise ValueError(
                    "duplicate verification procedure identity"
                )
            seen_identities.add(identity)
