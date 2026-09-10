from dataclasses import FrozenInstanceError, fields, replace
import inspect

import pytest

from sp001.contracts.retail_commercial_currency_identity import (
    RetailCommercialCurrencyIdentity,
)


def create_currency_identity() -> RetailCommercialCurrencyIdentity:
    return RetailCommercialCurrencyIdentity(
        currency_code="MXN",
        currency_scheme_id="ISO-4217",
        currency_scheme_version=1,
    )


def test_currency_identity_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailCommercialCurrencyIdentity)
    ) == (
        "currency_code",
        "currency_scheme_id",
        "currency_scheme_version",
    )


def test_currency_identity_is_immutable() -> None:
    identity = create_currency_identity()

    with pytest.raises(FrozenInstanceError):
        identity.currency_code = "USD"  # type: ignore[misc]


def test_currency_identity_uses_slots() -> None:
    assert not hasattr(create_currency_identity(), "__dict__")


@pytest.mark.parametrize(
    "currency_code",
    ["MXN", "mxn", " mxn ", "US Dollar", "X-CUSTOM"],
)
def test_declared_currency_code_is_preserved_literally(
    currency_code: str,
) -> None:
    identity = replace(
        create_currency_identity(),
        currency_code=currency_code,
    )

    assert identity.currency_code == currency_code


@pytest.mark.parametrize(
    "currency_code",
    [None, 1, True, (), object()],
)
def test_currency_code_requires_string(currency_code: object) -> None:
    with pytest.raises(
        TypeError,
        match="currency_code must be a string",
    ):
        replace(
            create_currency_identity(),
            currency_code=currency_code,  # type: ignore[arg-type]
        )


def test_currency_code_must_not_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="currency_code must not be empty",
    ):
        replace(create_currency_identity(), currency_code="")


def test_whitespace_currency_code_is_not_normalized() -> None:
    identity = replace(create_currency_identity(), currency_code="   ")

    assert identity.currency_code == "   "


@pytest.mark.parametrize(
    "scheme_id",
    ["ISO-4217", "iso-4217", " custom ", "CUSTOM"],
)
def test_declared_scheme_id_is_preserved_literally(
    scheme_id: str,
) -> None:
    identity = replace(
        create_currency_identity(),
        currency_scheme_id=scheme_id,
    )

    assert identity.currency_scheme_id == scheme_id


@pytest.mark.parametrize(
    "scheme_id",
    [None, 1, True, (), object()],
)
def test_currency_scheme_id_requires_string(scheme_id: object) -> None:
    with pytest.raises(
        TypeError,
        match="currency_scheme_id must be a string",
    ):
        replace(
            create_currency_identity(),
            currency_scheme_id=scheme_id,  # type: ignore[arg-type]
        )


def test_currency_scheme_id_must_not_be_empty() -> None:
    with pytest.raises(
        ValueError,
        match="currency_scheme_id must not be empty",
    ):
        replace(create_currency_identity(), currency_scheme_id="")


def test_whitespace_scheme_id_is_not_normalized() -> None:
    identity = replace(
        create_currency_identity(),
        currency_scheme_id="   ",
    )

    assert identity.currency_scheme_id == "   "


@pytest.mark.parametrize(
    "version",
    [True, False, 1.0, "1", None, (), object()],
)
def test_currency_scheme_version_requires_strict_integer(
    version: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="currency_scheme_version must be an integer",
    ):
        replace(
            create_currency_identity(),
            currency_scheme_version=version,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("version", [0, -1, -100])
def test_currency_scheme_version_must_be_positive(
    version: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="currency_scheme_version must be positive",
    ):
        replace(
            create_currency_identity(),
            currency_scheme_version=version,
        )


@pytest.mark.parametrize("version", [1, 2, 100])
def test_positive_scheme_versions_are_preserved(version: int) -> None:
    identity = replace(
        create_currency_identity(),
        currency_scheme_version=version,
    )

    assert identity.currency_scheme_version == version


def test_equal_declarations_have_value_equality() -> None:
    first = create_currency_identity()
    second = create_currency_identity()

    assert first == second
    assert first is not second


def test_same_code_in_different_schemes_remains_distinct() -> None:
    first = create_currency_identity()
    second = replace(first, currency_scheme_id="CUSTOM")

    assert first.currency_code == second.currency_code
    assert first != second


def test_same_code_in_different_scheme_versions_remains_distinct() -> None:
    first = create_currency_identity()
    second = replace(first, currency_scheme_version=2)

    assert first.currency_code == second.currency_code
    assert first != second


def test_contract_introduces_no_monetary_behavior() -> None:
    module = inspect.getmodule(RetailCommercialCurrencyIdentity)
    assert module is not None
    source = inspect.getsource(module).lower()

    for forbidden_term in (
        ".strip(",
        ".upper(",
        ".lower(",
        "amount",
        "minor_unit",
        "exchange",
        "convert",
        "price",
        "cost",
        "margin",
        "requests",
        "notion",
        "openai",
        "subprocess",
    ):
        assert forbidden_term not in source
