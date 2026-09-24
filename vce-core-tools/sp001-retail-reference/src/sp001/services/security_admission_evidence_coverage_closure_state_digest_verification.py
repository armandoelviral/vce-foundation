import hmac
import re

from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_digest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigest,
    digest_security_admission_evidence_coverage_closure_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_payload import (
    SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING,
)


def verify_security_admission_evidence_coverage_closure_state_digest(
    *,
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
    digest: SecurityAdmissionEvidenceCoverageClosureStateDigest,
) -> bool:
    """Verify closure-state content correspondence without authenticity claims."""

    if not isinstance(
        record,
        SecurityAdmissionEvidenceCoverageClosureStateRecord,
    ):
        raise TypeError(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        )
    if not isinstance(
        digest,
        SecurityAdmissionEvidenceCoverageClosureStateDigest,
    ):
        raise TypeError(
            "digest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigest"
        )
    if digest.algorithm != "SHA-256":
        raise ValueError("digest algorithm must be SHA-256")
    if (
        digest.encoding
        != SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING
    ):
        raise ValueError("digest encoding must be UTF-8")
    if (
        not isinstance(digest.value, str)
        or re.fullmatch(
            r"[0-9a-f]{64}",
            digest.value,
        )
        is None
    ):
        raise ValueError(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        )

    expected = (
        digest_security_admission_evidence_coverage_closure_state(
            record=record,
        )
    )
    return hmac.compare_digest(
        expected.value,
        digest.value,
    )
