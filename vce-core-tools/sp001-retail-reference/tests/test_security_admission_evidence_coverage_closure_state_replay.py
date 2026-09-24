import ast
import inspect
import json

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.services.security_admission_evidence_coverage_closure_state_payload import (
    canonical_security_admission_evidence_coverage_closure_state_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_projection import (
    project_security_admission_evidence_coverage_closure_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_replay import (
    replay_security_admission_evidence_coverage_closure_state,
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
def test_exact_payload_replays_canonical_state(
    resolution_factory: object,
) -> None:
    original = create_record(resolution_factory)
    replayed = (
        replay_security_admission_evidence_coverage_closure_state(
            payload=payload_for(original),
            closure_resolution=original.closure_resolution,
        )
    )
    assert replayed == original
    assert replayed is not original
    assert replayed.closure_resolution is original.closure_resolution


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
def test_replay_is_deterministic(
    resolution_factory: object,
) -> None:
    original = create_record(resolution_factory)
    payload = payload_for(original)
    first = replay_security_admission_evidence_coverage_closure_state(
        payload=payload,
        closure_resolution=original.closure_resolution,
    )
    second = replay_security_admission_evidence_coverage_closure_state(
        payload=payload,
        closure_resolution=original.closure_resolution,
    )
    assert first == second
    assert first.domain_states == second.domain_states


@pytest.mark.parametrize(
    "invalid_value",
    (None, 1, True, "payload", bytearray()),
)
def test_payload_requires_exact_bytes(invalid_value: object) -> None:
    resolution = create_resolution()
    with pytest.raises(
        TypeError,
        match="payload must be bytes",
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=invalid_value,  # type: ignore[arg-type]
            closure_resolution=resolution,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_closure_resolution_requires_nominal_type(
    invalid_value: object,
) -> None:
    record = create_record()
    with pytest.raises(
        TypeError,
        match=(
            "closure_resolution must be a "
            "SecurityAdmissionEvidenceCoverageClosureResolution"
        ),
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=payload_for(record),
            closure_resolution=invalid_value,  # type: ignore[arg-type]
        )


def test_invalid_utf8_is_rejected() -> None:
    resolution = create_resolution()
    with pytest.raises(
        ValueError,
        match="payload must contain valid UTF-8",
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=b"\xff",
            closure_resolution=resolution,
        )


@pytest.mark.parametrize(
    "payload",
    (
        b"",
        b"{",
        b"not-json",
    ),
)
def test_invalid_json_is_rejected(payload: bytes) -> None:
    resolution = create_resolution()
    with pytest.raises(
        ValueError,
        match="payload must contain valid JSON",
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=payload,
            closure_resolution=resolution,
        )


@pytest.mark.parametrize(
    "payload",
    (
        b"null",
        b"[]",
        b"true",
        b"1",
        b"\"text\"",
    ),
)
def test_nonobject_json_is_rejected(payload: bytes) -> None:
    resolution = create_resolution()
    with pytest.raises(
        ValueError,
        match="payload document must be a JSON object",
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=payload,
            closure_resolution=resolution,
        )


@pytest.mark.parametrize(
    "document",
    (
        {},
        {"schema_version": 0},
        {"schema_version": 2},
        {"schema_version": "1"},
    ),
)
def test_unsupported_schema_is_rejected(
    document: dict[str, object],
) -> None:
    resolution = create_resolution()
    payload = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("UTF-8")
    with pytest.raises(
        ValueError,
        match="payload schema_version must be supported",
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=payload,
            closure_resolution=resolution,
        )


def test_changed_not_evaluated_state_is_rejected() -> None:
    record = create_record(
        lambda: create_first_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        )
    )
    document = json.loads(payload_for(record))
    document["domain_states"][1]["status"] = "RESOLVED"
    tampered = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("UTF-8")

    with pytest.raises(
        ValueError,
        match=(
            "payload must exactly match "
            "the recovered closure resolution"
        ),
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=tampered,
            closure_resolution=record.closure_resolution,
        )


def test_payload_for_different_terminal_is_rejected() -> None:
    closed = create_record()
    blocked = create_record(
        lambda: create_first_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        )
    )
    with pytest.raises(
        ValueError,
        match=(
            "payload must exactly match "
            "the recovered closure resolution"
        ),
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=payload_for(closed),
            closure_resolution=blocked.closure_resolution,
        )


def test_noncanonical_equivalent_json_is_rejected() -> None:
    record = create_record()
    document = json.loads(payload_for(record))
    noncanonical = json.dumps(
        document,
        sort_keys=False,
        indent=2,
        ensure_ascii=False,
    ).encode("UTF-8")
    assert json.loads(noncanonical) == document

    with pytest.raises(
        ValueError,
        match=(
            "payload must exactly match "
            "the recovered closure resolution"
        ),
    ):
        replay_security_admission_evidence_coverage_closure_state(
            payload=noncanonical,
            closure_resolution=record.closure_resolution,
        )


def test_replay_accepts_no_resolvers() -> None:
    signature = inspect.signature(
        replay_security_admission_evidence_coverage_closure_state
    )
    assert tuple(signature.parameters) == (
        "payload",
        "closure_resolution",
    )
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


def test_replay_uses_constant_time_payload_comparison() -> None:
    module = inspect.getmodule(
        replay_security_admission_evidence_coverage_closure_state
    )
    assert module is not None
    assert "hmac.compare_digest" in inspect.getsource(module)


def test_replay_does_not_execute_or_decide() -> None:
    source = inspect.getsource(
        replay_security_admission_evidence_coverage_closure_state
    )
    forbidden = (
        "assessment",
        "classification",
        "admission_decision",
        "rejection",
        "authority",
    )
    assert all(token not in source for token in forbidden)


def test_service_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        replay_security_admission_evidence_coverage_closure_state
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    imports = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert roots == {"sp001"}
    assert imports == {"hmac", "json"}
