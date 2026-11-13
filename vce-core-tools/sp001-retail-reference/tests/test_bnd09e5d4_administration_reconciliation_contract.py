from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.case_grant_administration_reconciliation import (
    AdministrationReconciliationResult,
    AdministrationReconciliationStatus,
)


@pytest.mark.parametrize(
    "status",
    list(AdministrationReconciliationStatus),
)
def test_accepts_each_defined_status(status):
    result = AdministrationReconciliationResult(
        event_id="EVENT-E5-1",
        status=status,
    )

    assert result.event_id == "EVENT-E5-1"
    assert result.status is status


@pytest.mark.parametrize(
    "event_id,error",
    [
        (None, TypeError),
        (123, TypeError),
        ("", ValueError),
        ("   ", ValueError),
    ],
)
def test_rejects_invalid_event_id(event_id, error):
    with pytest.raises(error):
        AdministrationReconciliationResult(
            event_id=event_id,
            status=AdministrationReconciliationStatus.EXACT_MATCH,
        )


@pytest.mark.parametrize(
    "status",
    [
        None,
        "EXACT_MATCH",
        "UNKNOWN",
        1,
    ],
)
def test_rejects_non_enum_status(status):
    with pytest.raises(TypeError):
        AdministrationReconciliationResult(
            event_id="EVENT-E5-1",
            status=status,
        )


def test_result_is_immutable():
    result = AdministrationReconciliationResult(
        event_id="EVENT-E5-1",
        status=AdministrationReconciliationStatus.EVENT_NOT_FOUND,
    )

    with pytest.raises(FrozenInstanceError):
        result.status = AdministrationReconciliationStatus.EXACT_MATCH


def test_result_has_no_dynamic_attributes():
    result = AdministrationReconciliationResult(
        event_id="EVENT-E5-1",
        status=AdministrationReconciliationStatus.READ_INVALID,
    )

    with pytest.raises(AttributeError):
        result.authorization = True
