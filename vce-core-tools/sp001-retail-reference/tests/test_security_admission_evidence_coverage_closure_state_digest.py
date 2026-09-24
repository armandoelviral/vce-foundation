import ast
import hashlib
import inspect
import re
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from sp001.services.security_admission_evidence_coverage_closure_state_digest import (
    SecurityAdmissionEvidenceCoverageClosureStateDigest,
    digest_security_admission_evidence_coverage_closure_state,
)
from sp001.services.security_admission_evidence_coverage_closure_state_payload import (
    canonical_security_admission_evidence_coverage_closure_state_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_projection import (
    project_security_admission_evidence_coverage_closure_state,
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


def digest_record(
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
) -> SecurityAdmissionEvidenceCoverageClosureStateDigest:
    return digest_security_admission_evidence_coverage_closure_state(
        record=record
    )


def test_digest_fields_are_exact() -> None:
    digest_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateDigest
    )
    assert tuple(field.name for field in digest_fields) == (
        "algorithm",
        "encoding",
        "value",
    )
    assert all(field.type is str for field in digest_fields)


def test_digest_is_immutable_and_slotted() -> None:
    digest = digest_record(create_record())
    assert not hasattr(digest, "__dict__")
    with pytest.raises(FrozenInstanceError):
        digest.value = "0" * 64  # type: ignore[misc]


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
def test_digest_matches_exact_canonical_payload(
    resolution_factory: object,
) -> None:
    record = create_record(resolution_factory)
    payload = (
        canonical_security_admission_evidence_coverage_closure_state_payload_bytes(
            record=record
        )
    )
    digest = digest_record(record)
    assert digest.algorithm == "SHA-256"
    assert digest.encoding == "UTF-8"
    assert digest.value == hashlib.sha256(payload).hexdigest()
    assert re.fullmatch(r"[0-9a-f]{64}", digest.value)


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
def test_digest_is_deterministic(
    resolution_factory: object,
) -> None:
    record = create_record(resolution_factory)
    assert digest_record(record) == digest_record(record)


def test_distinct_terminal_states_have_distinct_digests() -> None:
    closed = digest_record(create_record())
    blocked = digest_record(
        create_record(
            lambda: create_first_domain_blocked_resolution(
                Domain.MEDIA_TYPE
            )
        )
    )
    assert closed.value != blocked.value


def test_distinct_policy_orders_have_distinct_digests() -> None:
    media_first = digest_record(
        create_record(
            lambda: create_first_domain_blocked_resolution(
                Domain.MEDIA_TYPE
            )
        )
    )
    byte_first = digest_record(
        create_record(
            lambda: create_first_domain_blocked_resolution(
                Domain.BYTE_LENGTH
            )
        )
    )
    assert media_first.value != byte_first.value


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_record_requires_nominal_type(invalid_value: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        ),
    ):
        digest_security_admission_evidence_coverage_closure_state(
            record=invalid_value  # type: ignore[arg-type]
        )


def test_digest_makes_no_authenticity_or_authority_claim() -> None:
    digest = digest_record(create_record())
    for field_name in (
        "signature",
        "signer",
        "authority",
        "authorization",
        "admission_decision",
    ):
        assert not hasattr(digest, field_name)


def test_digest_accepts_only_keyword_record() -> None:
    signature = inspect.signature(
        digest_security_admission_evidence_coverage_closure_state
    )
    assert tuple(signature.parameters) == ("record",)
    assert signature.parameters["record"].kind is inspect.Parameter.KEYWORD_ONLY


def test_service_imports_only_hashing_and_local_contracts() -> None:
    module = inspect.getmodule(
        digest_security_admission_evidence_coverage_closure_state
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
    assert roots == {"dataclasses", "sp001"}
    assert imports == {"hashlib"}
