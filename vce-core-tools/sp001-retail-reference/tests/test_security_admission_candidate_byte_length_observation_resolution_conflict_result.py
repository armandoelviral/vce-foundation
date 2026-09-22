import ast
import inspect

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta

import pytest

from sp001.contracts.security_admission_candidate_measured_byte_length_observation import (
    SecurityAdmissionCandidateMeasuredByteLengthObservation,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_basis import (
    SecurityAdmissionCandidateByteLengthObservationResolutionBasis,
)
from sp001.contracts.security_admission_candidate_byte_length_observation_resolution_conflict_result import (
    SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult,
    SecurityAdmissionByteLengthObservationResolutionConflictReason,
)
from tests.test_security_admission_candidate_byte_length_observation_resolution_basis import (
    create_basis,
)
from tests.test_security_admission_candidate_byte_length_observation_selection_result import (
    create_result as create_selection_result,
)
from tests.test_security_admission_policy_verification_procedure_authority_order import (
    create_order,
)


def create_normative_conflict(
) -> SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult:
    basis = create_basis()
    first, second = basis.observation_set.observations
    conflicting_identity = (
        basis.authority_order.verification_procedure_identities[1]
    )
    conflicting_second = replace(
        second,
        verification_procedure_identity=conflicting_identity,
        observed_at=first.observed_at + timedelta(seconds=1),
    )
    observation_set = replace(
        basis.observation_set,
        observations=(first, conflicting_second),
    )
    basis = replace(basis, observation_set=observation_set)
    return (
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult(
            result_id="conflict-001",
            result_version=1,
            resolution_basis=basis,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .CONFLICTING_NORMATIVE_PROCEDURE_IDENTITIES
            ),
            conflicting_observations=(first, conflicting_second),
            determined_at=(
                conflicting_second.observed_at + timedelta(seconds=1)
            ),
        )
    )


def create_unranked_conflict(
) -> SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult:
    basis = create_basis()
    first, second = basis.observation_set.observations
    unranked_identity = (
        create_order().verification_procedure_identities[1]
    )
    unranked_second = replace(
        second,
        verification_procedure_identity=unranked_identity,
        observed_at=first.observed_at + timedelta(seconds=1),
    )
    observation_set = replace(
        basis.observation_set,
        observations=(first, unranked_second),
    )
    basis = replace(basis, observation_set=observation_set)
    return (
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult(
            result_id="conflict-002",
            result_version=1,
            resolution_basis=basis,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .UNRANKED_VERIFICATION_PROCEDURE
            ),
            conflicting_observations=(unranked_second,),
            determined_at=unranked_second.observed_at,
        )
    )


def create_timestamp_tie(
) -> SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult:
    basis = create_basis()
    observations = basis.observation_set.observations
    return (
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult(
            result_id="conflict-003",
            result_version=1,
            resolution_basis=basis,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .LATEST_TIMESTAMP_TIE
            ),
            conflicting_observations=observations,
            determined_at=observations[-1].observed_at,
        )
    )


def test_fields_are_exact() -> None:
    result_fields = fields(
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult
    )
    assert tuple(field.name for field in result_fields) == (
        "result_id",
        "result_version",
        "resolution_basis",
        "reason",
        "conflicting_observations",
        "determined_at",
    )
    assert (
        result_fields[2].type
        is SecurityAdmissionCandidateByteLengthObservationResolutionBasis
    )
    assert (
        result_fields[3].type
        is SecurityAdmissionByteLengthObservationResolutionConflictReason
    )
    assert result_fields[5].type is datetime


def test_reason_set_is_exact() -> None:
    assert tuple(
        SecurityAdmissionByteLengthObservationResolutionConflictReason
    ) == (
        SecurityAdmissionByteLengthObservationResolutionConflictReason
        .CONFLICTING_NORMATIVE_PROCEDURE_IDENTITIES,
        SecurityAdmissionByteLengthObservationResolutionConflictReason
        .UNRANKED_VERIFICATION_PROCEDURE,
        SecurityAdmissionByteLengthObservationResolutionConflictReason
        .LATEST_TIMESTAMP_TIE,
    )


def test_result_is_immutable_and_slotted() -> None:
    result = create_normative_conflict()
    assert not hasattr(result, "__dict__")
    with pytest.raises(FrozenInstanceError):
        result.result_version = 2  # type: ignore[misc]


@pytest.mark.parametrize(
    "factory",
    (
        create_normative_conflict,
        create_unranked_conflict,
        create_timestamp_tie,
    ),
)
def test_each_conflict_preserves_exact_basis_and_observations(
    factory: object,
) -> None:
    result = factory()  # type: ignore[operator]
    assert result.resolution_basis is not None
    basis_observations = result.resolution_basis.observation_set.observations
    for observation in result.conflicting_observations:
        assert any(
            observation is basis_observation
            for basis_observation in basis_observations
        )


def test_equal_reconstruction_has_value_equality() -> None:
    result = create_normative_conflict()
    reconstructed = replace(result)
    assert reconstructed == result
    assert reconstructed is not result


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_result_id_requires_string(invalid_value: object) -> None:
    with pytest.raises(TypeError, match="result_id must be a string"):
        replace(
            create_normative_conflict(),
            result_id=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", ("", " ", "\t", "\n"))
def test_result_id_must_not_be_blank(invalid_value: str) -> None:
    with pytest.raises(ValueError, match="result_id must not be blank"):
        replace(create_normative_conflict(), result_id=invalid_value)


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
            create_normative_conflict(),
            result_version=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (0, -1))
def test_result_version_must_be_positive(invalid_value: int) -> None:
    with pytest.raises(
        ValueError,
        match="result_version must be positive",
    ):
        replace(
            create_normative_conflict(),
            result_version=invalid_value,
        )


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
            create_normative_conflict(),
            resolution_basis=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_value",
    (None, "LATEST_TIMESTAMP_TIE", 1, object()),
)
def test_reason_requires_nominal_type(invalid_value: object) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "reason must be a "
            "SecurityAdmissionByteLengthObservationResolutionConflictReason"
        ),
    ):
        replace(
            create_normative_conflict(),
            reason=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, [], {}, set()))
def test_conflicting_observations_require_tuple(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="conflicting_observations must be an immutable tuple",
    ):
        replace(
            create_normative_conflict(),
            conflicting_observations=invalid_value,  # type: ignore[arg-type]
        )


def test_conflicting_observations_must_not_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="conflicting_observations must not be empty",
    ):
        replace(
            create_normative_conflict(),
            conflicting_observations=(),
        )


def test_conflicting_observation_requires_nominal_type() -> None:
    with pytest.raises(
        TypeError,
        match="conflicting_observations must contain",
    ):
        replace(
            create_normative_conflict(),
            conflicting_observations=(object(),),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("invalid_value", (None, 1, True, object()))
def test_determined_at_requires_datetime(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="determined_at must be a datetime",
    ):
        replace(
            create_normative_conflict(),
            determined_at=invalid_value,  # type: ignore[arg-type]
        )


def test_determined_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        ValueError,
        match="determined_at must be timezone-aware",
    ):
        replace(
            create_normative_conflict(),
            determined_at=datetime(2026, 9, 22),
        )


def test_normative_conflict_reason_must_be_truthful() -> None:
    result = create_normative_conflict()
    with pytest.raises(
        ValueError,
        match="reason must identify the first applicable logical conflict",
    ):
        replace(
            result,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .UNRANKED_VERIFICATION_PROCEDURE
            ),
        )


def test_unranked_conflict_reason_must_be_truthful() -> None:
    result = create_unranked_conflict()
    with pytest.raises(
        ValueError,
        match="reason must identify the first applicable logical conflict",
    ):
        replace(
            result,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .LATEST_TIMESTAMP_TIE
            ),
        )


def test_timestamp_tie_reason_must_be_truthful() -> None:
    result = create_timestamp_tie()
    with pytest.raises(
        ValueError,
        match="reason must identify the first applicable logical conflict",
    ):
        replace(
            result,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .UNRANKED_VERIFICATION_PROCEDURE
            ),
        )


def test_conflicting_observations_must_be_exact() -> None:
    result = create_normative_conflict()
    with pytest.raises(
        ValueError,
        match="conflicting_observations must exactly identify",
    ):
        replace(
            result,
            conflicting_observations=(
                result.conflicting_observations[0],
            ),
        )


def test_conflicting_observation_order_must_match_basis_order() -> None:
    result = create_normative_conflict()
    with pytest.raises(
        ValueError,
        match="conflicting_observations must exactly identify",
    ):
        replace(
            result,
            conflicting_observations=tuple(
                reversed(result.conflicting_observations)
            ),
        )


def test_normative_conflict_precedes_unranked_conflict() -> None:
    basis = create_basis()
    first, second = basis.observation_set.observations
    unranked_variant = replace(
        first.verification_procedure_identity,
        verifier_version="unranked-conflicting-version",
    )
    second = replace(
        second,
        verification_procedure_identity=unranked_variant,
        observed_at=first.observed_at + timedelta(seconds=1),
    )
    basis = replace(
        basis,
        observation_set=replace(
            basis.observation_set,
            observations=(first, second),
        ),
    )
    result = (
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult(
            result_id="precedence-001",
            result_version=1,
            resolution_basis=basis,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .CONFLICTING_NORMATIVE_PROCEDURE_IDENTITIES
            ),
            conflicting_observations=(first, second),
            determined_at=second.observed_at,
        )
    )
    assert result.reason is (
        SecurityAdmissionByteLengthObservationResolutionConflictReason
        .CONFLICTING_NORMATIVE_PROCEDURE_IDENTITIES
    )


def test_unranked_conflict_precedes_timestamp_tie() -> None:
    tie = create_timestamp_tie()
    first, second = tie.resolution_basis.observation_set.observations
    third = replace(
        second,
        observation_id="observation-003",
        verification_procedure_identity=(
            create_order().verification_procedure_identities[1]
        ),
    )
    basis = replace(
        tie.resolution_basis,
        observation_set=replace(
            tie.resolution_basis.observation_set,
            observations=(first, second, third),
        ),
    )
    result = (
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult(
            result_id="precedence-002",
            result_version=1,
            resolution_basis=basis,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .UNRANKED_VERIFICATION_PROCEDURE
            ),
            conflicting_observations=(third,),
            determined_at=third.observed_at,
        )
    )
    assert result.conflicting_observations == (third,)


def test_nonconflicting_basis_cannot_form_conflict_result() -> None:
    selection = create_selection_result()
    with pytest.raises(
        ValueError,
        match="resolution basis contains no logical selection conflict",
    ):
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult(
            result_id="not-a-conflict",
            result_version=1,
            resolution_basis=selection.resolution_basis,
            reason=(
                SecurityAdmissionByteLengthObservationResolutionConflictReason
                .LATEST_TIMESTAMP_TIE
            ),
            conflicting_observations=(
                selection.selected_observation,
            ),
            determined_at=selection.resolved_at,
        )


def test_determined_at_must_not_precede_all_resolution_evidence() -> None:
    result = create_normative_conflict()
    latest_evidence = max(
        observation.observed_at
        for observation
        in result.resolution_basis.observation_set.observations
    )
    with pytest.raises(
        ValueError,
        match="determined_at must not precede resolution evidence",
    ):
        replace(
            result,
            determined_at=latest_evidence - timedelta(microseconds=1),
        )


def test_equal_latest_evidence_and_determined_time_is_permitted() -> None:
    result = create_normative_conflict()
    latest_evidence = max(
        observation.observed_at
        for observation
        in result.resolution_basis.observation_set.observations
    )
    preserved = replace(result, determined_at=latest_evidence)
    assert preserved.determined_at == latest_evidence


def test_all_fields_participate_in_result_value() -> None:
    result = create_normative_conflict()
    assert replace(result, result_id="conflict-999") != result
    assert replace(result, result_version=2) != result
    assert replace(
        result,
        determined_at=result.determined_at + timedelta(seconds=1),
    ) != result


def test_admission_decision_and_coverage_fields_are_absent() -> None:
    names = {
        field.name
        for field in fields(
            SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult
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
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult
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
        SecurityAdmissionCandidateByteLengthObservationResolutionConflictResult
    )
    assert module is not None
    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert roots == {"dataclasses", "datetime", "enum", "sp001"}
