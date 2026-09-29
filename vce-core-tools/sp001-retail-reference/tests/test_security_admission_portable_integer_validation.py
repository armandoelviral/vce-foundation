import ast
import inspect

import pytest

from sp001.services.security_admission_portable_integer_validation import (
    SECURITY_ADMISSION_PORTABLE_UINT64_MAX,
    validate_security_admission_non_negative_uint64,
    validate_security_admission_positive_uint64,
)


MAX_UINT64 = 18_446_744_073_709_551_615


def test_portable_uint64_max_is_exact() -> None:
    assert SECURITY_ADMISSION_PORTABLE_UINT64_MAX == MAX_UINT64
    assert SECURITY_ADMISSION_PORTABLE_UINT64_MAX == (1 << 64) - 1


@pytest.mark.parametrize(
    "value",
    (
        1,
        2,
        MAX_UINT64,
    ),
)
def test_positive_uint64_accepts_portable_values(
    value: int,
) -> None:
    assert (
        validate_security_admission_positive_uint64(
            value=value,
            field="coverage_version",
        )
        == value
    )


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
        -MAX_UINT64,
    ),
)
def test_positive_uint64_rejects_non_positive_values(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="coverage_version must be positive",
    ):
        validate_security_admission_positive_uint64(
            value=value,
            field="coverage_version",
        )


def test_positive_uint64_rejects_overflow() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "coverage_version must not exceed "
            "portable uint64 maximum"
        ),
    ):
        validate_security_admission_positive_uint64(
            value=MAX_UINT64 + 1,
            field="coverage_version",
        )


@pytest.mark.parametrize(
    "value",
    (
        0,
        1,
        MAX_UINT64,
    ),
)
def test_non_negative_uint64_accepts_portable_values(
    value: int,
) -> None:
    assert (
        validate_security_admission_non_negative_uint64(
            value=value,
            field="measured_byte_length",
        )
        == value
    )


@pytest.mark.parametrize(
    "value",
    (
        -1,
        -MAX_UINT64,
    ),
)
def test_non_negative_uint64_rejects_negative_values(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="measured_byte_length must be non-negative",
    ):
        validate_security_admission_non_negative_uint64(
            value=value,
            field="measured_byte_length",
        )


def test_non_negative_uint64_rejects_overflow() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "measured_byte_length must not exceed "
            "portable uint64 maximum"
        ),
    ):
        validate_security_admission_non_negative_uint64(
            value=MAX_UINT64 + 1,
            field="measured_byte_length",
        )


@pytest.mark.parametrize(
    "validator",
    (
        validate_security_admission_positive_uint64,
        validate_security_admission_non_negative_uint64,
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        True,
        False,
        1.0,
        "1",
        object(),
    ),
)
def test_value_requires_exact_integer_type(
    validator: object,
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="portable_value must be an integer",
    ):
        validator(  # type: ignore[operator]
            value=invalid_value,
            field="portable_value",
        )


@pytest.mark.parametrize(
    "validator",
    (
        validate_security_admission_positive_uint64,
        validate_security_admission_non_negative_uint64,
    ),
)
@pytest.mark.parametrize(
    "invalid_field",
    (
        None,
        1,
        True,
        object(),
    ),
)
def test_field_requires_string(
    validator: object,
    invalid_field: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="field must be a string",
    ):
        validator(  # type: ignore[operator]
            value=1,
            field=invalid_field,
        )


@pytest.mark.parametrize(
    "validator",
    (
        validate_security_admission_positive_uint64,
        validate_security_admission_non_negative_uint64,
    ),
)
@pytest.mark.parametrize(
    "invalid_field",
    (
        "",
        " ",
        "\t",
        "\n",
    ),
)
def test_field_must_not_be_blank(
    validator: object,
    invalid_field: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="field must not be blank",
    ):
        validator(  # type: ignore[operator]
            value=1,
            field=invalid_field,
        )


@pytest.mark.parametrize(
    "validator,value",
    (
        (
            validate_security_admission_positive_uint64,
            0,
        ),
        (
            validate_security_admission_non_negative_uint64,
            -1,
        ),
    ),
)
def test_field_name_is_preserved_in_validation_message(
    validator: object,
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match=r"candidate_version must",
    ):
        validator(  # type: ignore[operator]
            value=value,
            field="candidate_version",
        )


def test_module_defines_validation_only() -> None:
    module = inspect.getmodule(
        validate_security_admission_positive_uint64
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
        "validate_security_admission_positive_uint64",
        "validate_security_admission_non_negative_uint64",
        "_validate_field_name",
    }


def test_module_imports_no_external_capability() -> None:
    module = inspect.getmodule(
        validate_security_admission_positive_uint64
    )
    assert module is not None

    tree = ast.parse(inspect.getsource(module))
    imports = tuple(
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    )

    assert imports == ()
