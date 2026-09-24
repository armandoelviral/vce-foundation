import ast
import inspect
from dataclasses import FrozenInstanceError, fields, replace
from typing import Callable

import pytest

from sp001.contracts.security_admission_evidence_coverage_closure import (
    SecurityAdmissionEvidenceCoverageClosure,
)
from sp001.contracts.security_admission_evidence_coverage_closure_blockage import (
    SecurityAdmissionEvidenceCoverageClosureBlockage,
)
from sp001.contracts.security_admission_evidence_coverage_closure_resolution import (
    SecurityAdmissionEvidenceCoverageClosureResolution,
    SecurityAdmissionEvidenceCoverageClosureResolutionValue,
)
from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_policy_evidence_requirements import (
    SecurityAdmissionEvidenceDomain,
)
from tests.test_security_admission_evidence_coverage_closure import (
    create_closure,
)
from tests.test_security_admission_evidence_coverage_closure_blockage import (
    create_first_domain_blockage,
    create_second_domain_blockage,
)


ClosureFactory = Callable[
    [],
    SecurityAdmissionEvidenceCoverageClosureResolutionValue,
]


def coverage_identity_for(
    outcome: SecurityAdmissionEvidenceCoverageClosureResolutionValue,
) -> SecurityAdmissionEvidenceCoverageIdentity:
    if isinstance(
        outcome,
        SecurityAdmissionEvidenceCoverageClosure,
    ):
        return outcome.resolution_outcome_set.coverage_identity
    return outcome.coverage_identity


def create_resolution(
    factory: ClosureFactory = create_closure,
) -> SecurityAdmissionEvidenceCoverageClosureResolution:
    outcome = factory()
    return SecurityAdmissionEvidenceCoverageClosureResolution(
        coverage_identity=coverage_identity_for(outcome),
        outcome=outcome,
    )


def create_media_type_first_blockage(
) -> SecurityAdmissionEvidenceCoverageClosureBlockage:
    return create_first_domain_blockage(
        SecurityAdmissionEvidenceDomain.MEDIA_TYPE
    )


def create_byte_length_first_blockage(
) -> SecurityAdmissionEvidenceCoverageClosureBlockage:
    return create_first_domain_blockage(
        SecurityAdmissionEvidenceDomain.BYTE_LENGTH
    )


def create_media_type_prefix_blockage(
) -> SecurityAdmissionEvidenceCoverageClosureBlockage:
    return create_second_domain_blockage(
        SecurityAdmissionEvidenceDomain.MEDIA_TYPE
    )


def create_byte_length_prefix_blockage(
) -> SecurityAdmissionEvidenceCoverageClosureBlockage:
    return create_second_domain_blockage(
        SecurityAdmissionEvidenceDomain.BYTE_LENGTH
    )


def test_fields_are_exact() -> None:
    resolution_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureResolution
    )
    assert tuple(field.name for field in resolution_fields) == (
        "coverage_identity",
        "outcome",
    )
    assert (
        resolution_fields[0].type
        is SecurityAdmissionEvidenceCoverageIdentity
    )
    assert (
        resolution_fields[1].type
        == SecurityAdmissionEvidenceCoverageClosureResolutionValue
    )


def test_closure_resolution_is_immutable_and_slotted() -> None:
    resolution = create_resolution()
    assert not hasattr(resolution, "__dict__")
    with pytest.raises(FrozenInstanceError):
        resolution.outcome = create_closure()  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    resolution = create_resolution()
    reconstructed = SecurityAdmissionEvidenceCoverageClosureResolution(
        coverage_identity=resolution.coverage_identity,
        outcome=resolution.outcome,
    )
    assert reconstructed.coverage_identity is resolution.coverage_identity
    assert reconstructed.outcome is resolution.outcome


@pytest.mark.parametrize(
    "factory",
    (
        create_closure,
        create_media_type_first_blockage,
        create_byte_length_first_blockage,
        create_media_type_prefix_blockage,
        create_byte_length_prefix_blockage,
    ),
)
def test_each_terminal_variant_is_preserved(
    factory: ClosureFactory,
) -> None:
    outcome = factory()
    resolution = SecurityAdmissionEvidenceCoverageClosureResolution(
        coverage_identity=coverage_identity_for(outcome),
        outcome=outcome,
    )
    assert resolution.outcome is outcome


@pytest.mark.parametrize(
    "factory",
    (
        create_closure,
        create_media_type_first_blockage,
        create_byte_length_first_blockage,
        create_media_type_prefix_blockage,
        create_byte_length_prefix_blockage,
    ),
)
def test_each_terminal_variant_preserves_complete_lineage(
    factory: ClosureFactory,
) -> None:
    resolution = create_resolution(factory)
    outcome = resolution.outcome

    assert (
        resolution.coverage_identity
        is coverage_identity_for(outcome)
    )

    if isinstance(
        outcome,
        SecurityAdmissionEvidenceCoverageClosure,
    ):
        assert outcome.resolution_outcome_set.outcomes
        assert (
            len(outcome.resolution_outcome_set.outcomes)
            == len(
                resolution
                .coverage_identity
                .evaluation_record_policy_evidence_requirements_binding
                .policy_evidence_requirements
                .required_evidence_domains
            )
        )
    else:
        assert (
            len(outcome.resolved_prefix)
            < len(
                resolution
                .coverage_identity
                .evaluation_record_policy_evidence_requirements_binding
                .policy_evidence_requirements
                .required_evidence_domains
            )
        )
        assert outcome.impediment is not None


def test_equal_reconstruction_has_value_equality() -> None:
    resolution = create_resolution()
    reconstructed = replace(
        resolution,
        coverage_identity=replace(resolution.coverage_identity),
        outcome=replace(resolution.outcome),
    )
    assert reconstructed == resolution
    assert reconstructed is not resolution


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    outcome = create_closure()
    with pytest.raises(
        TypeError,
        match=(
            "coverage_identity must be a "
            "SecurityAdmissionEvidenceCoverageIdentity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureResolution(
            coverage_identity=invalid_value,  # type: ignore[arg-type]
            outcome=outcome,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_outcome_requires_one_terminal_variant(
    invalid_value: object,
) -> None:
    closure = create_closure()
    coverage_identity = coverage_identity_for(closure)
    with pytest.raises(
        TypeError,
        match=(
            "outcome must be one complete coverage closure "
            "or closure blockage"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureResolution(
            coverage_identity=coverage_identity,
            outcome=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "factory",
    (
        create_closure,
        create_media_type_first_blockage,
        create_byte_length_first_blockage,
        create_media_type_prefix_blockage,
        create_byte_length_prefix_blockage,
    ),
)
def test_different_coverage_occurrence_is_rejected(
    factory: ClosureFactory,
) -> None:
    outcome = factory()
    coverage_identity = coverage_identity_for(outcome)
    different_coverage = replace(
        coverage_identity,
        coverage_version=coverage_identity.coverage_version + 1,
    )
    with pytest.raises(
        ValueError,
        match=(
            "closure outcome must use the exact coverage identity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureResolution(
            coverage_identity=different_coverage,
            outcome=outcome,
        )


def test_single_outcome_field_prevents_simultaneous_terminal_states() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureResolution
        )
    ) == (
        "coverage_identity",
        "outcome",
    )


def test_assessment_and_decision_fields_are_absent() -> None:
    resolution = create_resolution()
    for field_name in (
        "assessment",
        "assessments",
        "classification",
        "admission_status",
        "admission_decision",
        "rejection",
        "authority",
    ):
        assert not hasattr(resolution, field_name)


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageClosureResolution
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
        SecurityAdmissionEvidenceCoverageClosureResolution
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
