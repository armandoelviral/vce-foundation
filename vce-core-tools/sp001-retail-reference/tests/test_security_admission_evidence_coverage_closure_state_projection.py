import ast
import inspect

import pytest

from sp001.contracts.security_admission_evidence_coverage_domain_closure_state import (
    SecurityAdmissionEvidenceCoverageDomainClosureStatus,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
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
Status = SecurityAdmissionEvidenceCoverageDomainClosureStatus


def statuses_of(record: object) -> tuple[Status, ...]:
    return tuple(
        state.status
        for state in record.domain_states
    )


def domains_of(record: object) -> tuple[Domain, ...]:
    return tuple(
        state.domain
        for state in record.domain_states
    )


def required_domains_of(resolution: object) -> tuple[Domain, ...]:
    return (
        resolution
        .coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
        .required_evidence_domains
    )


def test_complete_closure_projects_every_domain_as_resolved() -> None:
    resolution = create_resolution()
    record = (
        project_security_admission_evidence_coverage_closure_state(
            resolution
        )
    )
    assert record.closure_resolution is resolution
    assert statuses_of(record) == (
        Status.RESOLVED,
    ) * len(record.domain_states)


@pytest.mark.parametrize(
    "first_domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_first_impediment_projects_unevaluated_suffix(
    first_domain: Domain,
) -> None:
    resolution = create_first_domain_blocked_resolution(
        first_domain
    )
    record = (
        project_security_admission_evidence_coverage_closure_state(
            resolution
        )
    )
    assert record.closure_resolution is resolution
    assert statuses_of(record) == (
        Status.IMPEDED,
        Status.NOT_EVALUATED,
    )


@pytest.mark.parametrize(
    "first_domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_second_impediment_projects_resolved_prefix(
    first_domain: Domain,
) -> None:
    resolution = create_second_domain_blocked_resolution(
        first_domain
    )
    record = (
        project_security_admission_evidence_coverage_closure_state(
            resolution
        )
    )
    assert record.closure_resolution is resolution
    assert statuses_of(record) == (
        Status.RESOLVED,
        Status.IMPEDED,
    )


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
def test_projection_preserves_required_domain_order(
    resolution_factory: object,
) -> None:
    resolution = resolution_factory()
    record = (
        project_security_admission_evidence_coverage_closure_state(
            resolution
        )
    )
    assert domains_of(record) == required_domains_of(resolution)


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
def test_projection_is_deterministic(
    resolution_factory: object,
) -> None:
    resolution = resolution_factory()
    first = (
        project_security_admission_evidence_coverage_closure_state(
            resolution
        )
    )
    second = (
        project_security_admission_evidence_coverage_closure_state(
            resolution
        )
    )
    assert first == second
    assert first is not second
    assert first.domain_states is not second.domain_states
    assert first.closure_resolution is resolution
    assert second.closure_resolution is resolution


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_closure_resolution_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "closure_resolution must be a "
            "SecurityAdmissionEvidenceCoverageClosureResolution"
        ),
    ):
        project_security_admission_evidence_coverage_closure_state(
            invalid_value  # type: ignore[arg-type]
        )


def test_projection_accepts_only_the_terminal_graph() -> None:
    signature = inspect.signature(
        project_security_admission_evidence_coverage_closure_state
    )
    assert tuple(signature.parameters) == ("closure_resolution",)


def test_projection_has_no_resolver_or_reexecution_dependency() -> None:
    source = inspect.getsource(
        project_security_admission_evidence_coverage_closure_state
    )
    forbidden = (
        "resolver",
        "Callable",
        "execute",
        "evaluate",
        "replay",
    )
    assert all(token not in source for token in forbidden)


def test_projection_does_not_define_assessment_or_decision_semantics() -> None:
    source = inspect.getsource(
        project_security_admission_evidence_coverage_closure_state
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
        project_security_admission_evidence_coverage_closure_state
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"sp001"}
