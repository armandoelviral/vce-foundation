from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.observation_mandate import (
    ObservationMandate,
)


def mandate(**overrides):
    values = {
        "mandate_id": "MANDATE-001",
        "issuer_id": "ISSUER-001",
        "observer_id": "OBSERVER-001",
        "host_id": "HOST-001",
        "resource_ids": ("RESOURCE-001",),
        "check_ids": ("HOST-P01",),
        "policy_version": "POLICY-001",
        "valid_from": 100,
        "valid_until": 200,
    }
    values.update(overrides)
    return ObservationMandate(**values)


def test_valid_mandate_preserves_values():
    result = mandate()
    assert result.observer_id == "OBSERVER-001"
    assert result.resource_ids == ("RESOURCE-001",)
    assert result.check_ids == ("HOST-P01",)


def test_all_host_checks_are_structurally_accepted():
    checks = tuple(
        f"HOST-P{i:02d}" for i in range(1, 11)
    )
    assert mandate(check_ids=checks).check_ids == checks


def test_mandate_is_immutable():
    result = mandate()
    with pytest.raises(FrozenInstanceError):
        result.host_id = "OTHER"


@pytest.mark.parametrize(
    "field",
    (
        "mandate_id",
        "issuer_id",
        "observer_id",
        "host_id",
        "policy_version",
    ),
)
@pytest.mark.parametrize("invalid", ("", " ", None, 7))
def test_invalid_identity_is_rejected(field, invalid):
    with pytest.raises(ValueError):
        mandate(**{field: invalid})


@pytest.mark.parametrize(
    "field",
    ("resource_ids", "check_ids"),
)
@pytest.mark.parametrize("invalid", (None, [], "VALUE"))
def test_collection_type_is_rejected(field, invalid):
    with pytest.raises(TypeError):
        mandate(**{field: invalid})


@pytest.mark.parametrize(
    "field",
    ("resource_ids", "check_ids"),
)
def test_empty_collection_is_rejected(field):
    with pytest.raises(ValueError):
        mandate(**{field: ()})


@pytest.mark.parametrize(
    "field",
    ("resource_ids", "check_ids"),
)
@pytest.mark.parametrize("invalid", ("", " ", None, 7))
def test_invalid_collection_member_is_rejected(
    field, invalid
):
    with pytest.raises(ValueError):
        mandate(**{field: (invalid,)})


@pytest.mark.parametrize(
    "field,values",
    (
        ("resource_ids", ("R1", "R1")),
        ("check_ids", ("HOST-P01", "HOST-P01")),
    ),
)
def test_duplicate_members_are_rejected(field, values):
    with pytest.raises(ValueError):
        mandate(**{field: values})


@pytest.mark.parametrize(
    "invalid",
    ("HOST-P00", "HOST-P11", "OTHER"),
)
def test_unknown_host_check_is_rejected(invalid):
    with pytest.raises(ValueError):
        mandate(check_ids=(invalid,))


@pytest.mark.parametrize(
    "field",
    ("valid_from", "valid_until"),
)
@pytest.mark.parametrize(
    "invalid",
    (None, True, False, 1.5, "100"),
)
def test_invalid_timestamp_type_is_rejected(field, invalid):
    with pytest.raises(TypeError):
        mandate(**{field: invalid})


def test_negative_start_is_rejected():
    with pytest.raises(ValueError):
        mandate(valid_from=-1)


def test_negative_end_is_rejected():
    with pytest.raises(ValueError):
        mandate(valid_until=-1)


def test_equal_timestamps_are_rejected():
    with pytest.raises(ValueError):
        mandate(valid_from=100, valid_until=100)


def test_reversed_interval_is_rejected():
    with pytest.raises(ValueError):
        mandate(valid_from=200, valid_until=100)


def test_construction_does_not_grant_authority():
    result = mandate()
    for field in (
        "authorized",
        "trusted",
        "verified",
        "eligible",
    ):
        assert not hasattr(result, field)


def test_replacement_preserves_validation():
    result = mandate()
    with pytest.raises(ValueError):
        replace(result, host_id="")
