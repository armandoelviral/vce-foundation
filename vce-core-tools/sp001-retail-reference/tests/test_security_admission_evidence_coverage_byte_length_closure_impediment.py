import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace
from typing import Callable

import pytest

from sp001.contracts.security_admission_candidate_identity import (
    SecurityAdmissionCandidateIdentity,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_conflict_result import (
    SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
)
from sp001.contracts.security_admission_evaluation_record_policy_evidence_requirements_binding import (
    SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_byte_length_closure_impediment import (
    SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment,
)
from sp001.contracts.security_admission_policy_identity import (
    SecurityAdmissionPolicyIdentity,
)
from tests.test_security_admission_candidate_byte_length_observation_resolution_conflict_result import (
    create_normative_conflict,
    create_timestamp_tie,
    create_unranked_conflict,
)
from tests.test_security_admission_evidence_coverage_identity import (
    create_identity,
)


ConflictFactory = Callable[
    [],
    SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
]


def create_coverage_identity(
    conflict: SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
    *,
    candidate_identity: SecurityAdmissionCandidateIdentity | None = None,
    policy_identity: SecurityAdmissionPolicyIdentity | None = None,
) -> SecurityAdmissionEvidenceCoverageIdentity:
    initial = create_identity()
    initial_binding = (
        initial.evaluation_record_policy_evidence_requirements_binding
    )
    conflict_candidate = (
        conflict.resolution_basis.observation_set.candidate_identity
    )
    conflict_policy = (
        conflict.resolution_basis.authority_order.admission_policy_identity
    )
    selected_candidate = (
        conflict_candidate
        if candidate_identity is None
        else candidate_identity
    )
    selected_policy = (
        conflict_policy
        if policy_identity is None
        else policy_identity
    )
    evaluation_record = replace(
        initial_binding.evaluation_record,
        evaluation_identity=replace(
            initial_binding.evaluation_record.evaluation_identity,
            evaluation_basis=replace(
                initial_binding
                .evaluation_record
                .evaluation_identity
                .evaluation_basis,
                candidate_identity=selected_candidate,
                admission_policy_identity=selected_policy,
            ),
        ),
    )
    requirements = replace(
        initial_binding.policy_evidence_requirements,
        admission_policy_identity=selected_policy,
    )
    binding = (
        SecurityAdmissionEvaluationRecordPolicyEvidenceRequirementsBinding(
            evaluation_record=evaluation_record,
            policy_evidence_requirements=requirements,
        )
    )
    return replace(
        initial,
        evaluation_record_policy_evidence_requirements_binding=binding,
    )


def create_impediment(
    conflict: (
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult
        | None
    ) = None,
) -> SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment:
    selected_conflict = (
        create_normative_conflict() if conflict is None else conflict
    )
    return SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment(
        coverage_identity=create_coverage_identity(selected_conflict),
        resolution_conflict_result=selected_conflict,
    )


def test_fields_are_exact() -> None:
    impediment_fields = fields(
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment
    )
    assert tuple(field.name for field in impediment_fields) == (
        "coverage_identity",
        "resolution_conflict_result",
    )
    assert (
        impediment_fields[0].type
        is SecurityAdmissionEvidenceCoverageIdentity
    )
    assert (
        impediment_fields[1].type
        is SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult
    )


def test_impediment_is_immutable_and_slotted() -> None:
    impediment = create_impediment()
    assert not hasattr(impediment, "__dict__")
    with pytest.raises(FrozenInstanceError):
        impediment.coverage_identity = create_identity()  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    impediment = create_impediment()
    coverage = impediment.coverage_identity
    conflict = impediment.resolution_conflict_result
    reconstructed = (
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment(
            coverage_identity=coverage,
            resolution_conflict_result=conflict,
        )
    )
    assert reconstructed.coverage_identity is coverage
    assert reconstructed.resolution_conflict_result is conflict


@pytest.mark.parametrize(
    "factory",
    (
        create_normative_conflict,
        create_unranked_conflict,
        create_timestamp_tie,
    ),
)
def test_every_logical_conflict_becomes_a_closure_impediment(
    factory: ConflictFactory,
) -> None:
    conflict = factory()
    impediment = create_impediment(conflict)
    assert impediment.resolution_conflict_result is conflict
    assert (
        impediment.coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .evaluation_record
        .evaluation_identity
        .evaluation_basis
        .candidate_identity
        == conflict.resolution_basis.observation_set.candidate_identity
    )
    assert (
        impediment.coverage_identity
        .evaluation_record_policy_evidence_requirements_binding
        .policy_evidence_requirements
        .admission_policy_identity
        == conflict.resolution_basis.authority_order.admission_policy_identity
    )


def test_complete_conflict_lineage_remains_reachable() -> None:
    impediment = create_impediment()
    conflict = impediment.resolution_conflict_result
    assert conflict.conflicting_observations
    assert conflict.resolution_basis.observation_set.observations
    assert (
        conflict.resolution_basis.authority_order
        .verification_procedure_identities
    )
    assert conflict.determined_at is not None


def test_equal_reconstruction_has_value_equality() -> None:
    impediment = create_impediment()
    reconstructed = replace(
        impediment,
        coverage_identity=replace(impediment.coverage_identity),
        resolution_conflict_result=replace(
            impediment.resolution_conflict_result
        ),
    )
    assert reconstructed == impediment
    assert reconstructed is not impediment


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    conflict = create_normative_conflict()
    with pytest.raises(
        TypeError,
        match=(
            "coverage_identity must be a "
            "SecurityAdmissionEvidenceCoverageIdentity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment(
            coverage_identity=invalid_value,  # type: ignore[arg-type]
            resolution_conflict_result=conflict,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_resolution_conflict_requires_nominal_type(
    invalid_value: object,
) -> None:
    conflict = create_normative_conflict()
    coverage = create_coverage_identity(conflict)
    with pytest.raises(
        TypeError,
        match=(
            "resolution_conflict_result must be a "
            "SecurityAdmissionCandidateByteLengthObservationResolution"
            "ConflictResult"
        ),
    ):
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment(
            coverage_identity=coverage,
            resolution_conflict_result=(  # type: ignore[arg-type]
                invalid_value
            ),
        )


def test_different_candidate_is_rejected() -> None:
    conflict = create_normative_conflict()
    candidate = (
        conflict.resolution_basis.observation_set.candidate_identity
    )
    different_candidate = replace(
        candidate,
        candidate_version=candidate.candidate_version + 1,
    )
    coverage = create_coverage_identity(
        conflict,
        candidate_identity=different_candidate,
    )
    with pytest.raises(
        ValueError,
        match=(
            "byte-length resolution conflict must use the coverage "
            "candidate_identity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment(
            coverage_identity=coverage,
            resolution_conflict_result=conflict,
        )


def test_different_policy_version_is_rejected() -> None:
    conflict = create_normative_conflict()
    policy = (
        conflict.resolution_basis.authority_order.admission_policy_identity
    )
    different_policy = replace(
        policy,
        admission_policy_version=policy.admission_policy_version + 1,
    )
    coverage = create_coverage_identity(
        conflict,
        policy_identity=different_policy,
    )
    with pytest.raises(
        ValueError,
        match=(
            "byte-length resolution conflict must use the coverage "
            "admission policy identity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment(
            coverage_identity=coverage,
            resolution_conflict_result=conflict,
        )


def test_contract_defines_impediment_without_admission_decision() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment
        )
    ) == (
        "coverage_identity",
        "resolution_conflict_result",
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment
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
        SecurityAdmissionEvidenceCoverageByteLengthClosureImpediment
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
