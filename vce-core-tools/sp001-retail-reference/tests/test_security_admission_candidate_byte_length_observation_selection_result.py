import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone

import pytest

from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_basis import (
    SecurityAdmissionCandidateByteLengthObservationResolutionBasis,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_selection_result import (
    SecurityAdmissionCandidateByteLengthObservationSelectionResult,
)
from tests.test_security_admission_candidate_byte_length_observation_resolution_basis import (
    create_basis,
)
from tests.test_security_admission_policy_verification_procedure_authority_order import (
    create_order,
)


def create_result(
) -> SecurityAdmissionCandidateByteLengthObservationSelectionResult:
    basis = create_basis()
    first, second = basis.observation_set.observations
    second = replace(
        second,
        observed_at=first.observed_at + timedelta(seconds=1),
    )
    observation_set = replace(
        basis.observation_set,
        observations=(first, second),
    )
    basis = replace(basis, observation_set=observation_set)
    return SecurityAdmissionCandidateByteLengthObservationSelectionResult(
        result_id="selection-001",
        result_version=1,
        resolution_basis=basis,
        selected_observation=second,
        resolved_at=second.observed_at + timedelta(seconds=1),
    )


def test_fields_are_exact() -> None:
    result_fields = fields(
        SecurityAdmissionCandidateByteLengthObservationSelectionResult
    )
    assert tuple(field.name for field in result_fields) == (
        "result_id",
        "result_version",
        "resolution_basis",
        "selected_observation",
        "resolved_at",
    )
    assert (
        result_fields[2].type
        is SecurityAdmissionCandidateByteLengthObservationResolutionBasis
    )
    assert (
        result_fields[3].type
        is SecurityAdmissionCandidateMeasuredByteLengthObservation
    )
    assert result_fields[4].type is datetime


def test_result_is_immutable_and_slotted() -> None:
    result = create_result()
    assert not hasattr(result, "__dict__")
    with pytest.raises(FrozenInstanceError):
        result.result_version = 2  # type: ignore[misc]


def test_exact_references_are_preserved() -> None:
    result = create_result()
    basis = result.resolution_basis
    selected = result.selected_observation
    reconstructed = (
        SecurityAdmissionCandidateByteLengthObservationSelectionResult(
            result_id=result.result_id,
            result_version=result.result_version,
            resolution_basis=basis,
            selected_observation=selected,
            resolved_at=result.resolved_at,
        )
    )
    assert reconstructed.resolution_basis is basis
    assert reconstructed.selected_observation is selected


def test_equal_reconstruction_has_value_equality() -> None:
    result = create_result()
    reconstructed = replace(result)
    assert reconstructed == result
    assert reconstructed is not result


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_result_id_requires_string(invalid_value: object) -> None:
    with pytest.raises(TypeError, match="result_id must be a string"):
        replace(
            create_result(),
            result_id=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", ("", " ", "\t", "\n"))
def test_result_id_must_not_be_blank(invalid_value: str) -> None:
    with pytest.raises(ValueError, match="result_id must not be blank"):
        replace(create_result(), result_id=invalid_value)


@pytest.mark.parametrize(
    "invalid_value",
    (None, True, False, 1.0, "1"),
)
def test_result_version_requires_strict_integer(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="result_version must be an integer",
    ):
        replace(
            create_result(),
            result_version=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (0, -1))
def test_result_version_must_be_positive(invalid_value: int) -> None:
    with pytest.raises(
        ValueError,
        match="result_version must be positive",
    ):
        replace(create_result(), result_version=invalid_value)


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_resolution_basis_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "resolution_basis must be a "
            "SecurityAdmissionCandidateByteLengthObservationResolutionBasis"
        ),
    ):
        replace(
            create_result(),
            resolution_basis=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_selected_observation_requires_nominal_type(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "selected_observation must be a "
            "SecurityAdmissionCandidateMeasuredByteLengthObservation"
        ),
    ):
        replace(
            create_result(),
            selected_observation=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_resolved_at_requires_datetime(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="resolved_at must be a datetime",
    ):
        replace(
            create_result(),
            resolved_at=invalid_value,  # type: ignore[arg-type]
        )


def test_resolved_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        ValueError,
        match="resolved_at must be timezone-aware",
    ):
        replace(
            create_result(),
            resolved_at=datetime(2026, 9, 22),
        )


def test_selected_observation_must_belong_to_basis() -> None:
    result = create_result()
    outsider = replace(
        result.selected_observation,
        observation_id="observation-999",
    )
    with pytest.raises(
        ValueError,
        match="selected_observation must belong to the resolution basis",
    ):
        replace(result, selected_observation=outsider)


def test_equal_reconstructed_member_is_permitted() -> None:
    result = create_result()
    reconstructed_selected = replace(result.selected_observation)
    preserved = replace(
        result,
        selected_observation=reconstructed_selected,
    )
    assert preserved == result
    assert preserved.selected_observation is reconstructed_selected


def test_conflicting_normative_procedure_identities_are_rejected() -> None:
    result = create_result()
    first, second = result.resolution_basis.observation_set.observations
    conflicting_identity = replace(
        second.verification_procedure_identity,
        verifier_version="conflicting-version",
    )
    conflicting_second = replace(
        second,
        verification_procedure_identity=conflicting_identity,
    )
    conflicting_set = replace(
        result.resolution_basis.observation_set,
        observations=(first, conflicting_second),
    )
    conflicting_basis = replace(
        result.resolution_basis,
        observation_set=conflicting_set,
    )
    with pytest.raises(
        ValueError,
        match="conflicting normative procedure identities",
    ):
        replace(
            result,
            resolution_basis=conflicting_basis,
            selected_observation=first,
        )


def test_unranked_procedure_is_rejected() -> None:
    result = create_result()
    first, second = result.resolution_basis.observation_set.observations
    unranked_identity = replace(
        create_order().verification_procedure_identities[1],
        verification_procedure_id="unranked-procedure",
    )
    unranked_second = replace(
        second,
        verification_procedure_identity=unranked_identity,
    )
    unranked_set = replace(
        result.resolution_basis.observation_set,
        observations=(first, unranked_second),
    )
    unranked_basis = replace(
        result.resolution_basis,
        observation_set=unranked_set,
    )
    with pytest.raises(
        ValueError,
        match="unranked verification procedure",
    ):
        replace(
            result,
            resolution_basis=unranked_basis,
            selected_observation=first,
        )


def test_higher_authority_precedes_more_recent_lower_authority() -> None:
    result = create_result()
    first, second = result.resolution_basis.observation_set.observations
    primary_identity = first.verification_procedure_identity
    lower_identity = (
        create_order().verification_procedure_identities[1]
    )
    lower_observation = replace(
        second,
        verification_procedure_identity=lower_identity,
        observed_at=first.observed_at + timedelta(hours=1),
    )
    observation_set = replace(
        result.resolution_basis.observation_set,
        observations=(first, lower_observation),
    )
    authority_order = replace(
        result.resolution_basis.authority_order,
        verification_procedure_identities=(
            primary_identity,
            lower_identity,
        ),
    )
    basis = replace(
        result.resolution_basis,
        observation_set=observation_set,
        authority_order=authority_order,
    )
    selected = replace(
        result,
        resolution_basis=basis,
        selected_observation=first,
        resolved_at=lower_observation.observed_at + timedelta(seconds=1),
    )
    assert selected.selected_observation is first


def test_latest_observation_wins_within_same_procedure() -> None:
    result = create_result()
    first, second = result.resolution_basis.observation_set.observations
    assert first.verification_procedure_identity == (
        second.verification_procedure_identity
    )
    assert second.observed_at > first.observed_at
    assert result.selected_observation is second


def test_older_observation_from_highest_authority_is_rejected() -> None:
    result = create_result()
    older = result.resolution_basis.observation_set.observations[0]
    with pytest.raises(
        ValueError,
        match=(
            "selected_observation must be the highest-authority "
            "latest observation"
        ),
    ):
        replace(result, selected_observation=older)


def test_tied_latest_observations_are_rejected() -> None:
    result = create_result()
    first, second = result.resolution_basis.observation_set.observations
    tied_second = replace(second, observed_at=first.observed_at)
    tied_set = replace(
        result.resolution_basis.observation_set,
        observations=(first, tied_second),
    )
    tied_basis = replace(
        result.resolution_basis,
        observation_set=tied_set,
    )
    with pytest.raises(
        ValueError,
        match="highest-authority latest observation must be unique",
    ):
        replace(
            result,
            resolution_basis=tied_basis,
            selected_observation=first,
        )


def test_resolved_at_must_not_precede_selected_observation() -> None:
    result = create_result()
    with pytest.raises(
        ValueError,
        match="resolved_at must not precede selected observation",
    ):
        replace(
            result,
            resolved_at=(
                result.selected_observation.observed_at
                - timedelta(microseconds=1)
            ),
        )


def test_equal_resolved_and_observed_timestamp_is_permitted() -> None:
    result = create_result()
    preserved = replace(
        result,
        resolved_at=result.selected_observation.observed_at,
    )
    assert preserved.resolved_at == preserved.selected_observation.observed_at


def test_result_identity_basis_selection_and_time_participate_in_value() -> None:
    result = create_result()
    assert replace(result, result_id="selection-002") != result
    assert replace(result, result_version=2) != result
    assert replace(
        result,
        resolution_basis=replace(
            result.resolution_basis,
            observation_set=replace(
                result.resolution_basis.observation_set,
                observation_set_version=2,
            ),
        ),
    ) != result
    assert replace(
        result,
        resolved_at=result.resolved_at + timedelta(seconds=1),
    ) != result


def test_admission_decision_and_coverage_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthObservationSelectionResult
        )
    }
    assert names.isdisjoint({
        "coverage_status",
        "decision",
        "admitted",
        "rejected",
        "authorized",
        "authorization",
        "quarantine",
        "retention",
    })


def test_contract_defines_validation_only() -> None:
    module = inspect.getmodule(
        SecurityAdmissionCandidateByteLengthObservationSelectionResult
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
        SecurityAdmissionCandidateByteLengthObservationSelectionResult
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "datetime", "sp001"}
