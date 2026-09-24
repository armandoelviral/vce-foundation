from dataclasses import dataclass

import hashlib

from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_payload import (
    SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING,
    canonical_security_admission_evidence_coverage_closure_state_payload_bytes,
)


@dataclass(frozen=True, slots=True)
class SecurityAdmissionEvidenceCoverageClosureStateDigest:
    """Immutable closure-state content identity without authenticity claims."""

    algorithm: str
    encoding: str
    value: str


def digest_security_admission_evidence_coverage_closure_state(
    *,
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
) -> SecurityAdmissionEvidenceCoverageClosureStateDigest:
    """Digest exact canonical coverage-closure state payload bytes."""

    if not isinstance(
        record,
        SecurityAdmissionEvidenceCoverageClosureStateRecord,
    ):
        raise TypeError(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        )

    payload_bytes = (
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes(
            record=record,
        )
    )
    value = hashlib.sha256(payload_bytes).hexdigest()

    return SecurityAdmissionEvidenceCoverageClosureStateDigest(
        algorithm="SHA-256",
        encoding=(
            SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING
        ),
        value=value,
    )
