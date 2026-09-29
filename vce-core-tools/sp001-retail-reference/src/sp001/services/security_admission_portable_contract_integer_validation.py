from sp001.contracts.security_admission_candidate_byte_length_comparison_basis import (
    SecurityAdmissionCandidateByteLengthComparisonBasis,
)
from sp001.contracts.security_admission_candidate_byte_length_comparison_result import (
    SecurityAdmissionCandidateByteLengthComparisonResult,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_conflict_result import (
    SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_result import (
    SecurityAdmissionCandidateByteLengthObservationSelectionResult,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_set import (
    SecurityAdmissionCandidateByteLengthObservationSet,
)
from sp001.contracts.security_admission_candidate_declared_byte_length import (
    SecurityAdmissionCandidateDeclaredByteLength,
)
from sp001.contracts.security_admission_candidate_detected_media_type_observation import (
    SecurityAdmissionCandidateDetectedMediaTypeObservation,
)
from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_candidate_indeterminate_byte_length_comparison_result import (
    SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult,
)
from sp001.contracts.security_admission_candidate_indeterminate_media_type_comparison_result import (
    SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResult,
)
from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
)
from sp001.contracts.security_admission_candidate_media_type_comparison_basis import (
    SecurityAdmissionCandidateMediaTypeComparisonBasis,
)
from sp001.contracts.security_admission_candidate_media_type_comparison_result import (
    SecurityAdmissionCandidateMediaTypeComparisonResult,
)
from sp001.contracts.security_admission_candidate_media_type_observation_resolution_conflict_result import (
    SecurityAdmissionCandidateMediaTypeObservationResolutionConflictResult,
)
from sp001.contracts.security_admission_candidate_media_type_observation_selection_result import (
    SecurityAdmissionCandidateMediaTypeObservationSelectionResult,
)
from sp001.contracts.security_admission_candidate_media_type_observation_set import (
    SecurityAdmissionCandidateMediaTypeObservationSet,
)
from sp001.contracts.security_admission_candidate_metadata_identity import (
    SecurityAdmissionCandidateMetadataIdentity,
)
from sp001.contracts.security_admission_evaluation_identity import (
    SecurityAdmissionEvaluationIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)
from sp001.services.security_admission_portable_integer_validation import (
    validate_security_admission_non_negative_uint64,
    validate_security_admission_positive_uint64,
)


def validate_security_admission_portable_contract_integers(
    *,
    value: object,
) -> None:
    """Validate direct integer fields before a portable ABI transition."""

    if isinstance(
        value,
        (
            SecurityAdmissionCandidateByteLengthComparisonBasis,
            SecurityAdmissionCandidateMediaTypeComparisonBasis,
        ),
    ):
        validate_security_admission_positive_uint64(
            value=value.comparison_scheme_version,
            field="comparison_scheme_version",
        )
        return

    if isinstance(
        value,
        (
            SecurityAdmissionCandidateByteLengthComparisonResult,
            SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
            SecurityAdmissionCandidateByteLengthObservationSelectionResult,
            SecurityAdmissionCandidateIndeterminateByteLengthComparisonResult,
            SecurityAdmissionCandidateIndeterminateMediaTypeComparisonResult,
            SecurityAdmissionCandidateMediaTypeComparisonResult,
            SecurityAdmissionCandidateMediaTypeObservationResolutionConflictResult,
            SecurityAdmissionCandidateMediaTypeObservationSelectionResult,
        ),
    ):
        validate_security_admission_positive_uint64(
            value=value.result_version,
            field="result_version",
        )
        return

    if isinstance(
        value,
        (
            SecurityAdmissionCandidateByteLengthObservationSet,
            SecurityAdmissionCandidateMediaTypeObservationSet,
        ),
    ):
        validate_security_admission_positive_uint64(
            value=value.observation_set_version,
            field="observation_set_version",
        )
        return

    if isinstance(
        value,
        SecurityAdmissionCandidateDetectedMediaTypeObservation,
    ):
        validate_security_admission_positive_uint64(
            value=value.observation_version,
            field="observation_version",
        )
        return

    if isinstance(
        value,
        SecurityAdmissionCandidateMeasuredByteLengthObservation,
    ):
        validate_security_admission_positive_uint64(
            value=value.observation_version,
            field="observation_version",
        )
        validate_security_admission_non_negative_uint64(
            value=value.measured_byte_length,
            field="measured_byte_length",
        )
        return

    if isinstance(
        value,
        SecurityAdmissionCandidateDeclaredByteLength,
    ):
        validate_security_admission_non_negative_uint64(
            value=value.declared_byte_length,
            field="declared_byte_length",
        )
        return

    if isinstance(value, SecurityAdmissionCandidateIdentity):
        validate_security_admission_positive_uint64(
            value=value.candidate_version,
            field="candidate_version",
        )
        return

    if isinstance(value, SecurityAdmissionCandidateMetadataIdentity):
        validate_security_admission_positive_uint64(
            value=value.metadata_schema_version,
            field="metadata_schema_version",
        )
        return

    if isinstance(value, SecurityAdmissionEvaluationIdentity):
        validate_security_admission_positive_uint64(
            value=value.evaluation_version,
            field="evaluation_version",
        )
        return

    if isinstance(value, SecurityAdmissionEvidenceCoverageIdentity):
        validate_security_admission_positive_uint64(
            value=value.coverage_version,
            field="coverage_version",
        )
        return

    if isinstance(value, SecurityAdmissionPolicyIdentity):
        validate_security_admission_positive_uint64(
            value=value.admission_policy_version,
            field="admission_policy_version",
        )
        return

    raise TypeError(
        "value must be a supported security-admission "
        "integer-bearing contract"
    )
