from dataclasses import dataclass

from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_digest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigest,
)
from sp001.services.security_admission_evidence_coverage_closure_state_digest_verification import (
    verify_security_admission_evidence_coverage_closure_state_digest,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry:
    """Bind one terminal closure-state occurrence to its verified digest."""

    record: SecurityAdmissionEvidenceCoverageClosureStateRecord
    digest: SecurityAdmissionEvidenceCoverageClosureStateDigest

    def __post_init__(self) -> None:
        if not isinstance(
            self.record,
            SecurityAdmissionEvidenceCoverageClosureStateRecord,
        ):
            raise TypeError(
                "record must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateRecord"
            )
        if not isinstance(
            self.digest,
            SecurityAdmissionEvidenceCoverageClosureStateDigest,
        ):
            raise TypeError(
                "digest must be a "
                "SecurityAdmissionEvidenceCoverageClosureStateDigest"
            )
        if not verify_security_admission_evidence_coverage_closure_state_digest(
            record=self.record,
            digest=self.digest,
        ):
            raise ValueError(
                "digest must correspond to the exact closure-state record"
            )


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateDigestManifest:
    """Preserve one finite ordered set of verified closure-state occurrences."""

    entries: tuple[
        SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(self.entries, tuple):
            raise TypeError("entries must be an immutable tuple")
        if not self.entries:
            raise ValueError("entries must not be empty")

        seen_coverage_occurrences: set[tuple[str, int]] = set()

        for entry in self.entries:
            if not isinstance(
                entry,
                SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry,
            ):
                raise TypeError(
                    "entries must contain "
                    "SecurityAdmissionEvidenceCoverageClosureStateDigestManifestEntry "
                    "values"
                )

            coverage_identity = (
                entry.record
                .closure_resolution
                .coverage_identity
            )
            occurrence = (
                coverage_identity.coverage_id,
                coverage_identity.coverage_version,
            )

            if occurrence in seen_coverage_occurrences:
                raise ValueError(
                    "duplicate coverage occurrence: "
                    f"{coverage_identity.coverage_id} "
                    f"{coverage_identity.coverage_version}"
                )

            seen_coverage_occurrences.add(occurrence)
