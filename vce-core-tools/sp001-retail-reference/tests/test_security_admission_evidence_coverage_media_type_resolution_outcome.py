import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace
from typing import Callable

import pytest

from sp001.contracts.security_admission_evidence_coverage_identity import (
    SecurityAdmissionEvidenceCoverageIdentity,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_closure_impediment import (
    SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_observation_selection_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_observation_selection_indeterminate_comparison_result_binding import (
    SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
)
from sp001.contracts.security_admission_evidence_coverage_media_type_resolution_outcome import (
    SecurityAdmissionEvidenceCoverageMediaTypeOutcomeValue,
    SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome,
)
from tests.test_security_admission_evidence_coverage_media_type_closure_impediment import (
    create_impediment,
)
from tests.test_security_admission_evidence_coverage_media_type_observation_selection_comparison_result_binding import (
    create_binding as create_conclusive_binding,
)
from tests.test_security_admission_evidence_coverage_media_type_observation_selection_indeterminate_comparison_result_binding import (
    create_binding as create_indeterminate_binding,
)


OutcomeFactory = Callable[
    [],
    SecurityAdmissionEvidenceCoverageMediaTypeOutcomeValue,
]


def coverage_identity_for(
    outcome: SecurityAdmissionEvidenceCoverageMediaTypeOutcomeValue,
) -> SecurityAdmissionEvidenceCoverageIdentity:
    if isinstance(
        outcome,
        SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
    ):
        return (
            outcome.evidence_coverage_media_type_comparison_result_binding
            .coverage_identity
        )
    if isinstance(
        outcome,
        SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionIndeterminateComparisonResultBinding,
    ):
        return (
            outcome
            .evidence_coverage_indeterminate_media_type_comparison_result_binding
            .coverage_identity
        )
    return outcome.coverage_identity


def create_outcome(
    factory: OutcomeFactory = create_conclusive_binding,
) -> SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome:
    value = factory()
    return SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome(
        coverage_identity=coverage_identity_for(value),
        outcome=value,
    )


def test_fields_are_exact() -> None:
    outcome_fields = fields(
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome
    )
    assert tuple(field.name for field in outcome_fields) == (
        "coverage_identity",
        "outcome",
    )
    assert (
        outcome_fields[0].type
        is SecurityAdmissionEvidenceCoverageIdentity
    )
    assert (
        outcome_fields[1].type
        == SecurityAdmissionEvidenceCoverageMediaTypeOutcomeValue
    )


def test_resolution_outcome_is_immutable_and_slotted() -> None:
    resolution_outcome = create_outcome()
    assert not hasattr(resolution_outcome, "__dict__")
    with pytest.raises(FrozenInstanceError):
        resolution_outcome.outcome = create_impediment()  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    resolution_outcome = create_outcome()
    coverage = resolution_outcome.coverage_identity
    value = resolution_outcome.outcome
    reconstructed = (
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome(
            coverage_identity=coverage,
            outcome=value,
        )
    )
    assert reconstructed.coverage_identity is coverage
    assert reconstructed.outcome is value


@pytest.mark.parametrize(
    "factory",
    (
        create_conclusive_binding,
        create_indeterminate_binding,
        create_impediment,
    ),
)
def test_each_nominal_variant_is_preserved(
    factory: OutcomeFactory,
) -> None:
    value = factory()
    resolution_outcome = (
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome(
            coverage_identity=coverage_identity_for(value),
            outcome=value,
        )
    )
    assert resolution_outcome.outcome is value


@pytest.mark.parametrize(
    "factory",
    (
        create_conclusive_binding,
        create_indeterminate_binding,
        create_impediment,
    ),
)
def test_each_variant_preserves_complete_lineage(
    factory: OutcomeFactory,
) -> None:
    resolution_outcome = create_outcome(factory)
    value = resolution_outcome.outcome
    assert (
        resolution_outcome.coverage_identity
        is coverage_identity_for(value)
    )
    if isinstance(
        value,
        SecurityAdmissionEvidenceCoverageMediaTypeClosureImpediment,
    ):
        assert value.resolution_conflict_result.conflicting_observations
    elif isinstance(
        value,
        SecurityAdmissionEvidenceCoverageMediaTypeObservationSelectionComparisonResultBinding,
    ):
        assert (
            value
            .evaluation_record_media_type_observation_selection_comparison_result_binding
            .observation_selection_comparison_result_binding
            .observation_selection_comparison_basis_binding
            .observation_selection_result
            .selected_observation
            is not None
        )
    else:
        assert (
            value
            .evaluation_record_media_type_observation_selection_indeterminate_comparison_result_binding
            .observation_selection_indeterminate_comparison_result_binding
            .observation_selection_comparison_basis_binding
            .observation_selection_result
            .selected_observation
            is not None
        )


def test_equal_reconstruction_has_value_equality() -> None:
    resolution_outcome = create_outcome()
    reconstructed = replace(
        resolution_outcome,
        coverage_identity=replace(
            resolution_outcome.coverage_identity
        ),
        outcome=replace(resolution_outcome.outcome),
    )
    assert reconstructed == resolution_outcome
    assert reconstructed is not resolution_outcome


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_coverage_identity_requires_nominal_type(
    invalid_value: object,
) -> None:
    value = create_conclusive_binding()
    with pytest.raises(
        TypeError,
        match=(
            "coverage_identity must be a "
            "SecurityAdmissionEvidenceCoverageIdentity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome(
            coverage_identity=invalid_value,  # type: ignore[arg-type]
            outcome=value,
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_outcome_requires_one_nominal_variant(
    invalid_value: object,
) -> None:
    value = create_conclusive_binding()
    coverage = coverage_identity_for(value)
    with pytest.raises(
        TypeError,
        match=(
            "outcome must be one media-type conclusive result, "
            "indeterminate result or closure impediment"
        ),
    ):
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome(
            coverage_identity=coverage,
            outcome=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "factory",
    (
        create_conclusive_binding,
        create_indeterminate_binding,
        create_impediment,
    ),
)
def test_different_coverage_occurrence_is_rejected(
    factory: OutcomeFactory,
) -> None:
    value = factory()
    coverage = coverage_identity_for(value)
    different_coverage = replace(
        coverage,
        coverage_version=coverage.coverage_version + 1,
    )
    with pytest.raises(
        ValueError,
        match=(
            "media-type outcome must use the exact coverage identity"
        ),
    ):
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome(
            coverage_identity=different_coverage,
            outcome=value,
        )


def test_single_outcome_field_prevents_multiple_simultaneous_variants() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome
        )
    ) == (
        "coverage_identity",
        "outcome",
    )


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome
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
        SecurityAdmissionEvidenceCoverageMediaTypeResolutionOutcome
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "sp001"}
