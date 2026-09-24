import ast
import inspect

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.services.security_admission_evidence_coverage_closure_state_payload import (
    SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING,
    canonical_security_admission_evidence_coverage_closure_state_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_projection import (
    project_security_admission_evidence_coverage_closure_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_serialization import (
    serialize_security_admission_evidence_coverage_closure_state,
)
from tests.test_security_admission_evidence_coverage_closure_resolution import (
    create_resolution,
)
from tests.test_security_admission_evidence_coverage_closure_state_record import (
    create_first_domain_blocked_resolution,
    create_second_domain_blocked_resolution,
)


Domain = SecurityAdmissionEvidenceDomain


def create_record(
    resolution_factory: object = create_resolution,
) -> SecurityAdmissionEvidenceCoverageClosureStateRecord:
    return project_security_admission_evidence_coverage_closure_state(
        resolution_factory()
    )


def payload_for(
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
) -> bytes:
    return (
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes(
            record=record
        )
    )


def test_encoding_is_explicit_utf8() -> None:
    assert (
        SECURITY_ADMISSION_EVIDENCE_COVERAGE_CLOSURE_STATE_ENCODING
        == "UTF-8"
    )


@pytest.mark.parametrize(
    "resolution_factory",
    (
        create_resolution,
        lambda: create_first_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        ),
        lambda: create_first_domain_blocked_resolution(
            Domain.BYTE_LENGTH
        ),
        lambda: create_second_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        ),
        lambda: create_second_domain_blocked_resolution(
            Domain.BYTE_LENGTH
        ),
    ),
)
def test_payload_is_exact_encoded_serialization(
    resolution_factory: object,
) -> None:
    record = create_record(resolution_factory)
    serialized = (
        serialize_security_admission_evidence_coverage_closure_state(
            record=record
        )
    )
    assert payload_for(record) == serialized.encode("UTF-8")


@pytest.mark.parametrize(
    "resolution_factory",
    (
        create_resolution,
        lambda: create_first_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        ),
        lambda: create_second_domain_blocked_resolution(
            Domain.BYTE_LENGTH
        ),
    ),
)
def test_payload_is_deterministic(
    resolution_factory: object,
) -> None:
    record = create_record(resolution_factory)
    first = payload_for(record)
    second = payload_for(record)
    assert first == second
    assert isinstance(first, bytes)


def test_payload_adds_no_bom_newline_or_delimiter() -> None:
    record = create_record()
    serialized = (
        serialize_security_admission_evidence_coverage_closure_state(
            record=record
        )
    )
    payload = payload_for(record)
    assert not payload.startswith(b"\xef\xbb\xbf")
    assert not payload.endswith(b"\n")
    assert payload.decode("UTF-8") == serialized


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_record_requires_nominal_type(invalid_value: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        ),
    ):
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes(
            record=invalid_value  # type: ignore[arg-type]
        )


def test_payload_accepts_only_keyword_record() -> None:
    signature = inspect.signature(
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes
    )
    assert tuple(signature.parameters) == ("record",)
    assert signature.parameters["record"].kind is inspect.Parameter.KEYWORD_ONLY


def test_payload_has_no_storage_digest_or_replay_capability() -> None:
    source = inspect.getsource(
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes
    )
    forbidden = (
        "open(",
        "write",
        "hashlib",
        "digest",
        "resolver",
        "replay",
        "subprocess",
        "socket",
    )
    assert all(token not in source for token in forbidden)


def test_service_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"sp001"}
