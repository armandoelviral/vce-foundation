from dataclasses import dataclass

from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_conflict_result import (
    SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment:
    """Bind a byte-length resolution conflict preventing coverage closure."""

    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity
    resolution_conflict_result: (
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult
    )

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
            self.resolution_conflict_result,
            SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
        ):
            raise TypeError(
                "resolution_conflict_result must be a "
                "SecurityAdmissionCandidateByteLengthObservationResolution"
                "ConflictResult"
            )
        coverage_binding = (
            self.coverage_identity
            .evaluation_record_policy_evidence_requirements_binding
        )
        coverage_candidate_identity = (
            coverage_binding
            .evaluation_record
            .evaluation_identity
            .evaluation_basis
            .candidate_identity
        )
        conflict_candidate_identity = (
            self.resolution_conflict_result
            .resolution_basis
            .observation_set
            .candidate_identity
        )
        if coverage_candidate_identity != conflict_candidate_identity:
            raise ValueError(
                "byte-length resolution conflict must use the coverage "
                "candidate_identity"
            )
        coverage_policy_identity = (
            coverage_binding
            .policy_evidence_requirements
            .admission_policy_identity
        )
        conflict_policy_identity = (
            self.resolution_conflict_result
            .resolution_basis
            .authority_order
            .admission_policy_identity
        )
        if coverage_policy_identity != conflict_policy_identity:
            raise ValueError(
                "byte-length resolution conflict must use the coverage "
                "admission policy identity"
            )
