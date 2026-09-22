from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_media_type_observation_set import (
    SecurityAdmissionCandidateMediaTypeObservationSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.contracts.security_admission_policy_verification_procedure_authority_order import (
    SecurityAdmissionPolicyVerificationProcedureAuthorityOrder,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateMediaTypeObservationResolutionBasis:
    """Observation set and exact policy authority order for later resolution."""

    observation_set: SecurityAdmissionCandidateMediaTypeObservationSet
    authority_order: (
        SecurityAdmissionPolicyVerificationProcedureAuthorityOrder
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_set,
            SecurityAdmissionCandidateMediaTypeObservationSet,
        ):
            raise TypeError(
                "observation_set must be a "
                "SecurityAdmissionCandidateMediaTypeObservationSet"
            )
        if not isinstance(
            self.authority_order,
            SecurityAdmissionPolicyVerificationProcedureAuthorityOrder,
        ):
            raise TypeError(
                "authority_order must be a "
                "SecurityAdmissionPolicyVerificationProcedureAuthorityOrder"
            )
        if (
            self.authority_order.evidence_domain
            is not SecurityAdmissionEvidenceDomain.MEDIA_TYPE
        ):
            raise ValueError(
                "authority_order must govern the MEDIA_TYPE evidence domain"
            )
