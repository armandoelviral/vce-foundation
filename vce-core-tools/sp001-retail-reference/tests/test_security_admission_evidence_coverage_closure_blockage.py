import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure_blockage import (
    SecurityAdmissionEvidenceCoverageClosureBlockage,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from tests.test_security_admission_evidence_coverage_byte_length_closure_impediment import (
    create_impediment as create_byte_length_impediment,
)
from tests.test_security_admission_evidence_coverage_media_type_closure_impediment import (
    create_impediment as create_media_type_impediment,
)
from tests.test_security_admission_evidence_coverage_resolution_outcome_set import (
    create_byte_length_conclusive_outcome,
    create_byte_length_impediment_outcome,
    create_coverage_identity,
    create_media_type_conclusive_outcome,
    create_media_type_impediment_outcome,
    rebind_outcome,
)


Domain = SecurityAdmissionEvidenceDomain


def rebind_impediment(
    impediment: object,
    coverage_identity: SecurityAdmissionEvidenceCoverageIdentity,
) -> object:
    impediment_field = next(
        field.name
        for field in fields(impediment)
        if field.name != "coverage_identity"
    )
    conflict = getattr(impediment, impediment_field)
    resolution_basis = conflict.resolution_basis
    authority_order = resolution_basis.authority_order
    policy_identity = (
        coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
        .admission_policy_identity
    )
    rebound_authority_order = replace(
        authority_order,
        admission_policy_identity=policy_identity,
    )
    rebound_conflict = replace(
        conflict,
        resolution_basis=replace(
            resolution_basis,
            authority_order=rebound_authority_order,
        ),
    )
    return replace(
        impediment,
        coverage_identity=coverage_identity,
        **{impediment_field: rebound_conflict},
    )


def create_first_domain_blockage(
    domain: Domain,
) -> SecurityAdmissionEvidenceCoverageClosureBlockage:
    impediment = (
        create_media_type_impediment()
        if domain is Domain.MEDIA_TYPE
        else create_byte_length_impediment()
    )
    coverage_identity = create_coverage_identity(
        (domain,),
        impediment.coverage_identity,
    )
    rebound_impediment = rebind_impediment(
        impediment,
        coverage_identity,
    )
    return SecurityAdmissionEvidenceCoverageClosureBlockage(
        coverage_identity=coverage_identity,
        resolved_prefix=(),
        impediment=rebound_impediment,
    )


def create_second_domain_blockage(
    first_domain: Domain,
) -> SecurityAdmissionEvidenceCoverageClosureBlockage:
    if first_domain is Domain.MEDIA_TYPE:
        resolved = create_media_type_conclusive_outcome()
        impediment = create_byte_length_impediment()
        second_domain = Domain.BYTE_LENGTH
    else:
        resolved = create_byte_length_conclusive_outcome()
        impediment = create_media_type_impediment()
        second_domain = Domain.MEDIA_TYPE

    coverage_identity = create_coverage_identity(
        (first_domain, second_domain),
        resolved.coverage_identity,
    )
    rebound_resolved = rebind_outcome(resolved, coverage_identity)
    rebound_impediment = rebind_impediment(
        impediment,
        coverage_identity,
    )
    return SecurityAdmissionEvidenceCoverageClosureBlockage(
        coverage_identity=coverage_identity,
        resolved_prefix=(rebound_resolved,),
        impediment=rebound_impediment,
    )


def test_blockage_fields_are_exact() -> None:
    blockage_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureBlockage
    )
    assert tuple(field.name for field in blockage_fields) == (
        "coverage_identity",
        "resolved_prefix",
        "impediment",
    )
    assert (
        blockage_fields[0].type
        is SecurityAdmissionEvidenceCoverageIdentity
    )


def test_blockage_is_immutable() -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    with pytest.raises(FrozenInstanceError):
        blockage.resolved_prefix = ()  # type: ignore[misc]


def test_blockage_uses_slots() -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    assert hasattr(
        SecurityAdmissionEvidenceCoverageClosureBlockage,
        "__slots__",
    )
    assert not hasattr(blockage, "__dict__")


@pytest.mark.parametrize(
    "domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_first_required_domain_can_block_before_any_resolution(
    domain: Domain,
) -> None:
    blockage = create_first_domain_blockage(domain)
    assert blockage.resolved_prefix == ()
    assert blockage.impediment.coverage_identity is blockage.coverage_identity


@pytest.mark.parametrize(
    "first_domain",
    (Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
)
def test_second_required_domain_can_block_after_exact_prefix(
    first_domain: Domain,
) -> None:
    blockage = create_second_domain_blockage(first_domain)
    assert len(blockage.resolved_prefix) == 1
    assert (
        blockage.resolved_prefix[0].coverage_identity
        is blockage.coverage_identity
    )
    assert blockage.impediment.coverage_identity is blockage.coverage_identity


@pytest.mark.parametrize(
    "factory",
    (
        lambda: create_first_domain_blockage(Domain.MEDIA_TYPE),
        lambda: create_first_domain_blockage(Domain.BYTE_LENGTH),
        lambda: create_second_domain_blockage(Domain.MEDIA_TYPE),
        lambda: create_second_domain_blockage(Domain.BYTE_LENGTH),
    ),
)
def test_exact_blockage_graph_is_preserved(factory: object) -> None:
    blockage = factory()
    reconstructed = SecurityAdmissionEvidenceCoverageClosureBlockage(
        coverage_identity=blockage.coverage_identity,
        resolved_prefix=blockage.resolved_prefix,
        impediment=blockage.impediment,
    )
    assert reconstructed.coverage_identity is blockage.coverage_identity
    assert reconstructed.resolved_prefix is blockage.resolved_prefix
    assert reconstructed.impediment is blockage.impediment


def test_equal_reconstructed_blockage_has_value_equality() -> None:
    blockage = create_second_domain_blockage(Domain.MEDIA_TYPE)
    reconstructed = SecurityAdmissionEvidenceCoverageClosureBlockage(
        coverage_identity=replace(blockage.coverage_identity),
        resolved_prefix=tuple(
            replace(outcome)
            for outcome in blockage.resolved_prefix
        ),
        impediment=replace(blockage.impediment),
    )
    assert reconstructed == blockage
    assert reconstructed is not blockage


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_exact_type(
    invalid_value: object,
) -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=invalid_value,  # type: ignore[arg-type]
            resolved_prefix=blockage.resolved_prefix,
            impediment=blockage.impediment,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, []))
def test_resolved_prefix_requires_immutable_tuple(
    invalid_value: object,
) -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=invalid_value,  # type: ignore[arg-type]
            impediment=blockage.impediment,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_impediment_requires_nominal_type(
    invalid_value: object,
) -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=(),
            impediment=invalid_value,  # type: ignore[arg-type]
        )


def test_prefix_members_require_resolution_outcomes() -> None:
    blockage = create_second_domain_blockage(Domain.MEDIA_TYPE)
    with pytest.raises(TypeError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=(object(),),
            impediment=blockage.impediment,
        )


@pytest.mark.parametrize(
    ("factory", "impeded_domain"),
    (
        (
            create_media_type_impediment_outcome,
            Domain.MEDIA_TYPE,
        ),
        (
            create_byte_length_impediment_outcome,
            Domain.BYTE_LENGTH,
        ),
    ),
)
def test_resolved_prefix_must_not_contain_impediments(
    factory: object,
    impeded_domain: Domain,
) -> None:
    outcome = factory()
    other_domain = (
        Domain.BYTE_LENGTH
        if impeded_domain is Domain.MEDIA_TYPE
        else Domain.MEDIA_TYPE
    )
    coverage_identity = create_coverage_identity(
        (impeded_domain, other_domain),
        outcome.coverage_identity,
    )
    rebound = rebind_outcome(outcome, coverage_identity)
    raw_impediment = (
        create_byte_length_impediment()
        if other_domain is Domain.BYTE_LENGTH
        else create_media_type_impediment()
    )
    rebound_impediment = rebind_impediment(
        raw_impediment,
        coverage_identity,
    )
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=coverage_identity,
            resolved_prefix=(rebound,),
            impediment=rebound_impediment,
        )


def test_complete_prefix_is_rejected() -> None:
    blockage = create_second_domain_blockage(Domain.MEDIA_TYPE)
    second = create_byte_length_conclusive_outcome()
    rebound_second = rebind_outcome(
        second,
        blockage.coverage_identity,
    )
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=(
                blockage.resolved_prefix[0],
                rebound_second,
            ),
            impediment=blockage.impediment,
        )


def test_prefix_must_follow_required_domain_order() -> None:
    blockage = create_second_domain_blockage(Domain.MEDIA_TYPE)
    wrong = create_byte_length_conclusive_outcome()
    wrong = rebind_outcome(wrong, blockage.coverage_identity)
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=(wrong,),
            impediment=blockage.impediment,
        )


def test_prefix_must_use_blockage_coverage_identity() -> None:
    blockage = create_second_domain_blockage(Domain.MEDIA_TYPE)
    foreign = create_media_type_conclusive_outcome()
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=(foreign,),
            impediment=blockage.impediment,
        )


def test_impediment_must_use_blockage_coverage_identity() -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    foreign_identity = replace(
        blockage.coverage_identity,
        coverage_version=(
            blockage.coverage_identity.coverage_version + 1
        ),
    )
    foreign = replace(
        blockage.impediment,
        coverage_identity=foreign_identity,
    )
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=(),
            impediment=foreign,
        )


def test_impediment_must_match_first_unresolved_domain() -> None:
    blockage = create_second_domain_blockage(Domain.MEDIA_TYPE)
    wrong = create_media_type_impediment()
    wrong = rebind_impediment(wrong, blockage.coverage_identity)
    with pytest.raises(ValueError):
        SecurityAdmissionEvidenceCoverageClosureBlockage(
            coverage_identity=blockage.coverage_identity,
            resolved_prefix=blockage.resolved_prefix,
            impediment=wrong,
        )


def test_post_closure_decision_fields_are_absent() -> None:
    blockage = create_first_domain_blockage(Domain.MEDIA_TYPE)
    for field_name in (
        "assessment",
        "assessments",
        "classification",
        "admission_status",
        "admission_decision",
        "rejection",
        "authority",
    ):
        assert not hasattr(blockage, field_name)


def test_contract_defines_validation_only() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureBlockage
    )
    tree = ast.parse(source)
    methods = {
        node.name
        for node in tree.body[0].body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert methods == {"__post_init__"}


def test_contract_has_no_external_capability_calls() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureBlockage
    )
    forbidden = (
        "open(",
        "requests.",
        "httpx.",
        "subprocess.",
        "socket.",
        "pathlib.",
    )
    assert all(token not in source for token in forbidden)
