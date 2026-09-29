import ast
import inspect
from collections.abc import Callable
from dataclasses import fields, replace

import pytest

from sp001.services.security_admission_portable_contract_integer_validation import (
    validate_security_admission_portable_contract_integers,
)
from sp001.services.security_admission_portable_integer_validation import (
    SECURITY_ADMISSION_PORTABLE_UINT64_MAX,
)
from tests.test_security_admission_candidate_byte_length_comparison_basis import (
    create_basis as create_byte_length_comparison_basis,
)
from tests.test_security_admission_candidate_byte_length_comparison_result import (
    create_result as create_byte_length_comparison_result,
)
from tests.test_security_admission_candidate_byte_length_observation_resolution_conflict_result import (
    create_normative_conflict as create_byte_length_conflict_result,
)
from tests.test_security_admission_candidate_byte_length_observation_selection_result import (
    create_result as create_byte_length_selection_result,
)
from tests.test_security_admission_candidate_byte_length_observation_set import (
    create_set as create_byte_length_observation_set,
)
from tests.test_security_admission_candidate_declared_byte_length import (
    create_declaration as create_declared_byte_length,
)
from tests.test_security_admission_candidate_detected_media_type_observation import (
    create_observation as create_detected_media_type_observation,
)
from tests.test_security_admission_candidate_identity import (
    create_identity as create_candidate_identity,
)
from tests.test_security_admission_candidate_indeterminate_byte_length_comparison_result import (
    create_result as create_indeterminate_byte_length_result,
)
from tests.test_security_admission_candidate_indeterminate_media_type_comparison_result import (
    create_result as create_indeterminate_media_type_result,
)
from tests.test_security_admission_candidate_measured_byte_length_observation import (
    create_observation as create_measured_byte_length_observation,
)
from tests.test_security_admission_candidate_media_type_comparison_basis import (
    create_basis as create_media_type_comparison_basis,
)
from tests.test_security_admission_candidate_media_type_comparison_result import (
    create_result as create_media_type_comparison_result,
)
from tests.test_security_admission_candidate_media_type_observation_resolution_conflict_result import (
    create_normative_conflict as create_media_type_conflict_result,
)
from tests.test_security_admission_candidate_media_type_observation_selection_result import (
    create_result as create_media_type_selection_result,
)
from tests.test_security_admission_candidate_media_type_observation_set import (
    create_set as create_media_type_observation_set,
)
from tests.test_security_admission_candidate_metadata_identity import (
    create_metadata_identity,
)
from tests.test_security_admission_evaluation_identity import (
    create_identity as create_evaluation_identity,
)
from tests.test_security_admission_evidence_coverage_identity import (
    create_identity as create_coverage_identity,
)
from tests.test_security_admission_policy_identity import (
    create_identity as create_policy_identity,
)


ContractFactory = Callable[[], object]
IntegerFieldCase = tuple[ContractFactory, str]


SUPPORTED_CONTRACT_FACTORIES: tuple[ContractFactory, ...] = (
    create_byte_length_comparison_basis,
    create_byte_length_comparison_result,
    create_byte_length_conflict_result,
    create_byte_length_selection_result,
    create_byte_length_observation_set,
    create_declared_byte_length,
    create_detected_media_type_observation,
    create_candidate_identity,
    create_indeterminate_byte_length_result,
    create_indeterminate_media_type_result,
    create_measured_byte_length_observation,
    create_media_type_comparison_basis,
    create_media_type_comparison_result,
    create_media_type_conflict_result,
    create_media_type_selection_result,
    create_media_type_observation_set,
    create_metadata_identity,
    create_evaluation_identity,
    create_coverage_identity,
    create_policy_identity,
)


INTEGER_FIELD_CASES: tuple[IntegerFieldCase, ...] = (
    (
        create_byte_length_comparison_basis,
        "comparison_scheme_version",
    ),
    (
        create_byte_length_comparison_result,
        "result_version",
    ),
    (
        create_byte_length_conflict_result,
        "result_version",
    ),
    (
        create_byte_length_selection_result,
        "result_version",
    ),
    (
        create_byte_length_observation_set,
        "observation_set_version",
    ),
    (
        create_declared_byte_length,
        "declared_byte_length",
    ),
    (
        create_detected_media_type_observation,
        "observation_version",
    ),
    (
        create_candidate_identity,
        "candidate_version",
    ),
    (
        create_indeterminate_byte_length_result,
        "result_version",
    ),
    (
        create_indeterminate_media_type_result,
        "result_version",
    ),
    (
        create_measured_byte_length_observation,
        "observation_version",
    ),
    (
        create_measured_byte_length_observation,
        "measured_byte_length",
    ),
    (
        create_media_type_comparison_basis,
        "comparison_scheme_version",
    ),
    (
        create_media_type_comparison_result,
        "result_version",
    ),
    (
        create_media_type_conflict_result,
        "result_version",
    ),
    (
        create_media_type_selection_result,
        "result_version",
    ),
    (
        create_media_type_observation_set,
        "observation_set_version",
    ),
    (
        create_metadata_identity,
        "metadata_schema_version",
    ),
    (
        create_evaluation_identity,
        "evaluation_version",
    ),
    (
        create_coverage_identity,
        "coverage_version",
    ),
    (
        create_policy_identity,
        "admission_policy_version",
    ),
)


@pytest.mark.parametrize(
    "factory",
    SUPPORTED_CONTRACT_FACTORIES,
)
def test_each_supported_contract_is_accepted(
    factory: ContractFactory,
) -> None:
    value = factory()

    assert (
        validate_security_admission_portable_contract_integers(
            value=value,
        )
        is None
    )


@pytest.mark.parametrize(
    "factory,field",
    INTEGER_FIELD_CASES,
)
def test_each_integer_field_accepts_portable_uint64_maximum(
    factory: ContractFactory,
    field: str,
) -> None:
    value = replace(
        factory(),
        **{
            field: SECURITY_ADMISSION_PORTABLE_UINT64_MAX,
        },
    )

    assert (
        validate_security_admission_portable_contract_integers(
            value=value,
        )
        is None
    )


@pytest.mark.parametrize(
    "factory,field",
    INTEGER_FIELD_CASES,
)
def test_each_integer_field_rejects_uint64_overflow(
    factory: ContractFactory,
    field: str,
) -> None:
    value = replace(
        factory(),
        **{
            field: SECURITY_ADMISSION_PORTABLE_UINT64_MAX + 1,
        },
    )

    with pytest.raises(
        ValueError,
        match=(
            rf"{field} must not exceed "
            r"portable uint64 maximum"
        ),
    ):
        validate_security_admission_portable_contract_integers(
            value=value,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        object(),
    ),
)
def test_unsupported_nominal_value_is_rejected(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "value must be a supported security-admission "
            "integer-bearing contract"
        ),
    ):
        validate_security_admission_portable_contract_integers(
            value=invalid_value,
        )


def test_inventory_contains_exactly_twenty_contract_occurrences() -> None:
    values = tuple(
        factory()
        for factory in SUPPORTED_CONTRACT_FACTORIES
    )

    assert len(values) == 20
    assert len({type(value) for value in values}) == 20


def test_inventory_contains_exactly_twenty_one_integer_fields() -> None:
    assert len(INTEGER_FIELD_CASES) == 21

    discovered = sum(
        1
        for factory in SUPPORTED_CONTRACT_FACTORIES
        for field in fields(factory())
        if field.type is int
    )

    assert discovered == 21


def test_every_discovered_integer_field_has_one_validation_case() -> None:
    expected = {
        (type(value), field.name)
        for factory in SUPPORTED_CONTRACT_FACTORIES
        for value in (factory(),)
        for field in fields(value)
        if field.type is int
    }
    actual = {
        (type(factory()), field)
        for factory, field in INTEGER_FIELD_CASES
    }

    assert actual == expected


def test_service_defines_validation_only() -> None:
    module = inspect.getmodule(
        validate_security_admission_portable_contract_integers
    )
    assert module is not None

    tree = ast.parse(inspect.getsource(module))
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    }

    assert functions == {
        "validate_security_admission_portable_contract_integers",
    }


def test_service_uses_no_dynamic_field_access() -> None:
    module = inspect.getmodule(
        validate_security_admission_portable_contract_integers
    )
    assert module is not None

    tree = ast.parse(inspect.getsource(module))
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
        )
    }

    assert "getattr" not in called_names
    assert "vars" not in called_names
    assert "eval" not in called_names
    assert "exec" not in called_names


def test_service_imports_only_internal_capabilities() -> None:
    module = inspect.getmodule(
        validate_security_admission_portable_contract_integers
    )
    assert module is not None

    tree = ast.parse(inspect.getsource(module))
    roots = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
        )
    }

    assert roots == {"sp001"}
