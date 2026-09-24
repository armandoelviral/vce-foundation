from collections.abc import Callable

from sp001.contracts.security_admission_evidence_coverage_byte_length_closure_impediment import (
    SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_closure_blockage import (
    SecurityAdmissionEvidenceCoverageClosureBlockage,
)
from sp001.contracts.security_admission_evidence_coverage_closure_resolution import (
    SecurityAdmissionEvidenceCoverageClosureResolution,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_closure_impediment import (
    SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
)
from sp001.contracts.security_admission_evidence_coverage_resolution_outcome_set import (
    SecurityAdmissionEvidenceCoverageResolutionOutcome,
    SecurityAdmissionEvidenceCoverageResolutionOutcomeSet,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)


SecurityAdmissionMediaTypeCoverageResolver = Callable[
    [SecurityAdmissionEvidenceCoverageIdentity],
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
]
SecurityAdmissionByteLengthCoverageResolver = Callable[
    [SecurityAdmissionEvidenceCoverageIdentity],
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
]


def resolve_security_admission_evidence_coverage_closure(
    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity,
    media_type_resolver: SecurityAdmissionMediaTypeCoverageResolver,
    byte_length_resolver: SecurityAdmissionByteLengthCoverageResolver,
) -> SecurityAdmissionEvidenceCoverageClosureResolution:
    """Resolve required evidence domains sequentially and stop at first impediment."""

    if not isinstance(
        coverage_identity,
        SecurityAdmissionEvidenceCoverageIdentity,
    ):
        raise TypeError(
            "coverage_identity must be a "
            "SecurityAdmissionEvidenceCoverageIdentity"
        )
    if not callable(media_type_resolver):
        raise TypeError("media_type_resolver must be callable")
    if not callable(byte_length_resolver):
        raise TypeError("byte_length_resolver must be callable")

    requirements = (
        coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
    )
    resolved_prefix: list[
        SecurityAdmissionEvidenceCoverageResolutionOutcome
    ] = []

    for domain in requirements.required_evidence_domains:
        if domain is SecurityAdmissionEvidenceDomain.MEDIA_TYPE:
            outcome = media_type_resolver(coverage_identity)
            if not isinstance(
                outcome,
                SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
            ):
                raise TypeError(
                    "media_type_resolver must return a "
                    "SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome"
                )
            impediment_type = (
                SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment
            )
        else:
            outcome = byte_length_resolver(coverage_identity)
            if not isinstance(
                outcome,
                SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
            ):
                raise TypeError(
                    "byte_length_resolver must return a "
                    "SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome"
                )
            impediment_type = (
                SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment
            )

        if outcome.coverage_identity != coverage_identity:
            raise ValueError(
                "resolved domain outcome must use the exact coverage identity"
            )

        if isinstance(outcome.outcome, impediment_type):
            blockage = SecurityAdmissionEvidenceCoverageClosureBlockage(
                coverage_identity=coverage_identity,
                resolved_prefix=tuple(resolved_prefix),
                impediment=outcome.outcome,
            )
            return SecurityAdmissionEvidenceCoverageClosureResolution(
                coverage_identity=coverage_identity,
                outcome=blockage,
            )

        resolved_prefix.append(outcome)

    outcome_set = SecurityAdmissionEvidenceCoverageResolutionOutcomeSet(
        coverage_identity=coverage_identity,
        outcomes=tuple(resolved_prefix),
    )
    closure = SecurityAdmissionEvidenceCoverageClosure(
        resolution_outcome_set=outcome_set,
    )
    return SecurityAdmissionEvidenceCoverageClosureResolution(
        coverage_identity=coverage_identity,
        outcome=closure,
    )
