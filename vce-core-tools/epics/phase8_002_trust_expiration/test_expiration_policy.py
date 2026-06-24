from epics.phase8_002_trust_expiration.expiration_policy import (
    trust_active,
)


def test_trust_active():
    assert trust_active(365) is True


def test_trust_expired():
    assert trust_active(0) is False
