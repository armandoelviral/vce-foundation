import hmac
import json

from sp001.contracts.security_admission_evidence_coverage_closure_resolution import (
    SecurityAdmissionEvidenceCoverageClosureResolution,
)
from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.services.security_admission_evidence_coverage_closure_state_payload import (
    SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING,
    canonical_security_admission_evidence_coverage_closure_state_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_projection import (
    project_security_admission_evidence_coverage_closure_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_serialization import (
    SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_SCHEMA_VERSION,
)


def replay_security_admission_evidence_coverage_closure_state(
    *,
    payload: bytes,
    closure_resolution: SecurityAdmissionEvidenceCoverageClosureResolution,
) -> SecurityAdmissionEvidenceCoverageClosureStateRecord:
    """Replay canonical closure state without executing domain resolvers."""

    if not isinstance(payload, bytes):
        raise TypeError("payload must be bytes")
    if not isinstance(
        closure_resolution,
        SecurityAdmissionEvidenceCoverageClosureResolution,
    ):
        raise TypeError(
            "closure_resolution must be a "
            "SecurityAdmissionEvidenceCoverageClosureResolution"
        )

    try:
        payload_text = payload.decode(
            SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING
        )
    except UnicodeDecodeError as error:
        raise ValueError(
            "payload must contain valid UTF-8"
        ) from error

    try:
        document = json.loads(payload_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            "payload must contain valid JSON"
        ) from error

    if not isinstance(document, dict):
        raise ValueError(
            "payload document must be a JSON object"
        )
    if (
        document.get("schema_version")
        != SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_SCHEMA_VERSION
    ):
        raise ValueError(
            "payload schema_version must be supported"
        )

    record = (
        project_security_admission_evidence_coverage_closure_state(
            closure_resolution
        )
    )
    expected_payload = (
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes(
            record=record
        )
    )
    if not hmac.compare_digest(
        expected_payload,
        payload,
    ):
        raise ValueError(
            "payload must exactly match the recovered closure resolution"
        )

    return record
