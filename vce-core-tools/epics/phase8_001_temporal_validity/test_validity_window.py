from epics.phase8_001_temporal_validity.validity_window import (
    validity_active,
)


def test_validity_active():
    assert validity_active(365) is True


def test_validity_expired():
    assert validity_active(0) is False
