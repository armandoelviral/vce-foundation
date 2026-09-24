import ast
import inspect
from dataclasses import replace

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
from sp001.services.security_admission_evidence_coverage_closure_state_digest_verification import (
    verify_security_admission_evidence_coverage_closure_state_digest,
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


def create_digest(
    record: SecurityAdmissionEvidenceCoverageClosureStateRecord,
) -> SecurityAdmissionEvidenceCoverageClosureStateDigest:
    return digest_security_admission_evidence_coverage_closure_state(
        record=record
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
def test_exact_digest_verifies(
    resolution_factory: object,
) -> None:
    record = create_record(resolution_factory)
    digest = create_digest(record)
    assert verify_security_admission_evidence_coverage_closure_state_digest(
        record=record,
        digest=digest,
    )


def test_different_terminal_state_returns_false() -> None:
    closed_record = create_record()
    blocked_record = create_record(
        lambda: create_first_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        )
    )
    digest = create_digest(closed_record)
    assert not verify_security_admission_evidence_coverage_closure_state_digest(
        record=blocked_record,
        digest=digest,
    )


def test_different_normative_order_returns_false() -> None:
    media_first = create_record(
        lambda: create_first_domain_blocked_resolution(
            Domain.MEDIA_TYPE
        )
    )
    byte_first = create_record(
        lambda: create_first_domain_blocked_resolution(
            Domain.BYTE_LENGTH
        )
    )
    digest = create_digest(media_first)
    assert not verify_security_admission_evidence_coverage_closure_state_digest(
        record=byte_first,
        digest=digest,
    )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_record_requires_nominal_type(invalid_value: object) -> None:
    record = create_record()
    digest = create_digest(record)
    with pytest.raises(
        TypeError,
        match=(
            "record must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateRecord"
        ),
    ):
        verify_security_admission_evidence_coverage_closure_state_digest(
            record=invalid_value,  # type: ignore[arg-type]
            digest=digest,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_digest_requires_nominal_type(invalid_value: object) -> None:
    record = create_record()
    with pytest.raises(
        TypeError,
        match=(
            "digest must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateDigest"
        ),
    ):
        verify_security_admission_evidence_coverage_closure_state_digest(
            record=record,
            digest=invalid_value,  # type: ignore[arg-type]
        )


def test_unsupported_algorithm_is_rejected() -> None:
    record = create_record()
    digest = replace(
        create_digest(record),
        algorithm="SHA-512",
    )
    with pytest.raises(
        ValueError,
        match="digest algorithm must be SHA-256",
    ):
        verify_security_admission_evidence_coverage_closure_state_digest(
            record=record,
            digest=digest,
        )


def test_unsupported_encoding_is_rejected() -> None:
    record = create_record()
    digest = replace(
        create_digest(record),
        encoding="UTF-16",
    )
    with pytest.raises(
        ValueError,
        match="digest encoding must be UTF-8",
    ):
        verify_security_admission_evidence_coverage_closure_state_digest(
            record=record,
            digest=digest,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "",
        "0" * 63,
        "0" * 65,
        "G" * 64,
        "A" * 64,
    ),
)
def test_malformed_digest_value_is_rejected(
    invalid_value: object,
) -> None:
    record = create_record()
    digest = replace(
        create_digest(record),
        value=invalid_value,  # type: ignore[arg-type]
    )
    with pytest.raises(
        ValueError,
        match=(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        ),
    ):
        verify_security_admission_evidence_coverage_closure_state_digest(
            record=record,
            digest=digest,
        )


def test_well_formed_but_incorrect_digest_returns_false() -> None:
    record = create_record()
    digest = replace(
        create_digest(record),
        value="0" * 64,
    )
    assert not verify_security_admission_evidence_coverage_closure_state_digest(
        record=record,
        digest=digest,
    )


def test_verification_uses_constant_time_comparison() -> None:
    module = inspect.getmodule(
        verify_security_admission_evidence_coverage_closure_state_digest
    )
    assert module is not None
    source = inspect.getsource(module)
    assert "hmac.compare_digest" in source


def test_verification_has_no_authenticity_or_authority_semantics() -> None:
    source = inspect.getsource(
        verify_security_admission_evidence_coverage_closure_state_digest
    )
    forbidden = (
        "signature",
        "signer",
        "authorization",
        "admission_decision",
        "resolver",
        "replay",
    )
    assert all(token not in source for token in forbidden)


def test_service_imports_only_verification_dependencies() -> None:
    module = inspect.getmodule(
        verify_security_admission_evidence_coverage_closure_state_digest
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
    assert imports == {"hmac", "re"}
