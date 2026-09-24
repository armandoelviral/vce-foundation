import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_evidence_coverage_domain_closure_state import (
    SecurityAdmissionEvidenceCoverageDomainClosureState,
    SecurityAdmissionEvidenceCoverageDomainClosureStatus,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)


Domain = SecurityAdmissionEvidenceDomain
Status = SecurityAdmissionEvidenceCoverageDomainClosureStatus


def create_state(
    domain: Domain = Domain.MEDIA_TYPE,
    status: Status = Status.RESOLVED,
) -> SecurityAdmissionEvidenceCoverageDomainClosureState:
    return SecurityAdmissionEvidenceCoverageDomainClosureState(
        domain=domain,
        status=status,
    )


def test_status_vocabulary_is_exact_and_closed() -> None:
    assert tuple(Status) == (
        Status.RESOLVED,
        Status.IMPEDED,
        Status.NOT_EVALUATED,
    )
    assert tuple(status.value for status in Status) == (
        "RESOLVED",
        "IMPEDED",
        "NOT_EVALUATED",
    )


@pytest.mark.parametrize(
    "status",
    (
        Status.RESOLVED,
        Status.IMPEDED,
        Status.NOT_EVALUATED,
    ),
)
def test_each_status_preserves_string_value(status: Status) -> None:
    assert str(status) == status.value


def test_fields_are_exact() -> None:
    state_fields = fields(
        SecurityAdmissionEvidenceCoverageDomainClosureState
    )
    assert tuple(field.name for field in state_fields) == (
        "domain",
        "status",
    )
    assert state_fields[0].type is SecurityAdmissionEvidenceDomain
    assert (
        state_fields[1].type
        is SecurityAdmissionEvidenceCoverageDomainClosureStatus
    )


def test_state_is_immutable_and_slotted() -> None:
    state = create_state()
    assert not hasattr(state, "__dict__")
    with pytest.raises(FrozenInstanceError):
        state.status = Status.IMPEDED  # type: ignore[misc]


@pytest.mark.parametrize(
    ("domain", "status"),
    (
        (Domain.MEDIA_TYPE, Status.RESOLVED),
        (Domain.MEDIA_TYPE, Status.IMPEDED),
        (Domain.MEDIA_TYPE, Status.NOT_EVALUATED),
        (Domain.BYTE_LENGTH, Status.RESOLVED),
        (Domain.BYTE_LENGTH, Status.IMPEDED),
        (Domain.BYTE_LENGTH, Status.NOT_EVALUATED),
    ),
)
def test_each_domain_status_pair_is_preserved(
    domain: Domain,
    status: Status,
) -> None:
    state = create_state(domain, status)
    assert state.domain is domain
    assert state.status is status


def test_equal_reconstruction_has_value_equality() -> None:
    state = create_state(
        Domain.BYTE_LENGTH,
        Status.NOT_EVALUATED,
    )
    reconstructed = replace(state)
    assert reconstructed == state
    assert reconstructed is not state


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_domain_requires_nominal_type(invalid_value: object) -> None:
    with pytest.raises(
        TypeError,
        match="domain must be a SecurityAdmissionEvidenceDomain",
    ):
        SecurityAdmissionEvidenceCoverageDomainClosureState(
            domain=invalid_value,  # type: ignore[arg-type]
            status=Status.RESOLVED,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_status_requires_nominal_type(invalid_value: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "status must be a "
            "SecurityAdmissionEvidenceCoverageDomainClosureStatus"
        ),
    ):
        SecurityAdmissionEvidenceCoverageDomainClosureState(
            domain=Domain.MEDIA_TYPE,
            status=invalid_value,  # type: ignore[arg-type]
        )


def test_status_is_not_assessment_or_decision_vocabulary() -> None:
    forbidden_values = {
        "SATISFIED",
        "NOT_SATISFIED",
        "REJECTED",
        "ADMITTED",
        "AUTHORIZED",
    }
    assert forbidden_values.isdisjoint(
        status.value for status in Status
    )


def test_post_coverage_fields_are_absent() -> None:
    state = create_state()
    for field_name in (
        "assessment",
        "classification",
        "admission_status",
        "admission_decision",
        "rejection",
        "authority",
    ):
        assert not hasattr(state, field_name)


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageDomainClosureState
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions == {"__post_init__"}


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageDomainClosureState
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "enum", "sp001"}
