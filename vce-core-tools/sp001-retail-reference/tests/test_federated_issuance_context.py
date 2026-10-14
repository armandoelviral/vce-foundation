from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.federated_issuance_context import (
    ValidatedFederatedIssuanceContext,
)


def context():
    return ValidatedFederatedIssuanceContext(
        principal=AuthenticatedPrincipal("external", "subject"),
        audience="issuance-service",
        issued_at=100, not_before=110, expires_at=200,
    )


@pytest.mark.parametrize("at_time", [110, 150, 199])
def test_valid_interval(at_time):
    context().require_valid(
        expected_audience="issuance-service", at_time=at_time,
    )


@pytest.mark.parametrize("at_time", [109, 200, 201])
def test_outside_interval_is_rejected(at_time):
    with pytest.raises(PermissionError):
        context().require_valid(
            expected_audience="issuance-service", at_time=at_time,
        )


def test_wrong_audience_is_rejected():
    with pytest.raises(PermissionError):
        context().require_valid(expected_audience="coordinator", at_time=150)


@pytest.mark.parametrize("field", ["issued_at", "not_before", "expires_at"])
@pytest.mark.parametrize("value", [True, -1, 150.0, "150"])
def test_invalid_temporal_fields(field, value):
    with pytest.raises(ValueError):
        replace(context(), **{field: value})


@pytest.mark.parametrize("changes", [
    {"issued_at": 111},
    {"not_before": 200},
    {"expires_at": 110},
])
def test_invalid_interval(changes):
    with pytest.raises(ValueError):
        replace(context(), **changes)


def test_context_is_immutable():
    value = context()
    with pytest.raises(FrozenInstanceError):
        value.expires_at = 300
    assert not hasattr(value, "__dict__")


def test_expiry_can_be_checked_again_after_work():
    value = context()
    value.require_valid(expected_audience="issuance-service", at_time=199)
    with pytest.raises(PermissionError):
        value.require_valid(expected_audience="issuance-service", at_time=200)
