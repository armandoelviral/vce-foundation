from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_observation_set import (
    SecurityAdmissionCandidateByteLengthObservationSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.contracts.security_admission_policy_verification_procedure_authority_order import (
    SecurityAdmissionPolicyVerificationProcedureAuthorityOrder,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionCandidateByteLengthObservationResolutionBasis:
    """Observation set and exact policy authority order for later resolution."""

    observation_set: SecurityAdmissionCandidateByteLengthObservationSet
    authority_order: (
        SecurityAdmissionPolicyVerificationProcedureAuthorityOrder
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.observation_set,
            SecurityAdmissionCandidateByteLengthObservationSet,
        ):
            raise TypeError(
                "observation_set must be a "
                "SecurityAdmissionCandidateByteLengthObservationSet"
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
            is not SecurityAdmissionEvidenceDomain.BYTE_LENGTH
        ):
            raise ValueError(
                "authority_order must govern the BYTE_LENGTH evidence domain"
            )
