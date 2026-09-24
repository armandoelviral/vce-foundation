from dataclasses import dataclass

from sp001.contracts.security_admission_assessment_status import (
    SecurityAdmissionAssessmentStatus,
)
from sp001.contracts.security_admission_candidate_byte_length_comparison_result import (
    SecurityAdmissionByteLengthComparisonStatus,
)
from sp001.contracts.security_admission_candidate_media_type_comparison_result import (
    SecurityAdmissionMediaTypeComparisonStatus,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_resolution_outcome_set import (
    SecurityAdmissionEvidenceCoverageResolutionOutcome,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceDomainAssessment:
    """Bind one closed domain outcome to its canonical assessment status."""

    coverage_closure: SecurityAdmissionEvidenceCoverageClosure
    domain: SecurityAdmissionEvidenceDomain
    resolution_outcome: SecurityAdmissionEvidenceCoverageResolutionOutcome
    status: SecurityAdmissionAssessmentStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.coverage_closure,
            SecurityAdmissionEvidenceCoverageClosure,
        ):
            raise TypeError(
                "coverage_closure must be a "
                "SecurityAdmissionEvidenceCoverageClosure"
            )
        if not isinstance(
            self.domain,
            SecurityAdmissionEvidenceDomain,
        ):
            raise TypeError(
                "domain must be a SecurityAdmissionEvidenceDomain"
            )
        if not isinstance(
            self.resolution_outcome,
            (
                SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
                SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
            ),
        ):
            raise TypeError(
                "resolution_outcome must be a "
                "SecurityAdmissionEvidenceCoverageResolutionOutcome"
            )
        if not isinstance(
            self.status,
            SecurityAdmissionAssessmentStatus,
        ):
            raise TypeError(
                "status must be a SecurityAdmissionAssessmentStatus"
            )

        closure_outcomes = (
            self.coverage_closure
            .resolution_outcome_set
            .outcomes
        )
        if not any(
            outcome is self.resolution_outcome
            for outcome in closure_outcomes
        ):
            raise ValueError(
                "resolution_outcome must be retained by coverage_closure"
            )

        if isinstance(
            self.resolution_outcome,
            SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
        ):
            if self.domain is not SecurityAdmissionEvidenceDomain.MEDIA_TYPE:
                raise ValueError(
                    "media-type resolution_outcome requires "
                    "MEDIA_TYPE domain"
                )
            expected_status = self._media_type_status()
        else:
            if self.domain is not SecurityAdmissionEvidenceDomain.BYTE_LENGTH:
                raise ValueError(
                    "byte-length resolution_outcome requires "
                    "BYTE_LENGTH domain"
                )
            expected_status = self._byte_length_status()

        if self.status is not expected_status:
            raise ValueError(
                "status must match the resolved domain outcome"
            )

    def _media_type_status(
        self,
    ) -> SecurityAdmissionAssessmentStatus:
        value = self.resolution_outcome.outcome
        if isinstance(
            value,
            SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
        ):
            return SecurityAdmissionAssessmentStatus.INDETERMINATE
        if not isinstance(
            value,
            SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
        ):
            raise ValueError(
                "media-type assessment requires a resolved "
                "conclusive or indeterminate outcome"
            )

        match_status = (
            value
            .evidence_coverage_media_type_comparison_result_binding
            .evaluation_record_media_type_comparison_result_binding
            .media_type_comparison_result_binding
            .media_type_comparison_result
            .match_status
        )
        if match_status is SecurityAdmissionMediaTypeComparisonStatus.MATCHES:
            return SecurityAdmissionAssessmentStatus.SATISFIED
        return SecurityAdmissionAssessmentStatus.NOT_SATISFIED

    def _byte_length_status(
        self,
    ) -> SecurityAdmissionAssessmentStatus:
        value = self.resolution_outcome.outcome
        if isinstance(
            value,
            SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionIndeterminateComparisonResultBinding,
        ):
            return SecurityAdmissionAssessmentStatus.INDETERMINATE
        if not isinstance(
            value,
            SecurityAdmissionEvidenceCoverageByteLengthObservationSelectionComparisonResultBinding,
        ):
            raise ValueError(
                "byte-length assessment requires a resolved "
                "conclusive or indeterminate outcome"
            )

        match_status = (
            value
            .evidence_coverage_byte_length_comparison_result_binding
            .evaluation_record_byte_length_comparison_result_binding
            .byte_length_comparison_result_binding
            .byte_length_comparison_result
            .match_status
        )
        if match_status is SecurityAdmissionByteLengthComparisonStatus.MATCHES:
            return SecurityAdmissionAssessmentStatus.SATISFIED
        return SecurityAdmissionAssessmentStatus.NOT_SATISFIED
