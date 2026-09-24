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
from sp001.contracts.security_admission_evidence_domain_assessment import (
    SecurityAdmissionEvidenceDomainAssessment,
)
from sp001.contracts.security_admission_evidence_domain_assessment_set import (
    SecurityAdmissionEvidenceDomainAssessmentSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)


def project_security_admission_evidence_domain_assessment_set(
    coverage_closure: SecurityAdmissionEvidenceCoverageClosure,
) -> SecurityAdmissionEvidenceDomainAssessmentSet:
    """Project one complete closure into exhaustive policy-ordered assessments."""

    if not isinstance(
        coverage_closure,
        SecurityAdmissionEvidenceCoverageClosure,
    ):
        raise TypeError(
            "coverage_closure must be a "
            "SecurityAdmissionEvidenceCoverageClosure"
        )

    outcome_set = coverage_closure.resolution_outcome_set
    required_domains = (
        outcome_set.coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
        .required_evidence_domains
    )
    assessments: list[
        SecurityAdmissionEvidenceDomainAssessment
    ] = []

    for domain, resolution_outcome in zip(
        required_domains,
        outcome_set.outcomes,
    ):
        if domain is SecurityAdmissionEvidenceDomain.MEDIA_TYPE:
            status = _media_type_status(resolution_outcome)
        else:
            status = _byte_length_status(resolution_outcome)

        assessments.append(
            SecurityAdmissionEvidenceDomainAssessment(
                coverage_closure=coverage_closure,
                domain=domain,
                resolution_outcome=resolution_outcome,
                status=status,
            )
        )

    return SecurityAdmissionEvidenceDomainAssessmentSet(
        coverage_closure=coverage_closure,
        assessments=tuple(assessments),
    )


def _media_type_status(
    resolution_outcome: object,
) -> SecurityAdmissionAssessmentStatus:
    if not isinstance(
        resolution_outcome,
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
    ):
        raise ValueError(
            "MEDIA_TYPE domain requires a media-type resolution outcome"
        )

    value = resolution_outcome.outcome
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
    resolution_outcome: object,
) -> SecurityAdmissionAssessmentStatus:
    if not isinstance(
        resolution_outcome,
        SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
    ):
        raise ValueError(
            "BYTE_LENGTH domain requires a byte-length resolution outcome"
        )

    value = resolution_outcome.outcome
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
