import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from enum import StrEnum

import pytest

from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
    SecurityAdmissionPolicyEvidenceRequirements,
)
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)
from tests.test_security_admission_policy_identity import create_identity


def create_requirements(
    *,
    admission_policy_identity: SecurityAdmissionPolicyIdentity | None = None,
    required_evidence_domains: (
        tuple[SecurityAdmissionEvidenceDomain, ...] | None
    ) = None,
) -> SecurityAdmissionPolicyEvidenceRequirements:
    return SecurityAdmissionPolicyEvidenceRequirements(
        admission_policy_identity=(
            create_identity()
            if admission_policy_identity is None
            else admission_policy_identity
        ),
        required_evidence_domains=(
            (SecurityAdmissionEvidenceDomain.MEDIA_TYPE,)
            if required_evidence_domains is None
            else required_evidence_domains
        ),
    )


def test_evidence_domain_members_are_exact() -> None:
    Domain = SecurityAdmissionEvidenceDomain

    assert issubclass(Domain, StrEnum)
    assert tuple(Domain) == (
        Domain.MEDIA_TYPE,
        Domain.BYTE_LENGTH,
    )
    assert tuple(member.value for member in Domain) == (
        "MEDIA_TYPE",
        "BYTE_LENGTH",
    )


def test_requirements_fields_are_exact() -> None:
    requirement_fields = fields(SecurityAdmissionPolicyEvidenceRequirements)

    assert tuple(field.name for field in requirement_fields) == (
        "admission_policy_identity",
        "required_evidence_domains",
    )
    assert requirement_fields[0].type is SecurityAdmissionPolicyIdentity
    assert requirement_fields[1].type == tuple[
        SecurityAdmissionEvidenceDomain,
        ...,
    ]


def test_requirements_are_immutable() -> None:
    requirements = create_requirements()

    with pytest.raises(FrozenInstanceError):
        requirements.required_evidence_domains = ()  # type: ignore[misc]


def test_requirements_use_slots() -> None:
    requirements = create_requirements()

    assert hasattr(SecurityAdmissionPolicyEvidenceRequirements, "__slots__")
    assert not hasattr(requirements, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_admission_policy_identity_requires_exact_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "admission_policy_identity must be a "
            "SecurityAdmissionPolicyIdentity"
        ),
    ):
        SecurityAdmissionPolicyEvidenceRequirements(
            admission_policy_identity=invalid_value,  # type: ignore[arg-type]
            required_evidence_domains=(
                SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
            ),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        [SecurityAdmissionEvidenceDomain.MEDIA_TYPE],
        {SecurityAdmissionEvidenceDomain.MEDIA_TYPE},
        frozenset({SecurityAdmissionEvidenceDomain.MEDIA_TYPE}),
    ),
)
def test_required_evidence_domains_requires_tuple(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="required_evidence_domains must be an immutable tuple",
    ):
        SecurityAdmissionPolicyEvidenceRequirements(
            admission_policy_identity=create_identity(),
            required_evidence_domains=invalid_value,  # type: ignore[arg-type]
        )


def test_required_evidence_domains_must_not_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="required_evidence_domains must not be empty",
    ):
        SecurityAdmissionPolicyEvidenceRequirements(
            admission_policy_identity=create_identity(),
            required_evidence_domains=(),
        )


@pytest.mark.parametrize(
    "invalid_member",
    (None, "MEDIA_TYPE", 1, True, object()),
)
def test_required_domains_require_exact_member_type(
    invalid_member: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "required_evidence_domains must contain "
            "SecurityAdmissionEvidenceDomain values"
        ),
    ):
        SecurityAdmissionPolicyEvidenceRequirements(
            admission_policy_identity=create_identity(),
            required_evidence_domains=(
                invalid_member,  # type: ignore[arg-type]
            ),
        )


@pytest.mark.parametrize(
    "domain",
    tuple(SecurityAdmissionEvidenceDomain),
)
def test_duplicate_required_domain_is_rejected(
    domain: SecurityAdmissionEvidenceDomain,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"duplicate required evidence domain: {domain}",
    ):
        SecurityAdmissionPolicyEvidenceRequirements(
            admission_policy_identity=create_identity(),
            required_evidence_domains=(domain, domain),
        )


@pytest.mark.parametrize(
    "domains",
    (
        (SecurityAdmissionEvidenceDomain.MEDIA_TYPE,),
        (SecurityAdmissionEvidenceDomain.BYTE_LENGTH,),
        (
            SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
            SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
        ),
        (
            SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
            SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
        ),
    ),
)
def test_supported_required_domain_tuples_are_preserved(
    domains: tuple[SecurityAdmissionEvidenceDomain, ...],
) -> None:
    requirements = create_requirements(
        required_evidence_domains=domains,
    )

    assert requirements.required_evidence_domains is domains


def test_exact_policy_identity_reference_is_preserved() -> None:
    policy = create_identity()
    requirements = create_requirements(
        admission_policy_identity=policy,
    )

    assert requirements.admission_policy_identity is policy


def test_reconstructed_equal_requirements_have_value_equality() -> None:
    requirements = create_requirements(
        required_evidence_domains=(
            SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
            SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
        ),
    )
    reconstructed = SecurityAdmissionPolicyEvidenceRequirements(
        admission_policy_identity=replace(
            requirements.admission_policy_identity
        ),
        required_evidence_domains=tuple(
            requirements.required_evidence_domains
        ),
    )

    assert reconstructed == requirements
    assert reconstructed is not requirements


def test_policy_identity_participates_in_requirement_value() -> None:
    requirements = create_requirements()
    policy = requirements.admission_policy_identity
    different_policy = replace(
        policy,
        admission_policy_version=policy.admission_policy_version + 1,
    )

    assert replace(
        requirements,
        admission_policy_identity=different_policy,
    ) != requirements


def test_domains_and_order_participate_in_requirement_value() -> None:
    Domain = SecurityAdmissionEvidenceDomain
    requirements = create_requirements(
        required_evidence_domains=(Domain.MEDIA_TYPE, Domain.BYTE_LENGTH),
    )

    assert replace(
        requirements,
        required_evidence_domains=(Domain.MEDIA_TYPE,),
    ) != requirements
    assert replace(
        requirements,
        required_evidence_domains=(Domain.BYTE_LENGTH, Domain.MEDIA_TYPE),
    ) != requirements


def test_optional_and_availability_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionPolicyEvidenceRequirements)
    }

    assert names.isdisjoint(
        {
            "optional_evidence_domains",
            "available_evidence_domains",
            "missing_evidence_domains",
        }
    )


def test_evaluation_decision_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(SecurityAdmissionPolicyEvidenceRequirements)
    }

    assert names.isdisjoint(
        {
            "evaluation_record",
            "evidence_bindings",
            "status",
            "decision",
            "reason",
            "admitted",
            "rejected",
            "authorized",
            "authorization",
            "quarantine",
            "retention",
        }
    )


def test_contract_performs_no_policy_or_evaluation_execution() -> None:
    source = inspect.getsource(SecurityAdmissionPolicyEvidenceRequirements)
    tree = ast.parse(source)
    forbidden_calls = {
        "compare",
        "evaluate",
        "execute",
        "authorize",
        "admit",
        "reject",
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert called_names.isdisjoint(forbidden_calls)


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(SecurityAdmissionPolicyEvidenceRequirements)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    imported_roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    imported_roots.update(
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    )

    assert imported_roots == {"dataclasses", "enum", "sp001"}


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(SecurityAdmissionPolicyEvidenceRequirements)
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert functions == {"__post_init__"}
