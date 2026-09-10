from dataclasses import FrozenInstanceError, fields, replace
from datetime import UTC, datetime, timedelta, timezone
import inspect

import pytest

from sp001.contracts.retail_commercial_observation_period import (
    RetailCommercialObservationPeriod,
)


PERIOD_FROM = datetime(2026, 9, 1, 0, 0, tzinfo=UTC)
PERIOD_UNTIL = datetime(2026, 9, 8, 0, 0, tzinfo=UTC)


def create_period() -> RetailCommercialObservationPeriod:
    return RetailCommercialObservationPeriod(
        period_id="commercial-period-001",
        period_version=1,
        period_from=PERIOD_FROM,
        period_until=PERIOD_UNTIL,
    )


def test_commercial_period_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(RetailCommercialObservationPeriod)
    ) == (
        "period_id",
        "period_version",
        "period_from",
        "period_until",
    )


def test_commercial_period_is_immutable() -> None:
    period = create_period()

    with pytest.raises(FrozenInstanceError):
        period.period_version = 2  # type: ignore[misc]


def test_commercial_period_uses_slots() -> None:
    assert not hasattr(create_period(), "__dict__")


def test_commercial_period_preserves_exact_values() -> None:
    period = create_period()

    assert period.period_id == "commercial-period-001"
    assert period.period_version == 1
    assert period.period_from is PERIOD_FROM
    assert period.period_until is PERIOD_UNTIL


def test_equal_periods_are_deterministically_equal() -> None:
    assert create_period() == create_period()


def test_distinct_period_versions_remain_distinct() -> None:
    period = create_period()

    assert replace(period, period_version=2) != period


@pytest.mark.parametrize("value", ["", " ", "\t", None, 1])
def test_period_id_requires_nonempty_string(value: object) -> None:
    with pytest.raises(
        ValueError,
        match="period_id must not be empty",
    ):
        replace(
            create_period(),
            period_id=value,
        )


@pytest.mark.parametrize(
    "value",
    [True, False, 0, -1, 1.0, "1", None],
)
def test_period_version_requires_positive_integer(
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="period_version must be a positive integer",
    ):
        replace(
            create_period(),
            period_version=value,
        )


@pytest.mark.parametrize("value", [1, 2, 100])
def test_positive_period_version_is_accepted(
    value: int,
) -> None:
    period = replace(
        create_period(),
        period_version=value,
    )

    assert period.period_version == value


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("period_from", None),
        ("period_from", "2026-09-01T00:00:00Z"),
        ("period_until", None),
        ("period_until", "2026-09-08T00:00:00Z"),
    ],
)
def test_period_bounds_require_datetime(
    field_name: str,
    value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a datetime",
    ):
        replace(
            create_period(),
            **{field_name: value},
        )


@pytest.mark.parametrize(
    "field_name",
    ["period_from", "period_until"],
)
def test_period_bounds_require_timezone_awareness(
    field_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be timezone-aware",
    ):
        replace(
            create_period(),
            **{
                field_name: datetime(
                    2026,
                    9,
                    1,
                    0,
                    0,
                )
            },
        )


def test_period_until_must_not_equal_period_from() -> None:
    with pytest.raises(
        ValueError,
        match="period_until must be after period_from",
    ):
        replace(
            create_period(),
            period_until=PERIOD_FROM,
        )


def test_period_until_must_not_precede_period_from() -> None:
    with pytest.raises(
        ValueError,
        match="period_until must be after period_from",
    ):
        replace(
            create_period(),
            period_until=(
                PERIOD_FROM - timedelta(microseconds=1)
            ),
        )


def test_smallest_representable_positive_period_is_accepted() -> None:
    period = RetailCommercialObservationPeriod(
        period_id="commercial-period-001",
        period_version=1,
        period_from=PERIOD_FROM,
        period_until=(
            PERIOD_FROM + timedelta(microseconds=1)
        ),
    )

    assert period.period_until > period.period_from


def test_equivalent_instants_across_offsets_form_no_period() -> None:
    offset = timezone(timedelta(hours=-6))
    equivalent_until = PERIOD_FROM.astimezone(offset)

    with pytest.raises(
        ValueError,
        match="period_until must be after period_from",
    ):
        RetailCommercialObservationPeriod(
            period_id="commercial-period-001",
            period_version=1,
            period_from=PERIOD_FROM,
            period_until=equivalent_until,
        )


def test_period_has_no_implicit_calendar_frequency() -> None:
    field_names = {
        field.name
        for field in fields(RetailCommercialObservationPeriod)
    }

    assert field_names.isdisjoint(
        {
            "day",
            "week",
            "month",
            "quarter",
            "year",
            "frequency",
            "timezone",
        }
    )


def test_period_has_no_provenance_or_applicability_fields() -> None:
    field_names = {
        field.name
        for field in fields(RetailCommercialObservationPeriod)
    }

    assert field_names.isdisjoint(
        {
            "observed_at",
            "recorded_at",
            "effective_from",
            "effective_until",
            "evidence_ids",
            "source_identity",
        }
    )


def test_contract_adds_no_commercial_value_or_io_capability() -> None:
    module = __import__(
        "sp001.contracts.retail_commercial_observation_period",
        fromlist=["*"],
    )
    source = inspect.getsource(module).lower()

    forbidden = (
        "sales_units",
        "sell_through",
        "margin",
        "currency",
        "price",
        "requests",
        "notion",
        "openai",
        "subprocess",
        "pathlib",
    )

    assert all(term not in source for term in forbidden)
    assert not hasattr(
        RetailCommercialObservationPeriod,
        "contains",
    )
