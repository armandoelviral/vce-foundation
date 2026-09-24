from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_serialization import (
    serialize_security_admission_evidence_coverage_closure_state,
)


SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING = "UTF-8"


def canonical_security_admission_evidence_coverage_closure_state_payload_bytes(
    *,
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
) -> bytes:
    """Return exact canonical coverage-closure state payload bytes."""

    if not isinstance(
        record,
        SecurityAdmissionEvidenceCoverageClosureStateRecord,
    ):
        raise TypeError(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        )

    payload = (
        serialize_security_admission_evidence_coverage_closure_state(
            record=record,
        )
    )
    return payload.encode(
        SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING
    )
