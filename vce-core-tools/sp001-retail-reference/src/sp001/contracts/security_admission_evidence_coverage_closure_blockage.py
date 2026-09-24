from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_byte_length_closure_impediment import (
    SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
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
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)


SecurityAdmissionEvidenceCoverageClosureImpediment = (
    SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment
    | SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureBlockage:
    """Stop coverage at the first impeded required evidence domain."""

    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity
    resolved_prefix: tuple[
        SecurityAdmissionEvidenceCoverageResolutionOutcome,
        ...,
    ]
    impediment: SecurityAdmissionEvidenceCoverageClosureImpediment

    def __post_init__(self) -> None:
        if not isinstance(
            self.coverage_identity,
            SecurityAdmissionEvidenceCoverageIdentity,
        ):
            raise TypeError(
                "coverage_identity must be a "
                "SecurityAdmissionEvidenceCoverageIdentity"
            )
        if not isinstance(self.resolved_prefix, tuple):
            raise TypeError(
                "resolved_prefix must be an immutable tuple"
            )
        if not isinstance(
            self.impediment,
            (
                SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
                SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
            ),
        ):
            raise TypeError(
                "impediment must be a media-type or byte-length "
                "closure impediment"
            )

        required_domains = (
            self.coverage_identity
            .evaluation_record_policy_evidence_requirements_binding
            .policy_evidence_requirements
            .required_evidence_domains
        )

        if len(self.resolved_prefix) >= len(required_domains):
            raise ValueError(
                "closure blockage must occur before all required "
                "domains resolve"
            )

        actual_prefix_domains: list[
            SecurityAdmissionEvidenceDomain
        ] = []
        for outcome in self.resolved_prefix:
            if isinstance(
                outcome,
                SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
            ):
                domain = SecurityAdmissionEvidenceDomain.MEDIA_TYPE
            elif isinstance(
                outcome,
                SecurityAdmissionEvidenceCoverageByteLengthResolutionOutcome,
            ):
                domain = SecurityAdmissionEvidenceDomain.BYTE_LENGTH
            else:
                raise TypeError(
                    "resolved_prefix must contain media-type or "
                    "byte-length resolution outcomes"
                )

            if isinstance(
                outcome.outcome,
                (
                    SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
                    SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
                ),
            ):
                raise ValueError(
                    "resolved_prefix must contain only resolved "
                    "conclusive or indeterminate outcomes"
                )
            if outcome.coverage_identity != self.coverage_identity:
                raise ValueError(
                    "each resolved prefix outcome must use the "
                    "coverage identity"
                )

            actual_prefix_domains.append(domain)

        expected_prefix_domains = required_domains[
            : len(self.resolved_prefix)
        ]
        if tuple(actual_prefix_domains) != expected_prefix_domains:
            raise ValueError(
                "resolved_prefix domains must exactly match the "
                "required evidence domain prefix"
            )

        if self.impediment.coverage_identity != self.coverage_identity:
            raise ValueError(
                "impediment must use the coverage identity"
            )

        if isinstance(
            self.impediment,
            SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
        ):
            impeded_domain = SecurityAdmissionEvidenceDomain.MEDIA_TYPE
        else:
            impeded_domain = SecurityAdmissionEvidenceDomain.BYTE_LENGTH

        expected_impeded_domain = required_domains[
            len(self.resolved_prefix)
        ]
        if impeded_domain is not expected_impeded_domain:
            raise ValueError(
                "impediment must target the first unresolved "
                "required evidence domain"
            )
