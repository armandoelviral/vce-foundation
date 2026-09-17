import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from datetime import timedelta

import pytest

from sp001.contracts.security_admission_evaluation_record import (
    SecurityAdmissionEvaluationRecord,
)
from sp001.contracts.security_admission_evaluation_record_policy_evidence_requirements_binding import (
    SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
    SecurityAdmissionPolicyEvidenceRequirements,
)
from tests.test_security_admission_evaluation_record import create_record
from tests.test_security_admission_policy_evidence_requirements import (
    create_requirements,
)


def create_binding(
    required_evidence_domains: tuple[SecurityAdmissionEvidenceDomain, ...] = (
        SecurityAdmissionEvidenceDomain.MEDIA_TYPE,
    ),
) -> SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding:
    evaluation_record = create_record()
    policy_identity = (
        evaluation_record
        .evaluation_identity
        .evaluation_basis
        .admission_policy_identity
    )
    requirements = replace(
        create_requirements(),
        admission_policy_identity=policy_identity,
        required_evidence_domains=required_evidence_domains,
    )
    return SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
        evaluation_record=evaluation_record,
        policy_evidence_requirements=requirements,
    )


def test_requirements_binding_fields_are_exact() -> None:
    binding_fields = fields(
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
    )

    assert tuple(field.name for field in binding_fields) == (
        "evaluation_record",
        "policy_evidence_requirements",
    )
    assert binding_fields[0].type is SecurityAdmissionEvaluationRecord
    assert (
        binding_fields[1].type
        is SecurityAdmissionPolicyEvidenceRequirements
    )


def test_requirements_binding_is_immutable() -> None:
    binding = create_binding()

    with pytest.raises(FrozenInstanceError):
        binding.evaluation_record = create_record()  # type: ignore[misc]


def test_requirements_binding_uses_slots() -> None:
    binding = create_binding()

    assert hasattr(
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
        "__slots__",
    )
    assert not hasattr(binding, "__dict__")


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_evaluation_record_requires_exact_type(invalid_value: object) -> None:
    requirements = create_binding().policy_evidence_requirements

    with pytest.raises(
        TypeError,
        match=(
            "evaluation_record must be a "
            "SecurityAdmissionEvaluationRecord"
        ),
    ):
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=invalid_value,  # type: ignore[arg-type]
            policy_evidence_requirements=requirements,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_policy_requirements_require_exact_type(
    invalid_value: object,
) -> None:
    record = create_record()

    with pytest.raises(
        TypeError,
        match=(
            "policy_evidence_requirements must be a "
            "SecurityAdmissionPolicyEvidenceRequirements"
        ),
    ):
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=record,
            policy_evidence_requirements=invalid_value,  # type: ignore[arg-type]
        )


def test_exact_evaluation_record_reference_is_preserved() -> None:
    record = create_record()
    policy = (
        record
        .evaluation_identity
        .evaluation_basis
        .admission_policy_identity
    )
    requirements = replace(
        create_requirements(),
        admission_policy_identity=policy,
    )
    binding = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=record,
            policy_evidence_requirements=requirements,
        )
    )

    assert binding.evaluation_record is record


def test_exact_policy_requirements_reference_is_preserved() -> None:
    binding = create_binding()
    requirements = binding.policy_evidence_requirements

    reconstructed = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=binding.evaluation_record,
            policy_evidence_requirements=requirements,
        )
    )

    assert reconstructed.policy_evidence_requirements is requirements


def test_reconstructed_equal_binding_has_value_equality() -> None:
    binding = create_binding()
    reconstructed = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=replace(binding.evaluation_record),
            policy_evidence_requirements=replace(
                binding.policy_evidence_requirements
            ),
        )
    )

    assert reconstructed == binding
    assert reconstructed is not binding


def test_equal_reconstructed_policy_identity_permits_binding() -> None:
    binding = create_binding()
    requirements = binding.policy_evidence_requirements
    reconstructed_requirements = replace(
        requirements,
        admission_policy_identity=replace(
            requirements.admission_policy_identity
        ),
    )

    reconstructed = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=binding.evaluation_record,
            policy_evidence_requirements=reconstructed_requirements,
        )
    )

    assert reconstructed.policy_evidence_requirements is reconstructed_requirements


def test_different_policy_identity_is_rejected() -> None:
    binding = create_binding()
    policy = binding.policy_evidence_requirements.admission_policy_identity
    different_policy = replace(
        policy,
        admission_policy_version=policy.admission_policy_version + 1,
    )
    different_requirements = replace(
        binding.policy_evidence_requirements,
        admission_policy_identity=different_policy,
    )

    with pytest.raises(
        ValueError,
        match=(
            "policy evidence requirements must use "
            "evaluation record policy identity"
        ),
    ):
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=binding.evaluation_record,
            policy_evidence_requirements=different_requirements,
        )


@pytest.mark.parametrize(
    "required_evidence_domains",
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
def test_required_domains_are_preserved_without_interpretation(
    required_evidence_domains: tuple[SecurityAdmissionEvidenceDomain, ...],
) -> None:
    binding = create_binding(required_evidence_domains)

    assert (
        binding.policy_evidence_requirements.required_evidence_domains
        is required_evidence_domains
    )


def test_evaluation_record_participates_in_binding_value() -> None:
    binding = create_binding()
    different_record = replace(
        binding.evaluation_record,
        evaluated_at=binding.evaluation_record.evaluated_at + timedelta(seconds=1),
    )
    different = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=different_record,
            policy_evidence_requirements=binding.policy_evidence_requirements,
        )
    )

    assert different != binding


def test_policy_requirements_participate_in_binding_value() -> None:
    binding = create_binding(
        (SecurityAdmissionEvidenceDomain.MEDIA_TYPE,)
    )
    different_requirements = replace(
        binding.policy_evidence_requirements,
        required_evidence_domains=(
            SecurityAdmissionEvidenceDomain.BYTE_LENGTH,
        ),
    )
    different = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=binding.evaluation_record,
            policy_evidence_requirements=different_requirements,
        )
    )

    assert different != binding


def test_policy_identity_and_domains_are_not_duplicated_as_fields() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
        )
    }

    assert names.isdisjoint(
        {
            "admission_policy_identity",
            "required_evidence_domains",
            "evidence_domains",
        }
    )


def test_availability_completeness_decision_and_authority_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
        )
    }

    assert names.isdisjoint(
        {
            "available_evidence_domains",
            "missing_evidence_domains",
            "evidence_bindings",
            "evidence_complete",
            "requirements_satisfied",
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
    module = inspect.getmodule(
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert function_names == {"__post_init__"}


def test_contract_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
    )
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

    assert imported_roots == {"dataclasses", "sp001"}


def test_contract_defines_validation_only() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding
    )
    tree = ast.parse(source)
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert calls <= {
        "dataclass",
        "isinstance",
        "TypeError",
        "ValueError",
    }
