from dataclasses import FrozenInstanceError, fields, replace
import inspect

import pytest

from sp001.contracts.retail_commercial_currency_identity import (
    RetailCommercialCurrencyIdentity,
)
from sp001.contracts.retail_commercial_monetary_amount import (
    RetailCommercialMonetaryAmount,
)


def create_currency_identity(
    *,
    currency_code: str = "MXN",
) -> RetailCommercialCurrencyIdentity:
    return RetailCommercialCurrencyIdentity(
        currency_code=currency_code,
        currency_scheme_id="ISO-4217",
        currency_scheme_version=1,
    )


def create_amount(
    *,
    minor_unit_amount: int = 125,
) -> RetailCommercialMonetaryAmount:
    return RetailCommercialMonetaryAmount(
        currency_identity=create_currency_identity(),
        minor_unit_amount=minor_unit_amount,
    )


def test_monetary_amount_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailCommercialMonetaryAmount)
    ) == (
        "currency_identity",
        "minor_unit_amount",
    )


def test_monetary_amount_is_immutable() -> None:
    amount = create_amount()

    with pytest.raises(FrozenInstanceError):
        amount.minor_unit_amount = 500  # type: ignore[misc]


def test_monetary_amount_uses_slots() -> None:
    assert not hasattr(create_amount(), "__dict__")


def test_exact_currency_identity_reference_is_preserved() -> None:
    currency = create_currency_identity()
    amount = RetailCommercialMonetaryAmount(
        currency_identity=currency,
        minor_unit_amount=125,
    )

    assert amount.currency_identity is currency


@pytest.mark.parametrize(
    "currency_identity",
    [None, "MXN", 1, True, object()],
)
def test_currency_identity_requires_exact_type(
    currency_identity: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "currency_identity must be a "
            "RetailCommercialCurrencyIdentity"
        ),
    ):
        replace(
            create_amount(),
            currency_identity=currency_identity,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "minor_unit_amount",
    [-10**30, -125, -1, 0, 1, 125, 10**30],
)
def test_signed_integer_amounts_are_preserved_exactly(
    minor_unit_amount: int,
) -> None:
    amount = create_amount(minor_unit_amount=minor_unit_amount)

    assert amount.minor_unit_amount == minor_unit_amount


@pytest.mark.parametrize(
    "minor_unit_amount",
    [True, False, 1.0, "125", None, (), object()],
)
def test_minor_unit_amount_requires_strict_integer(
    minor_unit_amount: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="minor_unit_amount must be an integer",
    ):
        create_amount(
            minor_unit_amount=minor_unit_amount,  # type: ignore[arg-type]
        )


def test_zero_amount_remains_distinct_from_missing_amount() -> None:
    zero = create_amount(minor_unit_amount=0)

    assert zero.minor_unit_amount == 0
    assert zero.minor_unit_amount is not None


def test_equal_reconstructed_amounts_have_value_equality() -> None:
    first = create_amount()
    second = create_amount()

    assert first == second
    assert first is not second
    assert first.currency_identity is not second.currency_identity


def test_equal_amounts_in_different_currencies_remain_distinct() -> None:
    mxn = create_amount()
    usd = replace(
        mxn,
        currency_identity=create_currency_identity(
            currency_code="USD",
        ),
    )

    assert mxn.minor_unit_amount == usd.minor_unit_amount
    assert mxn != usd


def test_amount_does_not_expose_decimal_value() -> None:
    amount = create_amount(minor_unit_amount=12345)

    assert not hasattr(amount, "decimal_amount")
    assert not hasattr(amount, "major_unit_amount")
    assert not hasattr(amount, "currency_exponent")


def test_amount_does_not_expose_commercial_meaning() -> None:
    field_names = {
        field.name
        for field in fields(RetailCommercialMonetaryAmount)
    }

    assert field_names.isdisjoint(
        {
            "price",
            "cost",
            "revenue",
            "margin",
            "tax",
            "discount",
        }
    )


def test_contract_introduces_no_conversion_or_arithmetic() -> None:
    module = inspect.getmodule(RetailCommercialMonetaryAmount)
    assert module is not None
    source = inspect.getsource(module).lower()

    for forbidden_term in (
        "decimal",
        "exponent",
        "exchange",
        "convert",
        "round(",
        "price",
        "cost",
        "revenue",
        "margin",
        "requests",
        "notion",
        "openai",
        "subprocess",
    ):
        assert forbidden_term not in source
