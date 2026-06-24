from epics.phase8_002_trust_expiration.expiration_record import (
    ExpirationRecord,
)


def test_expiration_record_creation():
    record = ExpirationRecord(
        expiration_id="exp.001",
        trust_id="trust.001",
        remaining_days=365,
    )

    assert record.remaining_days == 365


def test_requires_expiration_id():
    try:
        ExpirationRecord(
            "",
            "trust.001",
            365,
        )
        assert False
    except ValueError as exc:
        assert "expiration_id" in str(exc)
