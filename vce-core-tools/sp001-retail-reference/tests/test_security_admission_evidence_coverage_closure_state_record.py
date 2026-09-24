import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure_blockage import (
    SecurityAdmissionEvidenceCoverageClosureBlockage,
)
from sp001.contracts.security_admission_evidence_coverage_closure_resolution import (
    SecurityAdmissionEvidenceCoverageClosureResolution,
)
from sp001.contracts.security_admission_evidence_coverage_closure_state_record import (
    SecurityAdmissionEvidenceCoverageClosureStateRecord,
)
from sp001.contracts.security_admission_evidence_coverage_domain_closure_state import (
    SecurityAdmissionEvidenceCoverageDomainClosureState,
    SecurityAdmissionEvidenceCoverageDomainClosureStatus,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from tests.test_security_admission_evidence_coverage_byte_length_closure_impediment import (
    create_impediment as create_byte_length_impediment,
)
from tests.test_security_admission_evidence_coverage_closure_blockage import (
    create_second_domain_blockage,
    rebind_impediment,
)
from tests.test_security_admission_evidence_coverage_closure_resolution import (
    create_resolution,
)
from tests.test_security_admission_evidence_coverage_media_type_closure_impediment import (
    create_impediment as create_media_type_impediment,
)
from tests.test_security_admission_evidence_coverage_resolution_outcome_set import (
    create_coverage_identity,
)


Domain = SecurityAdmissionEvidenceDomain
Status = SecurityAdmissionEvidenceCoverageDomainClosureStatus
State = SecurityAdmissionEvidenceCoverageDomainClosureState


def required_domains_for(
    resolution: SecurityAdmissionEvidenceCoverageClosureResolution,
) -> tuple[Domain, ...]:
    return (
        resolution
        .coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
        .required_evidence_domains
    )


def states_for(
    resolution: SecurityAdmissionEvidenceCoverageClosureResolution,
    statuses: tuple[Status, ...],
) -> tuple[State, ...]:
    return tuple(
        State(domain=domain, status=status)
        for domain, status in zip(
            required_domains_for(resolution),
            statuses,
            strict=True,
        )
    )


def create_complete_record(
) -> SecurityAdmissionEvidenceCoverageClosureStateRecord:
    resolution = create_resolution()
    domains = required_domains_for(resolution)
    return SecurityAdmissionEvidenceCoverageClosureStateRecord(
        closure_resolution=resolution,
        domain_states=tuple(
            State(domain=domain, status=Status.RESOLVED)
            for domain in domains
        ),
    )


def create_first_domain_blocked_resolution(
    first_domain: Domain,
) -> SecurityAdmissionEvidenceCoverageClosureResolution:
    second_domain = (
        Domain.BYTE_LENGTH
        if first_domain is Domain.MEDIA_TYPE
        else Domain.MEDIA_TYPE
    )
    impediment = (
        create_media_type_impediment()
        if first_domain is Domain.MEDIA_TYPE
        else create_byte_length_impediment()
    )
    coverage_identity = create_coverage_identity(
        (first_domain, second_domain),
        impediment.coverage_identity,
    )
    rebound_impediment = rebind_impediment(
        impediment,
        coverage_identity,
    )
    blockage = SecurityAdmissionEvidenceCoverageClosureBlockage(
        coverage_identity=coverage_identity,
        resolved_prefix=(),
        impediment=rebound_impediment,
    )
    return SecurityAdmissionEvidenceCoverageClosureResolution(
        coverage_identity=coverage_identity,
        outcome=blockage,
    )


def create_second_domain_blocked_resolution(
    first_domain: Domain,
) -> SecurityAdmissionEvidenceCoverageClosureResolution:
    blockage = create_second_domain_blockage(first_domain)
    return SecurityAdmissionEvidenceCoverageClosureResolution(
        coverage_identity=blockage.coverage_identity,
        outcome=blockage,
    )


def test_fields_are_exact() -> None:
    record_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateRecord
    )
    assert tuple(field.name for field in record_fields) == (
        "closure_resolution",
        "domain_states",
    )
    assert (
        record_fields[0].type
        is SecurityAdmissionEvidenceCoverageClosureResolution
    )
    assert (
        record_fields[1].type
        == tuple[
            SecurityAdmissionEvidenceCoverageDomainClosureState,
            ...,
        ]
    )


def test_record_is_immutable_and_slotted() -> None:
    record = create_complete_record()
    assert not hasattr(record, "__dict__")
    with pytest.raises(FrozenInstanceError):
        record.domain_states = ()  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    record = create_complete_record()
    reconstructed = SecurityAdmissionEvidenceCoverageClosureStateRecord(
        closure_resolution=record.closure_resolution,
        domain_states=record.domain_states,
    )
    assert reconstructed.closure_resolution is record.closure_resolution
    assert reconstructed.domain_states is record.domain_states


def test_complete_closure_records_every_domain_as_resolved() -> None:
    record = create_complete_record()
    assert tuple(
        state.status
        for state in record.domain_states
    ) == (
        Status.RESOLVED,
    ) * len(record.domain_states)


@pytest.mark.parametrize(
    "first_domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_first_impediment_marks_later_domain_not_evaluated(
    first_domain: Domain,
) -> None:
    resolution = create_first_domain_blocked_resolution(first_domain)
    record = SecurityAdmissionEvidenceCoverageClosureStateRecord(
        closure_resolution=resolution,
        domain_states=states_for(
            resolution,
            (Status.IMPEDED, Status.NOT_EVALUATED),
        ),
    )
    assert tuple(
        state.status
        for state in record.domain_states
    ) == (
        Status.IMPEDED,
        Status.NOT_EVALUATED,
    )


@pytest.mark.parametrize(
    "first_domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_second_impediment_preserves_resolved_prefix(
    first_domain: Domain,
) -> None:
    resolution = create_second_domain_blocked_resolution(first_domain)
    record = SecurityAdmissionEvidenceCoverageClosureStateRecord(
        closure_resolution=resolution,
        domain_states=states_for(
            resolution,
            (Status.RESOLVED, Status.IMPEDED),
        ),
    )
    assert tuple(
        state.status
        for state in record.domain_states
    ) == (
        Status.RESOLVED,
        Status.IMPEDED,
    )


def test_equal_reconstruction_has_value_equality() -> None:
    record = create_complete_record()
    reconstructed = replace(
        record,
        closure_resolution=replace(record.closure_resolution),
        domain_states=tuple(
            replace(state)
            for state in record.domain_states
        ),
    )
    assert reconstructed == record
    assert reconstructed is not record


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_closure_resolution_requires_nominal_type(
    invalid_value: object,
) -> None:
    record = create_complete_record()
    with pytest.raises(
        TypeError,
        match=(
            "closure_resolution must be a "
            "SecurityAdmissionEvidenceCoverageClosureResolution"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateRecord(
            closure_resolution=invalid_value,  # type: ignore[arg-type]
            domain_states=record.domain_states,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, []))
def test_domain_states_requires_immutable_tuple(
    invalid_value: object,
) -> None:
    resolution = create_resolution()
    with pytest.raises(
        TypeError,
        match="domain_states must be an immutable tuple",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateRecord(
            closure_resolution=resolution,
            domain_states=invalid_value,  # type: ignore[arg-type]
        )


def test_domain_states_require_nominal_members() -> None:
    resolution = create_resolution()
    domains = required_domains_for(resolution)
    invalid_states = (
        object(),
        *(
            State(domain=domain, status=Status.RESOLVED)
            for domain in domains[1:]
        ),
    )
    with pytest.raises(
        TypeError,
        match=(
            "domain_states must contain "
            "SecurityAdmissionEvidenceCoverageDomainClosureState values"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateRecord(
            closure_resolution=resolution,
            domain_states=invalid_states,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("delta", (-1, 1))
def test_domain_state_cardinality_must_be_exact(delta: int) -> None:
    record = create_complete_record()
    states = record.domain_states
    changed_states = (
        states[:-1]
        if delta < 0
        else states + (states[-1],)
    )
    with pytest.raises(
        ValueError,
        match=(
            "domain_states must contain exactly one state "
            "for each required evidence domain"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateRecord(
            closure_resolution=record.closure_resolution,
            domain_states=changed_states,
        )


def test_domain_states_must_preserve_policy_order() -> None:
    resolution = create_first_domain_blocked_resolution(
        Domain.MEDIA_TYPE
    )
    record = SecurityAdmissionEvidenceCoverageClosureStateRecord(
        closure_resolution=resolution,
        domain_states=states_for(
            resolution,
            (Status.IMPEDED, Status.NOT_EVALUATED),
        ),
    )
    with pytest.raises(
        ValueError,
        match=(
            "domain_states must preserve required evidence domain order"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateRecord(
            closure_resolution=record.closure_resolution,
            domain_states=tuple(reversed(record.domain_states)),
        )


def test_complete_closure_rejects_nonresolved_state() -> None:
    record = create_complete_record()
    changed_states = (
        replace(
            record.domain_states[0],
            status=Status.IMPEDED,
        ),
        *record.domain_states[1:],
    )
    with pytest.raises(
        ValueError,
        match=(
            "domain_states must exactly represent "
            "the terminal closure result"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateRecord(
            closure_resolution=record.closure_resolution,
            domain_states=changed_states,
        )


@pytest.mark.parametrize(
    "invalid_statuses",
    (
        (Status.RESOLVED, Status.NOT_EVALUATED),
        (Status.IMPEDED, Status.RESOLVED),
        (Status.NOT_EVALUATED, Status.IMPEDED),
    ),
)
def test_blockage_rejects_incorrect_state_sequence(
    invalid_statuses: tuple[Status, ...],
) -> None:
    resolution = create_first_domain_blocked_resolution(
        Domain.MEDIA_TYPE
    )
    with pytest.raises(
        ValueError,
        match=(
            "domain_states must exactly represent "
            "the terminal closure result"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateRecord(
            closure_resolution=resolution,
            domain_states=states_for(
                resolution,
                invalid_statuses,
            ),
        )


def test_assessment_and_decision_fields_are_absent() -> None:
    record = create_complete_record()
    for field_name in (
        "assessment",
        "classification",
        "admission_status",
        "admission_decision",
        "rejection",
        "authority",
    ):
        assert not hasattr(record, field_name)


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureStateRecord
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
        SecurityAdmissionEvidenceCoverageClosureStateRecord
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
